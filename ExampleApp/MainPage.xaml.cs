namespace ExampleApp;

using AdjustSdk;
#if ANDROID
    //using AdjustOaid;
#endif
public partial class MainPage : ContentPage
{
	int count = 0;

	public MainPage()
	{
		InitializeComponent();

		var adjustConfig = new AdjustConfig("2fm9gkqubvpc", AdjustEnvironment.Sandbox);
		adjustConfig.LogLevel = AdjustLogLevel.VERBOSE;
		Adjust.InitSdk(adjustConfig);
	}

	private void OnCounterClicked(object sender, EventArgs e)
	{
#if ANDROID
		//AdjustOaid.readOaid();
		//return;
#endif
		var adjustEvent = new AdjustEvent("g3mfiw");
		Adjust.TrackEvent(adjustEvent);

		count++;

		if (count == 1)
			CounterBtn.Text = $"Clicked {count} time";
		else
			CounterBtn.Text = $"Clicked {count} times";

		SemanticScreenReader.Announce(CounterBtn.Text);
	}
}

