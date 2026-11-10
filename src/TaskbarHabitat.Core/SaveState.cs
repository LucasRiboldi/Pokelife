namespace TaskbarHabitat.Core;

public sealed record SaveState(
    Guid SaveId,
    int StarterId,
    int Xp,
    int Level,
    DateTime LastSeenUtc,
    DateTime GameEpochUtc,
    long TotalTicks);
