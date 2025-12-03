namespace VStudioTestAndroid;

//using Adjust

[Activity(Label = "@string/app_name", MainLauncher = true)]
public class MainActivity : Activity
{
    protected override void OnCreate(Bundle? savedInstanceState)
    {
        base.OnCreate(savedInstanceState);

        // Set our view from the "main" layout resource
        SetContentView(Resource.Layout.activity_main);

        var testLibrary = new TestLibraryBridge();
        //testLibrary.AddTest("Test_VerifyTrack_no_json_multiple_requests");
        //testLibrary.AddTest("Test_AttributionGetter_before_install");

        //testLibrary.AddTestDirectory("attribution-getter");
        testLibrary.Start();

    }
}
