using System.Diagnostics;
using Microsoft.UI;
using Microsoft.UI.Dispatching;
using Microsoft.UI.Windowing;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Automation;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Media.Imaging;
using Microsoft.UI.Xaml.Shapes;
using Windows.Foundation;
using Windows.Graphics;
using VirtualKey = Windows.System.VirtualKey;

namespace TaskbarHabitat.Widget;

internal sealed class HabitatWindow : Window
{
    private const int SpriteScale = 2;
    private const int DisplayCellSize = CharmanderAnimation.CellSize * SpriteScale;
    private const int DepthPerPixel = 4;
    private const double WalkSpeed = 44;

    private readonly string starterName;
    private readonly HabitatNavigation navigation;
    private readonly Canvas scene;
    private readonly Canvas camera;
    private readonly Canvas creatureViewport;
    private readonly ViridianScenery scenery;
    private readonly bool animated;
    private readonly Ellipse shadow;
    private readonly CompositeTransform creaturePose = new();
    private readonly TranslateTransform creatureFrame = new();
    private readonly TranslateTransform shadowOffset = new();
    private readonly TextBlock activity = new() { FontSize = 10, Foreground = new SolidColorBrush(Colors.White) };
    private readonly DispatcherQueueTimer timer;
    private HabitatNavigation.Cell currentCell;
    private HabitatNavigation.Cell[] route = [];
    private int routeStep;
    private int nextDestination;
    private HabitatNavigation.Destination? destination;
    private Point creatureFeet;
    private double cameraX;
    private double cameraY;
    private double distance;
    private double pauseRemaining;
    private double stepTime;
    private double strideDistance;
    private double? restElapsed;
    private TimeSpan sceneElapsed;
    private long previousTick;

    public HabitatWindow(string starterName, ISpriteProvider sprites)
    {
        this.starterName = starterName;
        Title = "Floresta de Viridian — Taskbar Habitat";

        navigation = HabitatNavigation.Load(ViridianScenery.AssetPath("navigation.json"));
        var background = LoadHabitatImage("solo.png");
        Canvas.SetZIndex(background, -2);
        shadow = new Ellipse
        {
            Width = 24,
            Height = 7,
            Fill = new SolidColorBrush(ColorHelper.FromArgb(96, 26, 48, 33)),
            RenderTransform = shadowOffset
        };
        var animation = string.Equals(starterName, "Charmander", StringComparison.OrdinalIgnoreCase)
            ? sprites.GetCharmanderAnimation()
            : null;
        animated = animation is not null;
        int cellSize = animated ? DisplayCellSize : CharmanderAnimation.CellSize;
        var creature = new Image
        {
            Source = animation ?? sprites.GetSprite(starterName),
            Width = cellSize * (animated ? CharmanderAnimation.Columns : 1),
            Height = cellSize * (animated ? CharmanderAnimation.Rows : 1),
            Stretch = Stretch.Fill,
            RenderTransform = creatureFrame
        };
        creatureViewport = new Canvas
        {
            Width = cellSize,
            Height = cellSize,
            Clip = new RectangleGeometry { Rect = new Rect(0, 0, cellSize, cellSize) },
            RenderTransformOrigin = new Point(0.5, 0.5),
            RenderTransform = creaturePose,
            Children = { creature }
        };
        AutomationProperties.SetName(creatureViewport, starterName);
        if (animated)
            ShowFrame(CharmanderAnimation.FrontIdle);

        var nameplate = new Border
        {
            Padding = new Thickness(5, 3, 5, 3),
            Background = new SolidColorBrush(ColorHelper.FromArgb(240, 31, 57, 42)),
            BorderBrush = new SolidColorBrush(ColorHelper.FromArgb(255, 147, 176, 108)),
            BorderThickness = new Thickness(0.5),
            CornerRadius = new CornerRadius(2),
            Child = new StackPanel
            {
                Spacing = 1,
                Children =
                {
                    new TextBlock
                    {
                        Text = "FLORESTA DE VIRIDIAN",
                        FontSize = 13,
                        FontWeight = Microsoft.UI.Text.FontWeights.SemiBold,
                        Foreground = new SolidColorBrush(ColorHelper.FromArgb(255, 244, 224, 161))
                    },
                    activity
                }
            }
        };
        Canvas.SetLeft(nameplate, 6);
        Canvas.SetTop(nameplate, 6);

        scene = new Canvas
        {
            Width = navigation.Width,
            Height = navigation.Height,
            Children = { background, shadow, creatureViewport }
        };
        scenery = new ViridianScenery(scene);
        var collisionOverlay = LoadHabitatImage("grade.png");
        collisionOverlay.Visibility = Visibility.Collapsed;
        collisionOverlay.IsHitTestVisible = false;
        Canvas.SetZIndex(collisionOverlay, (navigation.Height + 1) * DepthPerPixel);
        scene.Children.Add(collisionOverlay);
        camera = new Canvas
        {
            Width = Math.Min(768, navigation.Width),
            Height = Math.Min(432, navigation.Height),
            Children = { scene, nameplate }
        };
        camera.Clip = new RectangleGeometry { Rect = new Rect(0, 0, camera.Width, camera.Height) };
        Canvas.SetZIndex(nameplate, 1);
        var toggleGrid = new Microsoft.UI.Xaml.Input.KeyboardAccelerator { Key = VirtualKey.F2 };
        toggleGrid.Invoked += (_, args) =>
        {
            collisionOverlay.Visibility = collisionOverlay.Visibility == Visibility.Visible
                ? Visibility.Collapsed : Visibility.Visible;
            args.Handled = true;
        };
        var root = new Grid
        {
            Background = new SolidColorBrush(ColorHelper.FromArgb(255, 25, 42, 32)),
            Children = { new Viewbox { Child = camera, Stretch = Stretch.Uniform } }
        };
        root.KeyboardAccelerators.Add(toggleGrid);
        Content = root;

        var area = DisplayArea.GetFromWindowId(AppWindow.Id, DisplayAreaFallback.Primary).WorkArea;
        AppWindow.MoveAndResize(new RectInt32(
            area.X + area.Width / 12, area.Y + area.Height / 12,
            area.Width * 5 / 6, area.Height * 5 / 6));

        activity.Text = $"{starterName} · Caminhando";
        currentCell = navigation.Spawn;
        PlaceCreature(Position(currentCell), 0);
        FollowCreature(1);
        timer = DispatcherQueue.CreateTimer();
        timer.Interval = TimeSpan.FromMilliseconds(40);
        timer.Tick += Walk;
        var appWindow = AppWindow;
        appWindow.Changed += UpdateTimer;
        Closed += (_, _) =>
        {
            appWindow.Changed -= UpdateTimer;
            timer.Stop();
        };
        previousTick = Stopwatch.GetTimestamp();
        timer.Start();
    }

    private void UpdateTimer(AppWindow sender, AppWindowChangedEventArgs args)
    {
        if (sender.Presenter is OverlappedPresenter { State: OverlappedPresenterState.Minimized })
            timer.Stop();
        else if (!timer.IsRunning)
        {
            previousTick = Stopwatch.GetTimestamp();
            timer.Start();
        }
    }

    private void Walk(DispatcherQueueTimer sender, object args)
    {
        long now = Stopwatch.GetTimestamp();
        double elapsed = Math.Min(Stopwatch.GetElapsedTime(previousTick, now).TotalSeconds, 0.12);
        previousTick = now;
        sceneElapsed += TimeSpan.FromSeconds(elapsed);
        scenery.Animate(sceneElapsed);
        FollowCreature(1 - Math.Exp(-elapsed * 3));

        if (restElapsed is double resting)
        {
            restElapsed = resting + elapsed;
            if (CharmanderAnimation.RestFrame(restElapsed.Value) is int frame)
            {
                ShowFrame(frame);
                return;
            }

            restElapsed = null;
            activity.Text = $"{starterName} · Caminhando";
        }

        if (pauseRemaining > 0)
        {
            pauseRemaining -= elapsed;
            if (pauseRemaining <= 0)
                activity.Text = $"{starterName} · Caminhando";
            return;
        }

        if (routeStep >= route.Length && !ChooseRoute())
        {
            activity.Text = $"{starterName} · Parado";
            pauseRemaining = 2;
            return;
        }

        Point start = Position(route[routeStep - 1]);
        Point end = Position(route[routeStep]);
        double dx = end.X - start.X;
        double dy = end.Y - start.Y;
        double length = Math.Sqrt(dx * dx + dy * dy);
        double advance = Math.Min(elapsed * WalkSpeed, length - distance);
        distance += advance;
        strideDistance += advance;
        stepTime += elapsed;

        creaturePose.ScaleX = dx > 0 ? -1 : 1;
        int walkingFrame = 0;
        if (animated)
        {
            walkingFrame = CharmanderAnimation.WalkFrame(dx, dy, strideDistance / SpriteScale);
            ShowFrame(walkingFrame);
        }

        if (distance < length)
        {
            double fraction = distance / length;
            var position = new Point(start.X + dx * fraction, start.Y + dy * fraction);
            PlaceCreature(position, animated ? 0 : Math.Abs(Math.Sin(stepTime * 10)));
            return;
        }

        currentCell = route[routeStep++];
        distance = 0;
        PlaceCreature(end, 0);
        if (routeStep < route.Length || destination is null)
            return;

        activity.Text = $"{starterName} · {destination.Activity}";
        if (animated && destination.Rest)
        {
            restElapsed = 0;
            ShowFrame(CharmanderAnimation.FrontIdle);
        }
        else
        {
            if (animated)
                ShowFrame(CharmanderAnimation.FrontIdle + walkingFrame / CharmanderAnimation.Columns);
            pauseRemaining = 1.5 + Random.Shared.NextDouble() * 1.5;
        }
    }

    private bool ChooseRoute()
    {
        for (int attempts = 0; attempts < navigation.Destinations.Count; attempts++)
        {
            var target = navigation.Destinations[nextDestination];
            nextDestination = (nextDestination + 1) % navigation.Destinations.Count;
            var candidate = navigation.FindPath(currentCell, target.Cell);
            if (candidate.Length > 1)
            {
                route = candidate;
                routeStep = 1;
                destination = target;
                return true;
            }
        }
        return false;
    }

    private Point Position(HabitatNavigation.Cell cell)
    {
        var (x, y) = navigation.Center(cell);
        return new Point(x, y);
    }

    private void FollowCreature(double fraction)
    {
        double targetX = Math.Clamp(creatureFeet.X - camera.Width / 2, 0, scene.Width - camera.Width);
        double targetY = Math.Clamp(creatureFeet.Y - camera.Height / 2, 0, scene.Height - camera.Height);
        cameraX += (targetX - cameraX) * fraction;
        cameraY += (targetY - cameraY) * fraction;
        Canvas.SetLeft(scene, -Math.Round(cameraX));
        Canvas.SetTop(scene, -Math.Round(cameraY));
    }

    private Image LoadHabitatImage(string fileName) => new()
    {
        Source = new BitmapImage(new Uri($"ms-appx:///Assets/Habitats/{ViridianScenery.AssetFolder}/{fileName}")),
        Width = navigation.Width,
        Height = navigation.Height,
        Stretch = Stretch.Fill
    };

    private void ShowFrame(int frame)
    {
        int cellSize = DisplayCellSize;
        creatureFrame.X = -(frame % CharmanderAnimation.Columns) * cellSize;
        creatureFrame.Y = -(frame / CharmanderAnimation.Columns) * cellSize;
    }

    private void PlaceCreature(Point feet, double bounce)
    {
        creatureFeet = feet;
        int depth = (int)Math.Round(feet.Y) * DepthPerPixel + 3;
        Canvas.SetZIndex(shadow, depth);
        Canvas.SetZIndex(creatureViewport, depth);
        shadowOffset.X = Math.Round(feet.X - shadow.Width / 2);
        shadowOffset.Y = Math.Round(feet.Y - shadow.Height / 2);
        creaturePose.TranslateX = Math.Round(feet.X - creatureViewport.Width / 2);
        creaturePose.TranslateY = Math.Round(feet.Y - creatureViewport.Height + creatureViewport.Height / 8 - bounce);
    }
}
