namespace testApp;

using System.Diagnostics;
using AdjustSdk;

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

		//Adjust.ping();
		//Adjust.commonPing();

		var testLibrary = new TestLibraryBridge();

		//testLibrary.addTest("Test_AttributionCallback_reattribution");

		//testLibrary.addTest("Test_MeasurementConsent_second_start_no_new_session");
		//testLibrary.addTestDirectory("deeplink");
		
		testLibrary.start();

		count++;

		if (count == 1)
			CounterBtn.Text = $"Clicked {count} time";
		else
			CounterBtn.Text = $"Clicked {count} times";

		SemanticScreenReader.Announce(CounterBtn.Text);
	}
}

