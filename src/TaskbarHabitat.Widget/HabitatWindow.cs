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

namespace TaskbarHabitat.Widget;

internal sealed class HabitatWindow : Window
{
    private const string GrassRest = "Descansando no gramado";
    private const int SceneWidth = 384;
    private const int SceneHeight = 216;

    // These points cross the trail and open meadow in viridian-valley.png.
    private static readonly (Point Position, string? Pause)[] Trail =
    [
        (new(95, 154), null), (new(119, 143), null), (new(137, 130), null),
        (new(154, 115), null), (new(166, 106), null), (new(179, 102), "Explorando a caverna"),
        (new(199, 111), null), (new(220, 122), null), (new(242, 132), null),
        (new(261, 142), "Observando o rio"), (new(244, 151), null), (new(224, 161), null),
        (new(198, 172), null), (new(174, 178), null), (new(150, 183), GrassRest),
        (new(125, 175), null), (new(108, 161), null), (new(87, 158), null),
        (new(72, 155), null)
    ];

    private readonly string starterName;
    private readonly Canvas creatureViewport;
    private readonly Image creature;
    private readonly Image water;
    private readonly bool animated;
    private readonly Ellipse shadow;
    private readonly ScaleTransform facing = new();
    private readonly TextBlock activity = new() { FontSize = 4, Foreground = new SolidColorBrush(Colors.White) };
    private readonly DispatcherQueueTimer timer;
    private int waypoint;
    private double distance;
    private double pauseRemaining;
    private double stepTime;
    private double strideDistance;
    private double? restElapsed;
    private readonly long waterStart;
    private int waterFrame;
    private long previousTick;

    public HabitatWindow(string starterName, ISpriteProvider sprites)
    {
        this.starterName = starterName;
        Title = "Floresta de Viridian — Taskbar Habitat";

        var background = LoadHabitatImage("viridian-valley.png", SceneWidth, SceneHeight);
        var foreground = LoadHabitatImage("viridian-foreground.png", SceneWidth, SceneHeight);
        water = LoadHabitatImage("viridian-water.png", ViridianWater.Width * ViridianWater.Columns,
            ViridianWater.Height * ViridianWater.Rows);
        var waterViewport = new Canvas
        {
            Width = ViridianWater.Width,
            Height = ViridianWater.Height,
            Clip = new RectangleGeometry { Rect = new Rect(0, 0, ViridianWater.Width, ViridianWater.Height) },
            Children = { water }
        };
        Canvas.SetLeft(waterViewport, ViridianWater.Left);
        shadow = new Ellipse
        {
            Width = 13,
            Height = 4,
            Fill = new SolidColorBrush(ColorHelper.FromArgb(96, 26, 48, 33))
        };
        var animation = string.Equals(starterName, "Charmander", StringComparison.OrdinalIgnoreCase)
            ? sprites.GetCharmanderAnimation()
            : null;
        animated = animation is not null;
        int cellSize = CharmanderAnimation.CellSize;
        creature = new Image
        {
            Source = animation ?? sprites.GetSprite(starterName),
            Width = cellSize * (animated ? CharmanderAnimation.Columns : 1),
            Height = cellSize * (animated ? CharmanderAnimation.Rows : 1),
            Stretch = Stretch.Fill
        };
        creatureViewport = new Canvas
        {
            Width = cellSize,
            Height = cellSize,
            Clip = new RectangleGeometry { Rect = new Rect(0, 0, cellSize, cellSize) },
            RenderTransformOrigin = new Point(0.5, 0.5),
            RenderTransform = facing,
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
                        FontSize = 5.5,
                        FontWeight = Microsoft.UI.Text.FontWeights.SemiBold,
                        Foreground = new SolidColorBrush(ColorHelper.FromArgb(255, 244, 224, 161))
                    },
                    activity
                }
            }
        };
        Canvas.SetLeft(nameplate, 6);
        Canvas.SetTop(nameplate, 6);

        var scene = new Canvas
        {
            Width = SceneWidth,
            Height = SceneHeight,
            Children = { background, waterViewport, shadow, creatureViewport, foreground, nameplate }
        };
        Content = new Grid
        {
            Background = new SolidColorBrush(ColorHelper.FromArgb(255, 25, 42, 32)),
            Children = { new Viewbox { Child = scene, Stretch = Stretch.Uniform } }
        };

        var area = DisplayArea.GetFromWindowId(AppWindow.Id, DisplayAreaFallback.Primary).WorkArea;
        AppWindow.MoveAndResize(new RectInt32(
            area.X + area.Width / 12, area.Y + area.Height / 12,
            area.Width * 5 / 6, area.Height * 5 / 6));

        activity.Text = $"{starterName} · Caminhando";
        PlaceCreature(Trail[0].Position, 0);
        timer = DispatcherQueue.CreateTimer();
        timer.Interval = TimeSpan.FromMilliseconds(40);
        timer.Tick += Walk;
        Closed += (_, _) => timer.Stop();
        previousTick = waterStart = Stopwatch.GetTimestamp();
        timer.Start();
    }

    private void Walk(DispatcherQueueTimer sender, object args)
    {
        long now = Stopwatch.GetTimestamp();
        double elapsed = Math.Min(Stopwatch.GetElapsedTime(previousTick, now).TotalSeconds, 0.12);
        previousTick = now;
        if (AppWindow.Presenter is OverlappedPresenter { State: OverlappedPresenterState.Minimized })
            return;

        int nextWaterFrame = ViridianWater.FrameAt(Stopwatch.GetElapsedTime(waterStart, now));
        if (nextWaterFrame != waterFrame)
        {
            waterFrame = nextWaterFrame;
            Canvas.SetLeft(water, -(waterFrame % ViridianWater.Columns) * ViridianWater.Width);
            Canvas.SetTop(water, -(waterFrame / ViridianWater.Columns) * ViridianWater.Height);
        }

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

        int next = (waypoint + 1) % Trail.Length;
        Point start = Trail[waypoint].Position;
        var (end, pause) = Trail[next];
        double dx = end.X - start.X;
        double dy = end.Y - start.Y;
        double length = Math.Sqrt(dx * dx + dy * dy);
        double advance = Math.Min(elapsed * 13, length - distance);
        distance += advance;
        strideDistance += advance;
        stepTime += elapsed;

        facing.ScaleX = dx > 0 ? -1 : 1;
        int walkingFrame = 0;
        if (animated)
        {
            walkingFrame = CharmanderAnimation.WalkFrame(dx, dy, strideDistance);
            ShowFrame(walkingFrame);
        }

        if (distance < length)
        {
            double fraction = distance / length;
            var position = new Point(start.X + dx * fraction, start.Y + dy * fraction);
            PlaceCreature(position, animated ? 0 : Math.Abs(Math.Sin(stepTime * 10)));
            return;
        }

        waypoint = next;
        distance = 0;
        PlaceCreature(end, 0);
        if (pause is not null)
        {
            activity.Text = $"{starterName} · {pause}";
            if (animated && pause == GrassRest)
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
    }

    private static Image LoadHabitatImage(string fileName, int width, int height) => new()
    {
        Source = new BitmapImage(new Uri($"ms-appx:///Assets/Habitats/{fileName}")),
        Width = width,
        Height = height,
        Stretch = Stretch.Fill
    };

    private void ShowFrame(int frame)
    {
        int cellSize = CharmanderAnimation.CellSize;
        Canvas.SetLeft(creature, -(frame % CharmanderAnimation.Columns) * cellSize);
        Canvas.SetTop(creature, -(frame / CharmanderAnimation.Columns) * cellSize);
    }

    private void PlaceCreature(Point feet, double bounce)
    {
        Canvas.SetLeft(shadow, Math.Round(feet.X - shadow.Width / 2));
        Canvas.SetTop(shadow, Math.Round(feet.Y - shadow.Height / 2));
        Canvas.SetLeft(creatureViewport, Math.Round(feet.X - creatureViewport.Width / 2));
        Canvas.SetTop(creatureViewport, Math.Round(feet.Y - creatureViewport.Height + 4 - bounce));
    }
}
