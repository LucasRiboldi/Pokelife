using System.Text.Json;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Media.Imaging;
using Windows.Foundation;

namespace TaskbarHabitat.Widget;

internal sealed class ViridianScenery
{
    public const string AssetFolder = "ViridianAmpliada";
    private sealed record Layout(Placement[] Objects);

    private sealed record Placement(string File, int X, int Y, int Width, int Height,
        int Depth, int Frames, int Phase, int FrameMs);

    private sealed class AnimatedPiece(TranslateTransform offset, Placement placement)
    {
        private int previousFrame = -1;

        public void Animate(long elapsedMs)
        {
            int frame = (int)((elapsedMs / placement.FrameMs + placement.Phase) % placement.Frames);
            if (frame == previousFrame)
                return;

            previousFrame = frame;
            offset.X = -frame * placement.Width;
        }
    }

    private readonly List<AnimatedPiece> animatedPieces = [];

    public static string AssetPath(string file) =>
        Path.Combine(AppContext.BaseDirectory, "Assets", "Habitats", AssetFolder, file);

    public ViridianScenery(Canvas scene)
    {
        string manifest = AssetPath("layout.json");
        var layout = JsonSerializer.Deserialize<Layout>(File.ReadAllText(manifest), JsonSerializerOptions.Web)
            ?? throw new InvalidDataException("O cenário de Viridian precisa de um catálogo de objetos.");
        var textures = new Dictionary<string, BitmapImage>();

        foreach (var placement in layout.Objects)
        {
            if (!textures.TryGetValue(placement.File, out var texture))
            {
                texture = new BitmapImage(new Uri($"ms-appx:///Assets/Habitats/{placement.File}"));
                textures.Add(placement.File, texture);
            }

            var image = new Image
            {
                Source = texture,
                Width = placement.Width * placement.Frames,
                Height = placement.Height,
                Stretch = Stretch.Fill
            };
            UIElement piece = image;
            if (placement.Frames > 1)
            {
                var offset = new TranslateTransform();
                image.RenderTransform = offset;
                piece = new Canvas
                {
                    Width = placement.Width,
                    Height = placement.Height,
                    Clip = new RectangleGeometry { Rect = new Rect(0, 0, placement.Width, placement.Height) },
                    Children = { image }
                };
                animatedPieces.Add(new AnimatedPiece(offset, placement));
            }

            Canvas.SetLeft(piece, placement.X);
            Canvas.SetTop(piece, placement.Y);
            Canvas.SetZIndex(piece, placement.Depth);
            scene.Children.Add(piece);
        }

        Animate(TimeSpan.Zero);
    }

    public void Animate(TimeSpan elapsed)
    {
        long elapsedMs = elapsed.Ticks / TimeSpan.TicksPerMillisecond;
        foreach (var piece in animatedPieces)
            piece.Animate(elapsedMs);
    }
}
