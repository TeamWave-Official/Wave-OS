using Microsoft.UI.Xaml;

namespace WaveBash
{
    public partial class App : Application
    {
        protected override void OnLaunched(LaunchActivatedEventArgs args)
        {
            MainWindow window = new MainWindow();
            window.Activate();
        }
    }
}
