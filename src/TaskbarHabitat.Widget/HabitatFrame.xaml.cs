using Microsoft.UI.Input;
using Microsoft.UI.Windowing;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Windows.Graphics;
using WinRT.Interop;

namespace TaskbarHabitat.Widget;

public sealed partial class HabitatFrame : UserControl
{
    private AppWindow appWindow = null!;
    private nint hwnd;
    private (int Width, int Height, int Left, int Top) appliedRegion;
    private uint? dragPointer;
    private PointInt32 grabOffset;

    public HabitatFrame() => InitializeComponent();

    internal Grid Viewport => HabitatViewport;

    internal void Attach(Window window)
    {
        appWindow = window.AppWindow;
        hwnd = WindowNative.GetWindowHandle(window);
        ApplyRegion();

        appWindow.Changed += OnWindowChanged;
        window.Closed += (_, _) => appWindow.Changed -= OnWindowChanged;
    }

    private void OnWindowChanged(AppWindow sender, AppWindowChangedEventArgs args)
    {
        if (args.DidSizeChange || args.DidPresenterChange)
            ApplyRegion();
    }

    private void ApplyRegion()
    {
        if (appWindow.Presenter is OverlappedPresenter { State: OverlappedPresenterState.Minimized })
            return;

        var client = appWindow.ClientSize;
        if (client.Width <= 0 || client.Height <= 0)
            return;

        var offset = HabitatFrameNative.GetClientOffset(hwnd);
        var region = (client.Width, client.Height, offset.X, offset.Y);
        if (region == appliedRegion)
            return;

        // SetWindowRgn can send a window-position notification before it returns.
        appliedRegion = region;
        HabitatFrameNative.SetRegion(hwnd, client, offset);
    }

    private void OnDragPressed(object sender, PointerRoutedEventArgs args)
    {
        var pointer = args.Pointer;
        if (dragPointer is not null ||
            pointer.PointerDeviceType != PointerDeviceType.Mouse ||
            !args.GetCurrentPoint(DragSurface).Properties.IsLeftButtonPressed ||
            !HabitatFrameNative.TryGetCursorPosition(out var pointerPosition) ||
            !DragSurface.CapturePointer(pointer))
            return;

        var windowPosition = appWindow.Position;
        grabOffset = new PointInt32(pointerPosition.X - windowPosition.X,
            pointerPosition.Y - windowPosition.Y);
        dragPointer = pointer.PointerId;
        args.Handled = true;
    }

    private void OnDragMoved(object sender, PointerRoutedEventArgs args)
    {
        if (dragPointer != args.Pointer.PointerId ||
            !args.GetCurrentPoint(DragSurface).Properties.IsLeftButtonPressed ||
            !HabitatFrameNative.TryGetCursorPosition(out var pointerPosition))
            return;

        appWindow.Move(new PointInt32(pointerPosition.X - grabOffset.X,
            pointerPosition.Y - grabOffset.Y));
        args.Handled = true;
    }

    private void OnDragReleased(object sender, PointerRoutedEventArgs args)
    {
        if (dragPointer != args.Pointer.PointerId ||
            args.GetCurrentPoint(DragSurface).Properties.IsLeftButtonPressed)
            return;

        dragPointer = null;
        DragSurface.ReleasePointerCapture(args.Pointer);
        args.Handled = true;
    }

    private void OnDragEnded(object sender, PointerRoutedEventArgs args)
    {
        if (dragPointer == args.Pointer.PointerId)
            dragPointer = null;
    }
}
