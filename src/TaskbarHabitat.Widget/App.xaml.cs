using System.Diagnostics;
using Deskband11Lib.WinUI;
using Microsoft.Data.Sqlite;
using Microsoft.UI.Windowing;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using TaskbarHabitat.Data;
using Windows.Graphics;

namespace TaskbarHabitat.Widget;

public partial class App : Application
{
    private readonly string saveDirectory = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "TaskbarHabitat");
    private readonly ISpriteProvider sprites = new PrototypeSpriteProvider();
    private Window? window;
    private HabitatWindow? desktopHabitat;

    public App()
    {
        InitializeComponent();
    }

    protected override async void OnLaunched(LaunchActivatedEventArgs args)
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
        await ShowTaskbarAsync(starterName);
    }

    private async void ChooseStarter(StarterSelectionWindow selection, int starterId)
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
        if (selection.IsWindowAlive())
            selection.Close();
        await ShowTaskbarAsync(starterName);
    }

    private void ShowDesktopHabitat(string starterName)
    {
        if (desktopHabitat is null)
        {
            desktopHabitat = new HabitatWindow(starterName, sprites);
            desktopHabitat.Closed += (_, _) => desktopHabitat = null;
        }

        if (desktopHabitat.AppWindow.Presenter is OverlappedPresenter { State: OverlappedPresenterState.Minimized } presenter)
            presenter.Restore();
        desktopHabitat.Activate();
    }

    private async Task ShowTaskbarAsync(string starterName)
    {
        MainWindow? habitat = null;
        try
        {
            habitat = new MainWindow(starterName, sprites, () => ShowDesktopHabitat(starterName));
            window = habitat;
            await habitat.Host.AttachWhenLayoutReadyAsync().WaitAsync(TimeSpan.FromSeconds(15));
            habitat.Host.TaskbarWindowRecreationRequired += async (_, _) =>
            {
                if (!ReferenceEquals(window, habitat))
                    return;

                habitat.Host.Dispose();
                await ShowTaskbarAsync(starterName);
                if (habitat.IsWindowAlive())
                    habitat.Close();
            };
            habitat.Activate();
        }
        catch (Exception error) when (error is InvalidOperationException or TimeoutException)
        {
            Trace.TraceError(error.ToString());
            if (desktopHabitat is null)
                ShowStatus("Barra de tarefas indisponível", $"Pokémon inicial: {starterName}");
            if (habitat?.IsWindowAlive() == true)
                habitat.Close();
        }
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
