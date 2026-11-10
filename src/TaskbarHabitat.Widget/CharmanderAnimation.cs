namespace TaskbarHabitat.Widget;

internal static class CharmanderAnimation
{
    public const int CellSize = 32;
    public const int Columns = 4;
    public const int Rows = 5;
    public const int FrontIdle = 12;

    public static int WalkFrame(double dx, double dy, double distance)
    {
        int view = Math.Abs(dx) >= Math.Abs(dy) ? 1 : dy > 0 ? 0 : 2;
        int step = (int)(distance / 2) % Columns;
        return view * Columns + step;
    }

    public static int? RestFrame(double seconds) => seconds switch
    {
        < .2 => FrontIdle,
        < .55 => 15, // Lower into the sit.
        < 1.2 => 16,
        < 1.55 => 17, // Tuck the head down.
        < 4 => (int)((seconds - 1.55) / .6) % 2 == 0 ? 18 : 19,
        < 4.3 => 17,
        < 4.65 => 16,
        < 4.95 => 15,
        < 5.2 => FrontIdle,
        _ => null
    };
}
