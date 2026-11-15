using System.ComponentModel;
using System.Runtime.InteropServices;
using Windows.Graphics;

namespace TaskbarHabitat.Widget;

internal static class HabitatFrameNative
{
    private const int ArtworkWidth = 307;
    private const int ArtworkHeight = 288;
    private const int RegionOr = 2;

    // Row bands extracted from habitat-frame.png by removing the exterior #C9B0A0.
    // Coordinates are half-open. The center stays inside the region for the habitat.
    private static readonly (int Top, int Bottom, int Left, int Right)[] Outline =
    [
        (3, 4, 14, 293),
        (4, 5, 11, 295),
        (5, 6, 10, 297),
        (6, 7, 8, 298),
        (7, 8, 7, 299),
        (8, 9, 6, 300),
        (9, 10, 6, 301),
        (10, 11, 5, 302),
        (11, 12, 4, 302),
        (12, 13, 4, 303),
        (13, 14, 3, 303),
        (14, 17, 3, 304),
        (17, 225, 2, 305),
        (225, 239, 2, 304),
        (239, 244, 2, 303),
        (244, 247, 2, 302),
        (247, 250, 2, 301),
        (250, 252, 2, 300),
        (252, 255, 2, 299),
        (255, 256, 2, 298),
        (256, 258, 2, 297),
        (258, 259, 2, 296),
        (259, 261, 2, 295),
        (261, 262, 2, 294),
        (262, 264, 2, 293),
        (264, 265, 2, 292),
        (265, 266, 2, 291),
        (266, 267, 2, 290),
        (267, 268, 3, 289),
        (268, 269, 3, 288),
        (269, 270, 3, 287),
        (270, 271, 3, 286),
        (271, 272, 3, 285),
        (272, 273, 3, 284),
        (273, 274, 3, 282),
        (274, 275, 3, 281),
        (275, 276, 4, 280),
        (276, 277, 4, 278),
        (277, 278, 5, 277),
        (278, 279, 6, 275),
        (279, 280, 6, 273),
        (280, 281, 7, 271),
        (281, 282, 8, 269),
        (282, 283, 10, 266),
        (283, 284, 11, 263),
        (284, 285, 13, 260),
        (285, 286, 17, 254),
    ];

    internal static PointInt32 GetClientOffset(nint hwnd)
    {
        var clientOrigin = new NativePoint();
        if (!GetWindowRect(hwnd, out var window) || !ClientToScreen(hwnd, ref clientOrigin))
            throw new Win32Exception(Marshal.GetLastWin32Error());

        return new PointInt32(clientOrigin.X - window.Left, clientOrigin.Y - window.Top);
    }

    internal static bool TryGetCursorPosition(out PointInt32 position)
    {
        bool success = GetCursorPos(out var point);
        position = new PointInt32(point.X, point.Y);
        return success;
    }

    internal static void SetRegion(nint hwnd, SizeInt32 client, PointInt32 clientOffset)
    {
        double scale = Math.Min((double)client.Width / ArtworkWidth, (double)client.Height / ArtworkHeight);
        double originX = clientOffset.X + (client.Width - ArtworkWidth * scale) / 2;
        double originY = clientOffset.Y + (client.Height - ArtworkHeight * scale) / 2;

        int X(int x) => (int)Math.Round(originX + x * scale);
        int Y(int y) => (int)Math.Round(originY + y * scale);

        nint region = CreateRectRgn(0, 0, 0, 0);
        nint band = CreateRectRgn(0, 0, 0, 0);
        try
        {
            if (region == 0 || band == 0)
                throw new InvalidOperationException("Could not allocate the habitat window region.");

            foreach (var (top, bottom, left, right) in Outline)
            {
                if (!SetRectRgn(band, X(left), Y(top), X(right), Y(bottom)) ||
                    CombineRgn(region, region, band, RegionOr) == 0)
                    throw new InvalidOperationException("Could not build the habitat window region.");
            }

            if (SetWindowRgn(hwnd, region, true) == 0)
                throw new InvalidOperationException("Could not apply the habitat window region.");

            region = 0; // The system owns the region after SetWindowRgn succeeds.
        }
        finally
        {
            if (band != 0)
                DeleteObject(band);
            if (region != 0)
                DeleteObject(region);
        }
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct NativePoint
    {
        public int X;
        public int Y;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct NativeRect
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool GetWindowRect(nint hwnd, out NativeRect rect);

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool ClientToScreen(nint hwnd, ref NativePoint point);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool GetCursorPos(out NativePoint point);

    [DllImport("user32.dll")]
    private static extern int SetWindowRgn(nint hwnd, nint region, [MarshalAs(UnmanagedType.Bool)] bool redraw);

    [DllImport("gdi32.dll")]
    private static extern nint CreateRectRgn(int left, int top, int right, int bottom);

    [DllImport("gdi32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool SetRectRgn(nint region, int left, int top, int right, int bottom);

    [DllImport("gdi32.dll")]
    private static extern int CombineRgn(nint destination, nint first, nint second, int mode);

    [DllImport("gdi32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool DeleteObject(nint handle);
}
