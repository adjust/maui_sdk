using System;
using AdjustSdk;
using Foundation;

public partial class TestLibraryBridge
{
    // simulator
    // private const string baseIp = "127.0.0.1";
    // device
    private const string baseIp = "192.168.86.227";

    private TestLibrary.iOSBinding.ATLTestLibrary testLibrary { get; init; }

    public TestLibraryBridge()
    {
        overwriteUrl = $"http://{baseIp}:8080";
        controlUrl = $"ws://{baseIp}:1987";

        testLibrary = TestLibrary.iOSBinding.ATLTestLibrary.TestLibraryWithBaseUrl(
            overwriteUrl, controlUrl, new CommandDelegate(this));
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
        if (infoToSend is null)
        {
            return;
        }

        foreach (KeyValuePair<string, string> keyValuePair in infoToSend)
        {
            AddInfoToSend(keyValuePair.Key, keyValuePair.Value);
        }
    }

    private partial void SendInfoToServer(string? extraPath)
    {
        testLibrary.SendInfoToServer(extraPath);
    }

    private void TrackAppStoreSubscription(Dictionary<string, List<string>> parameters)
    {
        if (!(FirstStringValue(parameters, "revenue") is string price
            && FirstStringValue(parameters, "currency") is string currency
            && FirstStringValue(parameters, "transactionId") is string transactionId))
        {
            return;
        }

        AdjustAppStoreSubscription adjustAppStoreSubscription = new (price, currency, transactionId);

        if (FirstStringValue(parameters, "transactionDate") is string transactionDate)
        {
            adjustAppStoreSubscription.TransactionDate = transactionDate;
        }

        if (FirstStringValue(parameters, "salesRegion") is string salesRegion)
        {
            adjustAppStoreSubscription.SalesRegion = salesRegion;
        }

        IterateTwoPairList(ListValues(parameters, "callbackParams"),
            adjustAppStoreSubscription.AddCallbackParameter);

        IterateTwoPairList(ListValues(parameters, "partnerParams"),
            adjustAppStoreSubscription.AddPartnerParameter);

        Adjust.TrackAppStoreSubscription(adjustAppStoreSubscription);
    }

    private void VerifyAppStorePurchase(Dictionary<string, List<string>> parameters)
    {
        if (!(FirstStringValue(parameters, "productId") is string productId
            && FirstStringValue(parameters, "transactionId") is string transactionId))
        {
            return;
        }

        string? localBasePath = currentExtraPath;
        Adjust.VerifyAppStorePurchase(new(transactionId, productId),
            VerificationResultCallback(localBasePath));
    }

    private static string? JsonResponseConvert(NSDictionary? jsonResponse)
    {
        if (jsonResponse is null)
        {
            return null;
        }

        return NSJsonSerialization.Serialize(jsonResponse, 0, out NSError nsError) switch
        {
            NSData jsonResponseData when jsonResponseData.Length > 0 =>
                new NSString(jsonResponseData, NSStringEncoding.UTF8).ToString(),
            _ => null
        };
    }
}

internal class CommandDelegate(TestLibraryBridge testLibraryBridge) :
    TestLibrary.iOSBinding.AdjustCommandDelegate
{
    /*
        public override void ExecuteCommand(string className, string methodName, NSDictionary parameters) {}
    */
    public override void ExecuteCommand(string className, string methodName, string jsonParameters)
    {
        testLibraryBridge.ExecuteCommon(className, methodName, jsonParameters);
    }
    /*
        public override void ExecuteCommandRawJson(string json) {}
    */
}