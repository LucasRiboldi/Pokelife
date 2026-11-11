using System.Diagnostics;
using Microsoft.Data.Sqlite;
using Microsoft.UI.Dispatching;
using Microsoft.UI.Windowing;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.Windows.AppLifecycle;
using TaskbarHabitat.Data;
using Windows.Graphics;

namespace TaskbarHabitat.Widget;

public partial class App : Application
{
    private readonly string saveDirectory = Environment.GetEnvironmentVariable("POKELIFE_SAVE_DIRECTORY")
        ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "TaskbarHabitat");
    private readonly ISpriteProvider sprites = new PrototypeSpriteProvider();
    private Window? window;

    public App()
    {
        InitializeComponent();
        var dispatcher = DispatcherQueue.GetForCurrentThread();
        AppInstance.GetCurrent().Activated += (_, _) => dispatcher.TryEnqueue(RestoreWindow);
    }

    protected override void OnLaunched(LaunchActivatedEventArgs args)
    {
        string? starterName;
        try
        {
            Directory.CreateDirectory(saveDirectory);
            using var connection = OpenSave();
            Database.Initialize(connection);
            starterName = new SaveService(connection).GetSavedStarterName();
        }
        catch (Exception error) when (IsSaveError(error))
        {
            Trace.TraceError(error.ToString());
            ShowStatus("Não foi possível abrir o save", "Feche a janela e tente abrir o jogo novamente.");
            return;
        }

        if (starterName is null)
        {
            var selection = new StarterSelectionWindow();
            selection.StarterChosen += starterId => ChooseStarter(selection, starterId);
            ShowWindow(selection);
            return;
        }

        ShowDesktopHabitat(starterName);
    }

    private void ChooseStarter(StarterSelectionWindow selection, int starterId)
    {
        var controls = (Control)selection.Content;
        controls.IsEnabled = false;
        string starterName;
        try
        {
            using var connection = OpenSave();
            var service = new SaveService(connection);
            string? savedName = service.GetSavedStarterName();
            if (savedName is null)
            {
                service.CreateNewSave(starterId);
                savedName = service.GetSavedStarterName();
            }
            starterName = savedName ?? throw new InvalidOperationException("The saved starter could not be read.");
        }
        catch (Exception error) when (IsSaveError(error))
        {
            Trace.TraceError(error.ToString());
            selection.ShowSaveError();
            controls.IsEnabled = true;
            return;
        }

        ShowDesktopHabitat(starterName);
        selection.Close();
    }

    private void ShowDesktopHabitat(string starterName)
    {
        window = new HabitatWindow(starterName, sprites);
        window.Activate();
    }

    private void RestoreWindow()
    {
        if (window?.AppWindow.Presenter is OverlappedPresenter { State: OverlappedPresenterState.Minimized } presenter)
            presenter.Restore();
        window?.Activate();
    }

    private SqliteConnection OpenSave()
    {
        var connectionString = new SqliteConnectionStringBuilder
        {
            DataSource = Path.Combine(saveDirectory, "save.db"),
            ForeignKeys = true
        };
        var connection = new SqliteConnection(connectionString.ToString());
        try
        {
            connection.Open();
            return connection;
        }
        catch
        {
            connection.Dispose();
            throw;
        }
    }

    private void ShowStatus(string heading, string message)
    {
        ShowWindow(new Window
        {
            Title = "Taskbar Habitat",
            Content = new StackPanel
            {
                Padding = new Thickness(24),
                Spacing = 12,
                Children =
                {
                    new TextBlock { Text = heading, FontSize = 24, TextWrapping = TextWrapping.Wrap },
                    new TextBlock { Text = message, TextWrapping = TextWrapping.Wrap }
                }
            }
        });
    }

    private void ShowWindow(Window next)
    {
        window = next;
        double scale = next.Content.XamlRoot?.RasterizationScale ?? 1;
        next.AppWindow.ResizeClient(new SizeInt32((int)(440 * scale), (int)(310 * scale)));
        next.Activate();
    }

    private static bool IsSaveError(Exception error) =>
        error is SqliteException or IOException or UnauthorizedAccessException or InvalidOperationException;
}
