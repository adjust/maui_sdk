using AdjustSdk;

public partial class TestLibraryBridge
{
    // emulator
    private const string baseIp = "10.0.2.2";
    // device
    // private const string baseIp = "192.168.86.211";
    //private const string baseIp = "127.0.0.1";
    private Com.Adjust.Test.TestLibrary testLibrary { get; init; }
    // Must keep a strong reference to prevent GC from collecting the listener
    // while native code still holds a reference to it
    private CommandJsonListener commandJsonListener { get; init; }

    public TestLibraryBridge()
    {
        overwriteUrl = $"https://{baseIp}:8443";
        controlUrl = $"ws://{baseIp}:1987";

        commandJsonListener = new CommandJsonListener(this);
        testLibrary = new Com.Adjust.Test.TestLibrary(
            overwriteUrl, controlUrl, Android.App.Application.Context,
            commandJsonListener);
    }

    public partial void Start()
    {
        Adjust.GetSdkVersion(testLibrary.StartTestSession);
    }

    public partial void AddTest(string testName)
    {
        testLibrary.AddTest(testName);
    }

    public partial void AddTestDirectory(string testDirectory)
    {
        testLibrary.AddTestDirectory(testDirectory);
    }

    private partial void AddInfoToSend(string key, string? value)
    {
        if (value is not null)
        {
            testLibrary.AddInfoToSend(key, value);
        }
    }

    private partial void SetInfoToServer(IDictionary<string, string>? infoToSend)
    {
        testLibrary.SetInfoToSend(infoToSend);
    }

    private partial void SendInfoToServer(string? extraPath)
    {
        testLibrary.SendInfoToServer(extraPath);
    }

    private void TrackPlayStoreSubscription(Dictionary<string, List<string>> parameters)
    {
        if (!(FirstLongValue(parameters, "revenue") is long price
            && FirstStringValue(parameters, "currency") is string currency
            && FirstStringValue(parameters, "productId") is string productId
            && FirstStringValue(parameters, "receipt") is string signature
            && FirstStringValue(parameters, "purchaseToken") is string purchaseToken
            && FirstStringValue(parameters, "transactionId") is string orderId))
        {
            return;
        }

        AdjustPlayStoreSubscription adjustPlayStoreSubscription = new(
            price, currency, productId, orderId, signature, purchaseToken);

        if (FirstLongValue(parameters, "transactionDate") is long purchaseTime)
        {
            adjustPlayStoreSubscription.PurchaseTime = purchaseTime;
        }

        IterateTwoPairList(ListValues(parameters, "callbackParams"),
            adjustPlayStoreSubscription.AddCallbackParameter);

        IterateTwoPairList(ListValues(parameters, "partnerParams"),
            adjustPlayStoreSubscription.AddPartnerParameter);

        Adjust.TrackPlayStoreSubscription(adjustPlayStoreSubscription);
    }

    private void VerifyPlayStorePurchase(Dictionary<string, List<string>> parameters)
    {
        if (!(FirstStringValue(parameters, "productId") is string productId
            && FirstStringValue(parameters, "purchaseToken") is string purchaseToken))
        {
            return;
        }

        string? localBasePath = currentExtraPath;
        Adjust.VerifyPlayStorePurchase(new(productId, purchaseToken),
            VerificationResultCallback(localBasePath));
    }

    private static string? JsonResponseConvert(Org.Json.JSONObject? jsonResponse)
    {
        return jsonResponse?.ToString();
    }

#region Commands
    private partial void PlayStoreKidsComplianceInDelay(Dictionary<string, List<string>> parameters)
    {
        if (FirstBoolValue(parameters, "isEnabled") is true)
        {
            Adjust.EnablePlayStoreKidsComplianceInDelay();
        }

        if (FirstBoolValue(parameters, "isEnabled") is false)
        {
            Adjust.DisablePlayStoreKidsComplianceInDelay();
        }
    }

    private partial void AmazonAdIdGetter(Dictionary<string, List<string>> parameters)
    {
        string? testCallbackId = FirstStringValue(parameters, "testCallbackId");
        Adjust.GetAmazonAdId(amazonAdId =>
        {
            AddInfoToSend("fire_adid", amazonAdId);
            AddInfoToSend("test_callback_id", testCallbackId);
            testLibrary.SendInfoToServer(currentExtraPath);
        });
    }

    private partial void GoogleAdIdGetter(Dictionary<string, List<string>> parameters)
    {
        string? testCallbackId = FirstStringValue(parameters, "testCallbackId");
        Adjust.GetGoogleAdId(googleAdId =>
        {
            testLibrary.AddInfoToSend("gps_adid", googleAdId);
            AddInfoToSend("test_callback_id", testCallbackId);
            testLibrary.SendInfoToServer(currentExtraPath);
        });
    }
#endregion Commands
}

internal class CommandJsonListener(TestLibraryBridge testLibraryBridge) :
    Java.Lang.Object, Com.Adjust.Test.ICommandJsonListener
{
    public void ExecuteCommand(string? className, string? methodName, string? jsonParameters)
    {
        if (className is null || methodName is null || jsonParameters is null)
        {
            return;
        }

        testLibraryBridge.ExecuteCommon(className, methodName, jsonParameters);
    }
}
