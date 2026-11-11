namespace TaskbarHabitat.Widget;

internal static class ViridianWater
{
    public const int Left = 248;
    public const int Width = 136;
    public const int Height = 288;
    public const int Columns = 4;
    public const int Rows = 2;

    public static int FrameAt(TimeSpan elapsed) =>
        (int)(elapsed.Ticks / (110 * TimeSpan.TicksPerMillisecond) % (Columns * Rows));
}
