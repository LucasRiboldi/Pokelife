using System.Globalization;
using Dapper;
using Microsoft.Data.Sqlite;
using TaskbarHabitat.Core;

namespace TaskbarHabitat.Data;

public sealed class SaveService(SqliteConnection connection)
{
    public string? GetSavedStarterName() => connection.QuerySingleOrDefault<string>("""
        SELECT species.display_name
        FROM save_state
        JOIN species ON species.id = save_state.starter_id
        WHERE save_state.id = 1
        """);

    public SaveState CreateNewSave(int starterId)
    {
        if (starterId is not (1 or 4 or 7))
            throw new ArgumentOutOfRangeException(nameof(starterId), starterId, "Choose Bulbasaur, Charmander, or Squirtle.");

        var now = DateTime.UtcNow;
        var save = new SaveState(Guid.NewGuid(), starterId, 0, 1, now, now, 0);
        string timestamp = now.ToString("O", CultureInfo.InvariantCulture);

        using var transaction = connection.BeginTransaction();
        connection.Execute("""
            INSERT INTO save_state
                (id, starter_id, xp, level, last_seen_utc, game_epoch_utc, total_ticks, save_id, created_at_utc)
            VALUES (1, @StarterId, @Xp, @Level, @Timestamp, @Timestamp, @TotalTicks, @SaveId, @Timestamp);
            INSERT INTO creature_state (save_id, last_updated_utc) VALUES (1, @Timestamp);
            """, new
            {
                save.StarterId,
                save.Xp,
                save.Level,
                save.TotalTicks,
                SaveId = save.SaveId.ToString("D"),
                Timestamp = timestamp
            }, transaction);
        transaction.Commit();
        return save;
    }
}
