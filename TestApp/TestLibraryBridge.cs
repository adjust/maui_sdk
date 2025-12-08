using System.Text.Json;
using AdjustSdk;
#if IOS
using UIKit;
using Foundation;
#endif

public partial class TestLibraryBridge
{
    private string? currentExtraPath;

    private string overwriteUrl { get ; init; }
    private string controlUrl { get ; init; }

    public partial void Start();
    public partial void AddTest(string testName);
    public partial void AddTestDirectory(string testDirectory);
    private partial void AddInfoToSend(string key, string value);
    private partial void SetInfoToServer(IDictionary<string, string>? infoToSend);
    private partial void SendInfoToServer(string? extraPath);
    #if ANDROID
    private partial void PlayStoreKidsComplianceInDelay(Dictionary<string, List<string>> parameters);
    #elif IOS
    private partial void IdfaGetter(Dictionary<string, List<string>> parameters);
    private partial void IdfvGetter(Dictionary<string, List<string>> parameters);
    #endif

#region Commands
    internal void ExecuteCommon(string className, string methodName, string jsonParameters)
    {
        var parameters = 
            JsonSerializer.Deserialize<Dictionary<string, List<string>>>(jsonParameters);

        if (parameters is null)
        {
            return;
        }

        switch (methodName)
        {
            case "testOptions": TestOptions(parameters); break;
            case "config": ConfigNative(parameters); break;
            case "start": Start(parameters); break;
            case "event": EventNative(parameters); break;
            case "trackEvent": TrackEvent(parameters); break;
            case "resume": Resume(parameters); break;
            case "pause": Pause(parameters); break;
            case "setEnabled": SetEnabled(parameters); break;
            case "setOfflineMode": SetOfflineMode(parameters); break;
            case "addGlobalCallbackParameter": AddGlobalCallbackParameter(parameters); break;
            case "addGlobalPartnerParameter": AddGlobalPartnerParameter(parameters); break;
            case "removeGlobalCallbackParameter": RemoveGlobalCallbackParameter(parameters); break;
            case "removeGlobalPartnerParameter": RemoveGlobalPartnerParameter(parameters); break;
            case "removeGlobalCallbackParameters": RemoveGlobalCallbackParameters(parameters); break;
            case "removeGlobalPartnerParameters": RemoveGlobalPartnerParameters(parameters); break;
            case "setPushToken": SetPushToken(parameters); break;
            case "openDeeplink": OpenDeeplink(parameters); break;
            case "gdprForgetMe": GdprForgetMe(parameters); break;
            case "trackSubscription": TrackSubscription(parameters); break;
            case "thirdPartySharing": ThirdPartySharing(parameters); break;
            case "measurementConsent": MeasurementConsent(parameters); break;
            case "trackAdRevenue": TrackAdRevenue(parameters); break;
            case "getLastDeeplink": GetLastDeeplink(parameters); break;
            case "verifyPurchase": VerifyPurchase(parameters); break;
            case "processDeeplink": ProcessDeeplink(parameters); break;
            case "attributionGetter": AttributionGetter(parameters); break;
            case "attributionGetterWithTimeout": AttributionGetterWithTimeout(parameters); break;
            case "adidGetter": AdidGetter(parameters); break;
            case "adidGetterWithTimeout": AdidGetterWithTimeout(parameters); break;
            case "verifyTrack": VerifyTrack(parameters); break;
            case "endFirstSessionDelay": EndFirstSessionDelay(parameters); break;
            case "coppaComplianceInDelay": CoppaComplianceInDelay(parameters); break;
            case "externalDeviceIdInDelay": ExternalDeviceIdInDelay(parameters); break;
            #if ANDROID
            case "playStoreKidsComplianceInDelay": PlayStoreKidsComplianceInDelay(parameters); break;
            #elif IOS
            case "idfaGetter": IdfaGetter(parameters); break;
            case "idfvGetter": IdfvGetter(parameters); break;
            #endif
        }
    }

    private void TestOptions(Dictionary<string, List<string>> parameters)
    {
        Dictionary<string, object> testOptions = new()
        {
            {"baseUrl", overwriteUrl},
            {"gdprUrl", overwriteUrl},
            {"subscriptionUrl", overwriteUrl},
            {"purchaseVerificationUrl", overwriteUrl},
            {"testUrlOverwrite", overwriteUrl},
        };

        if (FirstStringValue(parameters, "basePath") is string basePath)
        {
            currentExtraPath = basePath;
        }

        if (FirstLongValue(parameters, "timerInterval") is long timerInterval)
        {
            testOptions.Add("timerIntervalInMilliseconds", timerInterval);
        }

        if (FirstLongValue(parameters, "timerStart") is long timerStart)
        {
            testOptions.Add("timerStartInMilliseconds", timerStart);
        }

        if (FirstLongValue(parameters, "sessionInterval") is long sessionInterval)
        {
            testOptions.Add("sessionIntervalInMilliseconds", sessionInterval);
        }

        if (FirstLongValue(parameters, "subsessionInterval") is long subsessionInterval)
        {
            testOptions.Add("subsessionIntervalInMilliseconds", subsessionInterval);
        }

        if (FirstBoolValue(parameters, "noBackoffWait") is bool noBackoffWait)
        {
            testOptions.Add("noBackoffWait", noBackoffWait);
        }
#if IOS
        // AdServices.framework will not be used in test app by default
        testOptions.Add("adServicesFrameworkEnabled",
            FirstBoolValue(parameters, "adServicesFrameworkEnabled") ?? false);

        if (FirstIntValue(parameters, "attStatus") is int attStatus)
        {
            testOptions.Add("attStatusInt", attStatus);
        }

        if (FirstStringValue(parameters, "idfa") is string idfa)
        {
            testOptions.Add("idfa", idfa);
        }
#endif
        if (FirstBoolValue(parameters, "doNotIgnoreSystemLifecycleBootstrap") is true)
        {
            testOptions.Add("ignoreSystemLifecycleBootstrap", false);
        }
#if ANDROID
        bool useTestConnectionOptions = false;
#endif

        if (ListValues(parameters, "teardown") is List<string> teardownOptions)
        {
            foreach (string teardownOption in teardownOptions)
            {
                if (teardownOption == "resetSdk")
                {
                    testOptions.Add("teardown", true);
                    if (currentExtraPath is not null)
                    {
                        testOptions.Add("extraPath", currentExtraPath);
                    }
#if ANDROID
                    useTestConnectionOptions = true;
#endif
                }
                else if (teardownOption == "deleteState")
                {
                    testOptions.Add("deleteState", true);
                }
                else if (teardownOption == "resetTest")
                {
                    testOptions.Add("timerIntervalInMilliseconds", -1L);
                    testOptions.Add("timerStartInMilliseconds", -1L);
                    testOptions.Add("sessionIntervalInMilliseconds", -1L);
                    testOptions.Add("subsessionIntervalInMilliseconds", -1L);
                }
                else if (teardownOption == "sdk")
                {
                    testOptions.Add("teardown", "true");
                    testOptions.Remove("extraPath");
                }
                else if (teardownOption == "test")
                {
                    testOptions.Add("timerIntervalInMilliseconds", -1L);
                    testOptions.Add("timerStartInMilliseconds", -1L);
                    testOptions.Add("sessionIntervalInMilliseconds", -1L);
                    testOptions.Add("subsessionIntervalInMilliseconds", -1L);
                }
            }
        }

        Adjust.SetTestOptions(testOptions);
#if ANDROID
        if (useTestConnectionOptions)
        {
            Com.Adjust.Test_options.TestConnectionOptions.SetTestConnectionOptions();
        }
#endif
    }

    private AdjustConfig? ConfigNative(Dictionary<string, List<string>> parameters)
    {
        string? appToken = FirstStringValue(parameters, "appToken");
        AdjustEnvironment? environment =
            FirstStringValue(parameters, "environment") switch
        {
            "sandbox" => AdjustEnvironment.Sandbox,
            "production"  => AdjustEnvironment.Production,
            _ => null,
        };

        if (!(appToken is string appTokenValid
            && environment is AdjustEnvironment environmentValid))
        {
            return null;
        }

        #if IOS

        UIPasteboard pasteboard = UIPasteboard.General;
        pasteboard.Url = null;
        if (FirstStringValue(parameters, "pasteboard") is string pasteboardContent)
        {
            pasteboard.Url = new NSUrl(pasteboardContent);
        }

        #endif

        AdjustConfig adjustConfig = new (appTokenValid, environmentValid);

        AdjustLogLevel? adjustLogLevel = FirstStringValue(parameters, "logLevel") switch
        {
            "verbose" => AdjustLogLevel.VERBOSE,
            "debug" => AdjustLogLevel.DEBUG,
            "info" => AdjustLogLevel.INFO,
            "warn" => AdjustLogLevel.WARN,
            "error" => AdjustLogLevel.ERROR,
            "assert" => AdjustLogLevel.ASSERT,
            "suppress" => AdjustLogLevel.SUPPRESS,
            _ => null };
        if (adjustLogLevel is not null)
        {
            adjustConfig.LogLevel = adjustLogLevel;
        }

        // sdk prefix not tested from non-natives

        if (FirstStringValue(parameters, "defaultTracker") is string defaultTracker)
        {
            adjustConfig.DefaultTracker = defaultTracker;
        }

        if (FirstBoolValue(parameters, "needsCost") is true)
        {
            adjustConfig.IsCostDataInAttributionEnabled = true;
        }

        if (FirstBoolValue(parameters, "sendInBackground") is true)
        {
            adjustConfig.IsSendingInBackgroundEnabled = true;
        }

        if (FirstBoolValue(parameters, "firstSessionDelayEnabled") is true)
        {
            adjustConfig.IsFirstSessionDelayEnabled = true;
        }

        if (FirstIntValue(parameters, "eventDeduplicationIdsMaxSize")
            is int eventDeduplicationIdsMaxSize) 
        {
            adjustConfig.EventDeduplicationIdsMaxSize = eventDeduplicationIdsMaxSize;
        }

        if (FirstStringValue(parameters, "externalDeviceId") is string externalDeviceId)
        {
            adjustConfig.ExternalDeviceId = externalDeviceId;
        }

        if (FirstBoolValue(parameters, "coppaCompliant") is true)
        {
            adjustConfig.IsCoppaComplianceEnabled = true;
        }

        if (FirstStringValue(parameters, "storeName") is string storeName)
        {
            AdjustStoreInfo storeInfo = new AdjustStoreInfo(storeName);

            if (FirstStringValue(parameters, "storeAppId") is string storeAppId)
            {
                storeInfo.StoreAppId = storeAppId;
            }

            adjustConfig.StoreInfo = storeInfo;
        }

#if ANDROID
        if (FirstBoolValue(parameters, "playStoreKids") is true)
        {
            adjustConfig.IsPlayStoreKidsComplianceEnabled = true;
        }

        /* not being tested:
            IsPreinstallTrackingEnabled
            PreinstallFilePath
            FbAppId
        */
#elif IOS
        if (FirstBoolValue(parameters, "allowIdfaReading") is false)
        {
            adjustConfig.IsIdfaReadingEnabled = false;
        }

        if (FirstBoolValue(parameters, "allowIdfvReading") is false)
        {
            adjustConfig.IsIdfvReadingEnabled = false;
        }

        if (FirstBoolValue(parameters, "allowAdServicesInfoReading") is false)
        {
            adjustConfig.IsAdServicesEnabled = false;
        }

        if (FirstBoolValue(parameters, "allowSkAdNetworkHandling") is false)
        {
            adjustConfig.IsSkanAttributionEnabled = false;
        }

        if (FirstIntValue(parameters, "attConsentWaitingSeconds") is int attConsentWaitingSeconds)
        {
            adjustConfig.AttConsentWaitingInterval = attConsentWaitingSeconds;
        }

        if (parameters.ContainsKey("skanCallback"))
        {
            string? localBasePath = currentExtraPath;
            adjustConfig.SkanUpdatedDelegate = (Dictionary<string, string> data) =>
            {
                SetInfoToServer(data);
                SendInfoToServer(localBasePath);
            };
        }

        if (FirstBoolValue(parameters, "allowAttUsage") is false)
        {
            adjustConfig.IsAppTrackingTransparencyUsageEnabled = false;
        }

        if (FirstBoolValue(parameters, "checkPasteboard") is true)
        {
            adjustConfig.IsLinkMeEnabled = true;
        }

#endif
        if (parameters.ContainsKey("attributionCallbackSendAll"))
        {
            adjustConfig.AttributionChangedDelegate = attributionCallback(currentExtraPath);
        }

        if (parameters.ContainsKey("sessionCallbackSendSuccess"))
        {
            string? localBasePath = currentExtraPath;
            adjustConfig.SessionSuccessDelegate = (AdjustSessionSuccess adjustSessionSuccess) =>
            {
                Dictionary<string, string> infoToSend = new();

                if (adjustSessionSuccess.Message is not null)
                {
                    infoToSend.Add("message", adjustSessionSuccess.Message);
                }
                if (adjustSessionSuccess.Timestamp is not null)
                {
                    infoToSend.Add("timestamp", adjustSessionSuccess.Timestamp);
                }
                if (adjustSessionSuccess.Adid is not null)
                {
                    infoToSend.Add("adid", adjustSessionSuccess.Adid);
                }
                if (JsonResponseConvert(adjustSessionSuccess.JsonResponse) is string jsonResponse)
                {
                    infoToSend.Add("jsonResponse", jsonResponse);
                }

                SetInfoToServer(infoToSend);
                SendInfoToServer(localBasePath);
            };
        }

        if (parameters.ContainsKey("sessionCallbackSendFailure"))
        {
            string? localBasePath = currentExtraPath;
            adjustConfig.SessionFailureDelegate = (AdjustSessionFailure adjustSessionFailure) =>
            {
                Dictionary<string, string> infoToSend = new();

                if (adjustSessionFailure.Message is not null)
                {
                    infoToSend.Add("message", adjustSessionFailure.Message);
                }
                if (adjustSessionFailure.Timestamp is not null)
                {
                    infoToSend.Add("timestamp", adjustSessionFailure.Timestamp);
                }
                if (adjustSessionFailure.Adid is not null)
                {
                    infoToSend.Add("adid", adjustSessionFailure.Adid);
                }
                infoToSend.Add("willRetry", adjustSessionFailure.WillRetry.ToString().ToLowerInvariant());
                if (JsonResponseConvert(adjustSessionFailure.JsonResponse) is string jsonResponse)
                {
                    infoToSend.Add("jsonResponse", jsonResponse);
                }

                SetInfoToServer(infoToSend);
                SendInfoToServer(localBasePath);
            };
        }

        if (parameters.ContainsKey("eventCallbackSendSuccess"))
        {
            string? localBasePath = currentExtraPath;
            adjustConfig.EventSuccessDelegate = (AdjustEventSuccess adjustEventSuccess) =>
            {
                Dictionary<string, string> infoToSend = new();

                if (adjustEventSuccess.Message is not null)
                {
                    infoToSend.Add("message", adjustEventSuccess.Message);
                }
                if (adjustEventSuccess.Timestamp is not null)
                {
                    infoToSend.Add("timestamp", adjustEventSuccess.Timestamp);
                }
                if (adjustEventSuccess.Adid is not null)
                {
                    infoToSend.Add("adid", adjustEventSuccess.Adid);
                }
                if (adjustEventSuccess.EventToken is not null)
                {
                    infoToSend.Add("eventToken", adjustEventSuccess.EventToken);
                }
                if (adjustEventSuccess.CallbackId is not null)
                {
                    infoToSend.Add("callbackId", adjustEventSuccess.CallbackId);
                }
                if (JsonResponseConvert(adjustEventSuccess.JsonResponse) is string jsonResponse)
                {
                    infoToSend.Add("jsonResponse", jsonResponse);
                }

                SetInfoToServer(infoToSend);
                SendInfoToServer(localBasePath);
            };
        }

        if (parameters.ContainsKey("eventCallbackSendFailure"))
        {
            string? localBasePath = currentExtraPath;
            adjustConfig.EventFailureDelegate = (AdjustEventFailure adjustEventFailure) =>
            {
                Dictionary<string, string> infoToSend = new();

                if (adjustEventFailure.Message is not null)
                {
                    infoToSend.Add("message", adjustEventFailure.Message);
                }
                if (adjustEventFailure.Timestamp is not null)
                {
                    infoToSend.Add("timestamp", adjustEventFailure.Timestamp);
                }
                if (adjustEventFailure.Adid is not null)
                {
                    infoToSend.Add("adid", adjustEventFailure.Adid);
                }
                if (adjustEventFailure.EventToken is not null)
                {
                    infoToSend.Add("eventToken", adjustEventFailure.EventToken);
                }
                if (adjustEventFailure.CallbackId is not null)
                {
                    infoToSend.Add("callbackId", adjustEventFailure.CallbackId);
                }
                infoToSend.Add("willRetry", adjustEventFailure.WillRetry.ToString().ToLowerInvariant());
                if (JsonResponseConvert(adjustEventFailure.JsonResponse) is string jsonResponse)
                {
                    infoToSend.Add("jsonResponse", jsonResponse);
                }

                SetInfoToServer(infoToSend);
                SendInfoToServer(localBasePath);
            };
        }

        if (parameters.ContainsKey("deferredDeeplinkCallback"))
        {
            string? localBasePath = currentExtraPath;
            bool launchDeferredDeeplink = 
                FirstBoolValue(parameters, "deferredDeeplinkCallback") is true;
            adjustConfig.DeferredDeeplinkDelegate = (string deeplink) =>
            {
                AddInfoToSend("deeplink", deeplink);
                SendInfoToServer(localBasePath);
                return launchDeferredDeeplink;
            };
        }

        return adjustConfig;
    }

    private void Start(Dictionary<string, List<string>> parameters)
    {
        if (ConfigNative(parameters) is not AdjustConfig adjustConfig)
        {
            return;
        }

        Adjust.InitSdk(adjustConfig);
    }

    private AdjustEvent EventNative(Dictionary<string, List<string>> parameters)
    {
        string eventToken = FirstStringValue(parameters, "eventToken") ?? "";
        AdjustEvent adjustEvent = new (eventToken);

        if (RevenueCurrencyValues(parameters) is (string currency, double amount))
        {
            adjustEvent.SetRevenue(amount, currency);
        }

        IterateTwoPairList(ListValues(parameters, "callbackParams"),
            adjustEvent.AddCallbackParameter);

        IterateTwoPairList(ListValues(parameters, "partnerParams"),
            adjustEvent.AddPartnerParameter);

        if (FirstStringValue(parameters, "callbackId") is string callbackId)
        {
            adjustEvent.CallbackId = callbackId;
        }

        if (FirstStringValue(parameters, "productId") is string productId)
        {
            adjustEvent.ProductId = productId;
        }

        if (FirstStringValue(parameters, "deduplicationId") is string deduplicationId)
        {
            adjustEvent.DeduplicationId = deduplicationId;
        }
#if ANDROID
        if (FirstStringValue(parameters, "purchaseToken") is string purchaseToken)
        {
            adjustEvent.PurchaseToken = purchaseToken;
        }
#elif IOS
        if (FirstStringValue(parameters, "transactionId") is string transactionId)
        {
            adjustEvent.TransactionId = transactionId;
        }
#endif
        return adjustEvent;
    }

    private void TrackEvent(Dictionary<string, List<string>> parameters)
    {
        Adjust.TrackEvent(EventNative(parameters));
    }

    private void Resume(Dictionary<string, List<string>> parameters)
    {
        Adjust.Resume();
    }

    private void Pause(Dictionary<string, List<string>> parameters)
    {
        Adjust.Pause();
    }

    private void SetEnabled(Dictionary<string, List<string>> parameters)
    {
        if (FirstBoolValue(parameters, "enabled") is true)
        {
            Adjust.Enable();
        }
        else
        {
            Adjust.Disable();
        }
    }

    private void SetOfflineMode(Dictionary<string, List<string>> parameters)
    {
        if (FirstBoolValue(parameters, "enabled") is true)
        {
            Adjust.SwitchToOfflineMode();
        }
        else
        {
            Adjust.SwitchBackToOnlineMode();
        }
    }

    private void AddGlobalCallbackParameter(Dictionary<string, List<string>> parameters)
    {
        IterateTwoPairList(ListValues(parameters, "KeyValue"),
            Adjust.AddGlobalCallbackParameter);
    }

    private void AddGlobalPartnerParameter(Dictionary<string, List<string>> parameters)
    {
        IterateTwoPairList(ListValues(parameters, "KeyValue"),
            Adjust.AddGlobalPartnerParameter);
    }

    private void RemoveGlobalCallbackParameter(Dictionary<string, List<string>> parameters)
    {
        if (ListValues(parameters, "key") is not List<string> keys)
        {
            return;
        }

        foreach (var key in keys)
        {
            Adjust.RemoveGlobalCallbackParameter(key);
        }
    }

    private void RemoveGlobalPartnerParameter(Dictionary<string, List<string>> parameters)
    {
        if (ListValues(parameters, "key") is not List<string> keys)
        {
            return;
        }

        foreach (var key in keys)
        {
            Adjust.RemoveGlobalPartnerParameter(key);
        }
    }

    private void RemoveGlobalCallbackParameters(Dictionary<string, List<string>> parameters)
    {
        Adjust.RemoveGlobalCallbackParameters();
    }

    private void RemoveGlobalPartnerParameters(Dictionary<string, List<string>> parameters)
    {
        Adjust.RemoveGlobalPartnerParameters();
    }

    private void SetPushToken(Dictionary<string, List<string>> parameters)
    {
        if (FirstStringValue(parameters, "pushToken") is string pushToken)
        {
            // TODO try to change test app proj to allow null
            Adjust.SetPushToken(pushToken);
        }
    }

    private void OpenDeeplink(Dictionary<string, List<string>> parameters)
    {
        if (FirstStringValue(parameters, "deeplink") is string deeplink)
        {
            AdjustDeeplink adjustDeeplink = new(deeplink);
            if (FirstStringValue(parameters, "referrer") is string referrer)
            {
                adjustDeeplink.Referrer = referrer;
            }

            Adjust.ProcessDeeplink(adjustDeeplink);
        }
    }

    private void GdprForgetMe(Dictionary<string, List<string>> parameters)
    {
        Adjust.GdprForgetMe();
    }

    private void TrackSubscription(Dictionary<string, List<string>> parameters)
    {
#if ANDROID
        TrackPlayStoreSubscription(parameters);
#elif IOS
        TrackAppStoreSubscription(parameters);
#endif
    }

    private void ThirdPartySharing(Dictionary<string, List<string>> parameters)
    {
        AdjustThirdPartySharing adjustThirdPartySharing =
            new(FirstBoolValue(parameters, "isEnabled"));

        IterateThreePairList(ListValues(parameters, "granularOptions"),
            adjustThirdPartySharing.AddGranularOption);

        IterateThreePairList(ListValues(parameters, "partnerSharingSettings"),
            (string partnerName, string key, string boolStrValue) =>
                adjustThirdPartySharing.AddPartnerSharingSettings(
                    partnerName, key, boolStrValue == "true"));

        Adjust.TrackThirdPartySharing(adjustThirdPartySharing);
    }

    private void MeasurementConsent(Dictionary<string, List<string>> parameters)
    {
        Adjust.TrackMeasurementConsent(FirstBoolValue(parameters, "isEnabled") is true);
    }

    private void TrackAdRevenue(Dictionary<string, List<string>> parameters)
    {
        if (FirstStringValue(parameters, "adRevenueSource") is not string adRevenueSource)
        {
            return;
        }

        AdjustAdRevenue adRevenue = new(adRevenueSource);

        if (RevenueCurrencyValues(parameters) is (string currency, double amount))
        {
            adRevenue.SetRevenue(amount, currency);
        }

        if (FirstIntValue(parameters, "adImpressionsCount") is int adImpressionsCount)
        {
            adRevenue.AdImpressionsCount = adImpressionsCount;
        }

        if (FirstStringValue(parameters, "adRevenueUnit") is string adRevenueUnit)
        {
            adRevenue.AdRevenueUnit = adRevenueUnit;
        }

        if (FirstStringValue(parameters, "adRevenuePlacement") is string adRevenuePlacement)
        {
            adRevenue.AdRevenuePlacement = adRevenuePlacement;
        }

        if (FirstStringValue(parameters, "adRevenueNetwork") is string adRevenueNetwork)
        {
            adRevenue.AdRevenueNetwork = adRevenueNetwork;
        }

        IterateTwoPairList(ListValues(parameters, "callbackParams"),
            adRevenue.AddCallbackParameter);

        IterateTwoPairList(ListValues(parameters, "partnerParams"),
            adRevenue.AddPartnerParameter);

        Adjust.TrackAdRevenue(adRevenue);
    }

    private void GetLastDeeplink(Dictionary<string, List<string>> parameters)
    {
        string? localBasePath = currentExtraPath;
        Adjust.GetLastDeeplink((string? lastDeeplink) =>
        {
            AddInfoToSend("last_deeplink", lastDeeplink ?? "");
            SendInfoToServer(localBasePath);
        });
    }

    private void VerifyPurchase(Dictionary<string, List<string>> parameters)
    {
#if ANDROID
        VerifyPlayStorePurchase(parameters);
#elif IOS
        VerifyAppStorePurchase(parameters);
#endif
    }

    private void ProcessDeeplink(Dictionary<string, List<string>> parameters)
    {
        if (FirstStringValue(parameters, "deeplink") is not string deeplink)
        {
            return;
        }

        string? localBasePath = currentExtraPath;
        Adjust.ProcessAndResolveDeeplink(new AdjustDeeplink(deeplink), (string resolvedLink) =>
        {
            AddInfoToSend("resolved_link", resolvedLink);
            SendInfoToServer(localBasePath);
        });
    }

    private void AttributionGetter(Dictionary<string, List<string>> parameters)
    {
        Adjust.GetAttribution(attributionCallback(currentExtraPath));
    }

    private void AttributionGetterWithTimeout(Dictionary<string, List<string>> parameters)
    {
        Adjust.GetAttributionWithTimeout(FirstLongValue(parameters, "timeout") ?? 0,
            attributionCallbackNullable(currentExtraPath));
    }

    private void AdidGetter(Dictionary<string, List<string>> parameters)
    {
        Adjust.GetAdid(adid =>
        {
            testLibrary.AddInfoToSend("adid", adid);
            testLibrary.SendInfoToServer(currentExtraPath);
        });
    }

    private void AdidGetterWithTimeout(Dictionary<string, List<string>> parameters)
    {
        Adjust.GetAdidWithTimeout(FirstLongValue(parameters, "timeout") ?? 0, adid =>
        {
            if (adid is not null) {
                testLibrary.AddInfoToSend("adid", adid);
            } else {
                testLibrary.AddInfoToSend("adid", "nil");
            }
            testLibrary.SendInfoToServer(currentExtraPath);
        });
    }

    private void VerifyTrack(Dictionary<string, List<string>> parameters)
    {
        AdjustEvent adjustEvent = EventNative(parameters);
        string? localBasePath = currentExtraPath;
#if ANDROID
        Adjust.VerifyAndTrackPlayStorePurchase(adjustEvent, VerificationResultCallback(localBasePath));
#elif IOS
        Adjust.VerifyAndTrackAppStorePurchase(adjustEvent, VerificationResultCallback(localBasePath));
#endif
    }

    private void EndFirstSessionDelay(Dictionary<string, List<string>> parameters)
    {
        Adjust.EndFirstSessionDelay();
    }

    private void CoppaComplianceInDelay(Dictionary<string, List<string>> parameters)
    {
        if (FirstBoolValue(parameters, "isEnabled") is true)
        {
            Adjust.EnableCoppaComplianceInDelay();
        }

        if (FirstBoolValue(parameters, "isEnabled") is false)
        {
            Adjust.DisableCoppaComplianceInDelay();
        }
    }

    private void ExternalDeviceIdInDelay(Dictionary<string, List<string>> parameters)
    {
        if (FirstStringValue(parameters, "externalDeviceId") is string externalDeviceId)
        {
            Adjust.SetExternalDeviceIdInDelay(externalDeviceId);
        }
    }

    #endregion

    private Action<AdjustPurchaseVerificationResult> VerificationResultCallback(
        string? localBasePath) => (AdjustPurchaseVerificationResult result) =>
    {
        AddInfoToSend("verification_status", result.VerificationStatus ?? "");
        AddInfoToSend("code", Convert.ToString(result.Code));
        AddInfoToSend("message", result.Message ?? "");

        SendInfoToServer(localBasePath);
    };

    private Action<AdjustAttribution?> attributionCallbackNullable(string? localBasePath) =>
        (AdjustAttribution? attribution) =>
    {
        if (attribution is not null) {
            attributionCallback(localBasePath)(attribution);
        } else {
            AddInfoToSend("attribution", "null");
            SendInfoToServer(localBasePath);
        }
    };

    private Action<AdjustAttribution> attributionCallback(string? localBasePath) =>
        (AdjustAttribution attribution) =>
    {
        Dictionary<string, string> infoToSend = new();

        if (attribution.TrackerToken is not null)
        {
            infoToSend.Add("tracker_token", attribution.TrackerToken);
        }
        if (attribution.TrackerName is not null)
        {
            infoToSend.Add("tracker_name", attribution.TrackerName);
        }
        if (attribution.Network is not null)
        {
            infoToSend.Add("network", attribution.Network);
        }
        if (attribution.Campaign is not null)
        {
            infoToSend.Add("campaign", attribution.Campaign);
        }
        if (attribution.Adgroup is not null)
        {
            infoToSend.Add("adgroup", attribution.Adgroup);
        }
        if (attribution.Creative is not null)
        {
            infoToSend.Add("creative", attribution.Creative);
        }
        if (attribution.ClickLabel is not null)
        {
            infoToSend.Add("click_label", attribution.ClickLabel);
        }
        if (attribution.CostType is not null)
        {
            infoToSend.Add("cost_type", attribution.CostType);
        }
        if (attribution.CostAmount is double costAmountValue)
        {
            infoToSend.Add("cost_amount", costAmountValue.ToString(
                System.Globalization.CultureInfo.InvariantCulture));
        }
        if (attribution.CostCurrency is not null)
        {
            infoToSend.Add("cost_currency", attribution.CostCurrency);
        }
#if ANDROID
        if (attribution.FbInstallReferrer is not null)
        {
            infoToSend.Add("fb_install_referrer", attribution.FbInstallReferrer);
        }
#endif
        infoToSend.Add("json_response", attribution.JsonResponse);
        SetInfoToServer(infoToSend);
        SendInfoToServer(localBasePath);
    };

    private static (string, double)? RevenueCurrencyValues(
        Dictionary<string, List<string>> parameters,
        string key = "revenue")
    {
        if (FirstStringValue(parameters, key) is string currency
            && double.TryParse(
                ListValues(parameters, key)?.ElementAt(1),
                System.Globalization.CultureInfo.InvariantCulture,
                out double amount))
        {
            return (currency, amount);
        }
        else
        {
            return null;
        }
    }

    private static List<string>? ListValues(
        Dictionary<string, List<string>> parameters,
        string key)
    {
        parameters.TryGetValue(key, out List<string>? listValue);
        return listValue;
    }

    private static string? FirstStringValue(
        Dictionary<string, List<string>> parameters,
        string key)
    {
        return ListValues(parameters, key)?.FirstOrDefault();
    }

    private static bool? FirstBoolValue(
        Dictionary<string, List<string>> parameters,
        string key)
    {
        return FirstStringValue(parameters, key) switch
        {
            "true" => true,
            "false" => false,
            _ => null
        };
    }

    private static int? FirstIntValue(
        Dictionary<string, List<string>> parameters,
        string key)
    {
        return Int32.TryParse(FirstStringValue(parameters, key), out int result) ?
            result : null;
    }

    private static long? FirstLongValue(
        Dictionary<string, List<string>> parameters,
        string key)
    {
        return Int64.TryParse(FirstStringValue(parameters, key), out long result) ?
            result : null;
    }

    private static void IterateTwoPairList(
        List<string>? twoPairList, Action<string, string> TwoPairApply)
    {
        if (twoPairList is null)
        {
            return;
        }

        for (int i = 0; i + 1 < twoPairList.Count; i = i + 2)
        {
            if (twoPairList[i] is string key && twoPairList[i + 1] is string value)
            {
                TwoPairApply(key, value);
            }
        }
    }

    private static void IterateThreePairList(
        List<string>? threePairList, Action<string, string, string> threePairApply)
    {
        if (threePairList is null)
        {
            return;
        }

        for (int i = 0; i + 2 < threePairList.Count; i = i + 3)
        {
            if (threePairList[i] is string key
                && threePairList[i + 1] is string value
                && threePairList[i + 2] is string option)
            {
                threePairApply(key, value, option);
            }
        }
    }
}
