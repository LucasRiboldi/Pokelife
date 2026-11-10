using Dapper;
using Microsoft.Data.Sqlite;

namespace TaskbarHabitat.Data;

public static class Database
{
    private const int SchemaVersion = 1;

    public static void Initialize(SqliteConnection connection)
    {
        connection.Execute("PRAGMA foreign_keys = ON");
        using var transaction = connection.BeginTransaction();
        int version = connection.ExecuteScalar<int>("PRAGMA user_version", transaction: transaction);

        if (version > SchemaVersion)
            throw new InvalidOperationException($"SQLite schema version {version} is newer than supported version {SchemaVersion}.");

        if (version == 0)
        {
            using var script = typeof(Database).Assembly.GetManifestResourceStream(
                "TaskbarHabitat.Data.Migrations.001_initial.sql")
                ?? throw new InvalidOperationException("The initial SQLite migration is missing.");
            using var reader = new StreamReader(script);
            connection.Execute(reader.ReadToEnd(), transaction: transaction);
            connection.Execute($"PRAGMA user_version = {SchemaVersion}", transaction: transaction);
        }

        transaction.Commit();
    }
}
