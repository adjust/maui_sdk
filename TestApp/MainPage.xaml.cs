using System.Diagnostics;
using AdjustSdk;

namespace TestApp;

public partial class MainPage : ContentPage
{
    int count = 0;

    public MainPage()
    {
        InitializeComponent();
    }

    private void OnCounterClicked(object sender, EventArgs e)
    {
        Trace.WriteLine("OnCounterClicked");

        var testLibrary = new TestLibraryBridge();
        //testLibrary.AddTest("Test_MeasurementConsent_second_start_no_new_session");
        //testLibrary.AddTestDirectory("deeplink");
        testLibrary.Start();

        count++;

        if (count == 1)
            CounterBtn.Text = $"Clicked {count} time";
        else
            CounterBtn.Text = $"Clicked {count} times";

        SemanticScreenReader.Announce(CounterBtn.Text);
    }
}
