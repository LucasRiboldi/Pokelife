using System.Globalization;
using Dapper;
using Microsoft.Data.Sqlite;
using TaskbarHabitat.Data;

namespace TaskbarHabitat.Simulation.Tests;

public sealed class DataTests : IDisposable
{
    private readonly SqliteConnection connection = new("Data Source=:memory:");

    public DataTests()
    {
        connection.Open();
    }

    [Fact]
    public void InitializationSeedsTheHabitatAndEnablesForeignKeys()
    {
        Database.Initialize(connection);
        Database.Initialize(connection);

        Assert.Equal(9, connection.QuerySingle<int>("SELECT COUNT(*) FROM species"));
        Assert.Equal(6, connection.QuerySingle<int>("SELECT COUNT(*) FROM evolutions"));
        Assert.Equal("viridian-forest", connection.QuerySingle<string>("SELECT id FROM habitats"));
        Assert.Equal(new[] { 1, 4, 7 }, connection.Query<int>("SELECT species_id FROM encounters ORDER BY species_id"));
        Assert.Equal(1, connection.QuerySingle<int>("PRAGMA foreign_keys"));
    }

    [Theory]
    [InlineData(1)]
    [InlineData(4)]
    [InlineData(7)]
    public void CreateNewSaveStoresStarterAndCreatureDefaults(int starterId)
    {
        Database.Initialize(connection);

        var save = new SaveService(connection).CreateNewSave(starterId);

        Assert.Equal(starterId, save.StarterId);
        Assert.Equal(0, save.Xp);
        Assert.Equal(1, save.Level);
        Assert.Equal(0, save.TotalTicks);
        Assert.NotEqual(Guid.Empty, save.SaveId);
        Assert.Equal(DateTimeKind.Utc, save.LastSeenUtc.Kind);
        Assert.Equal(save.LastSeenUtc, save.GameEpochUtc);

        var storedSave = connection.QuerySingle<(int StarterId, int Xp, int Level, long TotalTicks, string SaveId, string LastSeen, string Epoch)>(
            "SELECT starter_id, xp, level, total_ticks, save_id, last_seen_utc, game_epoch_utc FROM save_state WHERE id = 1");
        Assert.Equal((starterId, 0, 1, 0L, save.SaveId.ToString("D"),
            save.LastSeenUtc.ToString("O", CultureInfo.InvariantCulture),
            save.GameEpochUtc.ToString("O", CultureInfo.InvariantCulture)), storedSave);

        var creature = connection.QuerySingle<(double Hunger, double Energy, double Happiness, string LastUpdated)>(
            "SELECT hunger, energy, happiness, last_updated_utc FROM creature_state WHERE save_id = 1");
        Assert.Equal((0d, 100d, 50d, storedSave.LastSeen), creature);
    }

    [Fact]
    public void CreateNewSaveRejectsNonStarter()
    {
        Database.Initialize(connection);

        Assert.Throws<ArgumentOutOfRangeException>(() => new SaveService(connection).CreateNewSave(2));
        Assert.Equal(0, connection.QuerySingle<int>("SELECT COUNT(*) FROM save_state"));
    }

    [Fact]
    public void CreateNewSaveRollsBackIfCreatureInsertFails()
    {
        Database.Initialize(connection);
        connection.Execute("""
            CREATE TRIGGER reject_creature BEFORE INSERT ON creature_state
            BEGIN
                SELECT RAISE(ABORT, 'test failure');
            END;
            """);

        Assert.Throws<SqliteException>(() => new SaveService(connection).CreateNewSave(1));
        Assert.Equal(0, connection.QuerySingle<int>("SELECT COUNT(*) FROM save_state"));
        Assert.Equal(0, connection.QuerySingle<int>("SELECT COUNT(*) FROM creature_state"));
    }

    [Fact]
    public void ExistingSaveSurvivesReopeningAndRejectsReplacement()
    {
        var path = Path.GetTempFileName();
        var connectionString = new SqliteConnectionStringBuilder { DataSource = path, Pooling = false }.ToString();
        try
        {
            Guid saveId;
            using (var file = new SqliteConnection(connectionString))
            {
                file.Open();
                Database.Initialize(file);
                var service = new SaveService(file);
                Assert.Null(service.GetSavedStarterName());
                saveId = service.CreateNewSave(7).SaveId;
            }

            using var reopened = new SqliteConnection(connectionString);
            reopened.Open();
            Database.Initialize(reopened);
            var reopenedService = new SaveService(reopened);
            Assert.Equal("Squirtle", reopenedService.GetSavedStarterName());
            Assert.Throws<SqliteException>(() => reopenedService.CreateNewSave(1));
            Assert.Equal(saveId.ToString("D"), reopened.QuerySingle<string>("SELECT save_id FROM save_state"));
            Assert.Equal(7, reopened.QuerySingle<int>("SELECT starter_id FROM save_state"));
            Assert.Equal(1, reopened.QuerySingle<int>("SELECT COUNT(*) FROM creature_state"));
        }
        finally
        {
            File.Delete(path);
        }
    }

    public void Dispose() => connection.Dispose();
}
