using System.Globalization;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace TaskbarHabitat.Widget;

public sealed partial class StarterSelectionWindow : Window
{
    public event Action<int>? StarterChosen;

    public StarterSelectionWindow()
    {
        InitializeComponent();
    }

    public void ShowSaveError() => SaveError.IsOpen = true;

    private void ChooseStarter(object sender, RoutedEventArgs args)
    {
        var button = (Button)sender;
        StarterChosen?.Invoke(int.Parse((string)button.Tag, CultureInfo.InvariantCulture));
    }
}
