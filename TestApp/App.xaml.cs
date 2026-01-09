namespace TestApp;

public partial class App : Application
{
	public App()
	{
		InitializeComponent();
	}

	protected override Window CreateWindow(IActivationState? activationState)
	{
		// Use NavigationPage instead of Shell to avoid layout loops during startup
		var navPage = new NavigationPage(new MainPage())
		{
			Title = "TestApp"
		};
		return new Window(navPage);
	}
}
