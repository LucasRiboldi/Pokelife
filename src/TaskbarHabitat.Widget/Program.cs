using Microsoft.UI.Dispatching;
using Microsoft.UI.Xaml;
using Microsoft.Windows.AppLifecycle;

namespace TaskbarHabitat.Widget;

internal static class Program
{
    [STAThread]
    private static void Main()
    {
        WinRT.ComWrappersSupport.InitializeComWrappers();
        var instance = AppInstance.FindOrRegisterForKey("PokeLife");
        if (!instance.IsCurrent)
        {
            var activation = AppInstance.GetCurrent().GetActivatedEventArgs();
            // Run redirection off the STA before it has a dispatcher to pump COM calls.
            Task.Run(async () => await instance.RedirectActivationToAsync(activation)).GetAwaiter().GetResult();
            return;
        }

        Application.Start(_ =>
        {
            var context = new DispatcherQueueSynchronizationContext(DispatcherQueue.GetForCurrentThread());
            SynchronizationContext.SetSynchronizationContext(context);
            new App();
        });
    }
}
