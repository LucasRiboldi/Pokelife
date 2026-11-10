using Deskband11Lib.WinUI;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Automation;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Media.Imaging;

namespace TaskbarHabitat.Widget;

internal sealed class MainWindow : Window
{
    public TaskbarContentHost Host { get; }

    public MainWindow(string starterName, ISpriteProvider sprites, Action openHabitat)
    {
        Title = "Taskbar Habitat";

        var exit = new MenuFlyoutItem { Text = "Fechar widget" };
        exit.Click += (_, _) => Close();
        var open = new MenuFlyoutItem { Text = "Abrir habitat" };
        open.Click += (_, _) => openHabitat();
        var menu = new MenuFlyout { Items = { open, exit } };

        var button = new Button
        {
            Padding = new Thickness(0, 0, 6, 0),
            HorizontalAlignment = HorizontalAlignment.Center,
            VerticalAlignment = VerticalAlignment.Center,
            Flyout = menu,
            Content = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                Spacing = 4,
                Children =
                {
                    new Image { Source = sprites.GetSprite(starterName), Width = 44, Height = 44 },
                    new TextBlock
                    {
                        Text = starterName,
                        FontWeight = Microsoft.UI.Text.FontWeights.SemiBold,
                        VerticalAlignment = VerticalAlignment.Center
                    }
                }
            }
        };
        AutomationProperties.SetName(button, starterName);
        ToolTipService.SetToolTip(button, "Floresta de Viridian");

        var forest = new Image
        {
            Source = new SvgImageSource(new Uri("ms-appx:///Assets/Habitats/viridian-forest.svg")),
            Stretch = Stretch.Fill,
            IsHitTestVisible = false
        };
        var root = new Grid { Children = { forest, button } };
        Content = root;
        Host = new TaskbarContentHost(this, root, new()
        {
            PreferredWidth = 360,
            PreferredHeight = 48
        });
        Closed += (_, _) => Host.Dispose();
    }
}
