using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Media.Imaging;

namespace TaskbarHabitat.Widget;

internal interface ISpriteProvider
{
    ImageSource GetSprite(string speciesName);
    ImageSource? GetCharmanderAnimation() => null;
}

internal sealed class PrototypeSpriteProvider : ISpriteProvider
{
    public ImageSource GetSprite(string speciesName)
    {
        return new BitmapImage(new Uri($"ms-appx:///Assets/Sprites/{speciesName.ToLowerInvariant()}.png"));
    }

    public ImageSource GetCharmanderAnimation() =>
        new BitmapImage(new Uri("ms-appx:///Assets/Sprites/charmander-habitat.png"));
}
