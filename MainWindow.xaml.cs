using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Hosting;
using Microsoft.UI.Xaml.Media;
using System;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;

namespace WaveBash
{
    public sealed partial class MainWindow : Window
    {
        public MainWindow()
        {
            this.InitializeComponent();

            // Resize + rounded corners
            this.AppWindow.Resize(new Windows.Graphics.SizeInt32(900, 550));
            this.SystemBackdrop = new MicaBackdrop();

            // Fade + slide in animation
            var compositor = ElementCompositionPreview.GetElementVisual(this.Content).Compositor;
            var visual = ElementCompositionPreview.GetElementVisual(this.Content);

            var fadeAnim = compositor.CreateScalarKeyFrameAnimation();
            fadeAnim.InsertKeyFrame(1f, 1f);
            fadeAnim.Duration = TimeSpan.FromMilliseconds(800);

            var offsetAnim = compositor.CreateVector3KeyFrameAnimation();
            offsetAnim.InsertKeyFrame(0f, new System.Numerics.Vector3(0, 40, 0));
            offsetAnim.InsertKeyFrame(1f, new System.Numerics.Vector3(0, 0, 0));
            offsetAnim.Duration = TimeSpan.FromMilliseconds(800);

            visual.Opacity = 0f;
            visual.StartAnimation("Opacity", fadeAnim);
            visual.StartAnimation("Offset", offsetAnim);
        }

        private void RunCommand_Click(object sender, RoutedEventArgs e)
        {
            string command = CommandBox.Text;
            if (string.IsNullOrWhiteSpace(command))
                return;

            AppendWithTyping($"\nWave@OS:~$ {command}");
            RunCommand(command);
            CommandBox.Text = "";
        }

        private async void AppendWithTyping(string text)
        {
            foreach (char c in text)
            {
                OutputBox.Text += c;
                await Task.Delay(3); // typing speed (faster but smooth)
            }
            OutputBox.Text += "\n";
        }

        private void RunCommand(string command)
        {
            try
            {
                var psi = new ProcessStartInfo("cmd.exe", "/c " + command)
                {
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8
                };

                var process = Process.Start(psi);
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (!string.IsNullOrEmpty(output))
                    AppendWithTyping(output);
                if (!string.IsNullOrEmpty(error))
                    AppendWithTyping("[Error]: " + error);
            }
            catch (Exception ex)
            {
                AppendWithTyping("[Exception]: " + ex.Message);
            }
        }
    }
}
