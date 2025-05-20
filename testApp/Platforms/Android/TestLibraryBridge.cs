using AdjustSdk;

public partial class TestLibraryBridge
{
    // emulator
    // private const string baseIp = "10.0.2.2";
    // device
    private const string baseIp = "192.168.86.227";
    private Com.Adjust.Test.TestLibrary testLibrary { get; init; }

    public TestLibraryBridge()
    {
        overwriteUrl = $"https://{baseIp}:8443";
        controlUrl = $"ws://{baseIp}:1987";

        testLibrary = new Com.Adjust.Test.TestLibrary(
            overwriteUrl, controlUrl, Platform.AppContext,
            new CommandJsonListener(this));
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

    private partial void AddInfoToSend(string key, string value)
    {
        testLibrary.AddInfoToSend(key, value);
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

        AdjustPlayStoreSubscription adjustPlayStoreSubscription = new (
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
        Adjust.VerifyPlayStorePurchase(new (productId, purchaseToken),
            VerificationResultCallback(localBasePath));
    }

    private static string? JsonResponseConvert(Org.Json.JSONObject? jsonResponse)
    {
        return jsonResponse?.ToString();
    }
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
