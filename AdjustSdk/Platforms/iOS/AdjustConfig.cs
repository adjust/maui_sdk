namespace AdjustSdk;

using Foundation;

public partial class AdjustConfig
{
    public bool? IsAdServicesEnabled { get; set; }
    public bool? IsIdfaReadingEnabled { get; set; }
    public bool? IsIdfvReadingEnabled { get; set; }
    public bool? IsSkanAttributionEnabled { get; set; }
    public bool? IsLinkMeEnabled { get; set; }
    public int? AttConsentWaitingInterval { get; set; }
    public Action<Dictionary<string, string>>? SkanUpdatedDelegate { get; set; }

    internal AdjustSdk.iOSBinding.ADJConfig toNative()
    {
        NSString? nativeEnvironment = Environment switch
        {
            AdjustEnvironment.Sandbox => AdjustSdk.iOSBinding.Constants.ADJEnvironmentSandbox,
            AdjustEnvironment.Production => AdjustSdk.iOSBinding.Constants.ADJEnvironmentProduction,
            _ => null,
        };

        AdjustSdk.iOSBinding.ADJConfig nativeAdjustConfig = AllowSuppressLogLevel switch
        {
            bool allowSuppressLogLevel => new AdjustSdk.iOSBinding.ADJConfig(AppToken, nativeEnvironment, allowSuppressLogLevel),
            _ => new AdjustSdk.iOSBinding.ADJConfig(AppToken, nativeEnvironment)
        };

        AdjustSdk.iOSBinding.ADJLogLevel? nativeLogLevel = LogLevel switch
        {
            AdjustLogLevel.VERBOSE => AdjustSdk.iOSBinding.ADJLogLevel.Verbose,
            AdjustLogLevel.DEBUG => AdjustSdk.iOSBinding.ADJLogLevel.Debug,
            AdjustLogLevel.INFO => AdjustSdk.iOSBinding.ADJLogLevel.Info,
            AdjustLogLevel.WARN => AdjustSdk.iOSBinding.ADJLogLevel.Warn,
            AdjustLogLevel.ERROR => AdjustSdk.iOSBinding.ADJLogLevel.Error,
            AdjustLogLevel.ASSERT => AdjustSdk.iOSBinding.ADJLogLevel.Assert,
            AdjustLogLevel.SUPPRESS => AdjustSdk.iOSBinding.ADJLogLevel.Suppress,
            _ => null
        };

        if (nativeLogLevel is AdjustSdk.iOSBinding.ADJLogLevel nativeLogLevelValue)
        {
            nativeAdjustConfig.LogLevel = nativeLogLevelValue;
        }

        nativeAdjustConfig.SdkPrefix = AdjustConfig.SdkPrefix;

        if (IsDeviceIdsReadingOnceEnabled is true)
        {
            nativeAdjustConfig.EnableDeviceIdsReadingOnce();
        }

        if (IsCoppaComplianceEnabled is true)
        {
            nativeAdjustConfig.EnableCoppaCompliance();
        }

        if (IsSendingInBackgroundEnabled is true)
        {
            nativeAdjustConfig.EnableSendingInBackground();
        }

        if (IsCostDataInAttributionEnabled is true)
        {
            nativeAdjustConfig.EnableCostDataInAttribution();
        }

        if (DefaultTracker is string defaultTrackerValue)
        {
            nativeAdjustConfig.DefaultTracker = defaultTrackerValue;
        }

        if (ExternalDeviceId is string externalDeviceIdValue)
        {
            nativeAdjustConfig.ExternalDeviceId = externalDeviceIdValue;
        }

        if (EventDeduplicationIdsMaxSize is int eventDeduplicationIdsMaxSizeValue)
        {
            nativeAdjustConfig.EventDeduplicationIdsMaxSize =
                (nint)EventDeduplicationIdsMaxSize;
        }

        if (UrlStrategyDomains is List<string> urlStrategyDomainsValue)
        {
            nativeAdjustConfig.SetUrlStrategy(
                NSArray.FromObjects(urlStrategyDomainsValue.ToArray()),
                ShouldUseSubdomains ?? false,
                IsDataResidency ?? false);
        }

        if (AdjustDelegateAdapter.adaptNative(this) is AdjustDelegateAdapter adjustDelegateAdapter)
        {
            nativeAdjustConfig.Delegate = adjustDelegateAdapter;
        }

        if (IsAdServicesEnabled is false)
        {
            nativeAdjustConfig.DisableAdServices();
        }

        if (IsIdfaReadingEnabled is false)
        {
            nativeAdjustConfig.DisableIdfaReading();
        }

        if (IsIdfvReadingEnabled is false)
        {
            nativeAdjustConfig.DisableIdfvReading();
        }

        if (IsSkanAttributionEnabled is false)
        {
            nativeAdjustConfig.DisableSkanAttribution();
        }

        if (IsLinkMeEnabled is true)
        {
            nativeAdjustConfig.EnableLinkMe();
        }

        if (AttConsentWaitingInterval is int attConsentWaitingIntervalValue)
        {
            nativeAdjustConfig.AttConsentWaitingInterval = (nuint)attConsentWaitingIntervalValue;
        }

        return nativeAdjustConfig;
    }
}

public partial class AdjustAttribution
{
    internal static AdjustAttribution? fromNative(AdjustSdk.iOSBinding.ADJAttribution? nativeAttribution)
    {
        if (nativeAttribution is null)
        {
            return null;
        }

        return new()
        {
            TrackerToken = nativeAttribution.TrackerToken,
            TrackerName = nativeAttribution.TrackerName,
            Network = nativeAttribution.Network,
            Campaign = nativeAttribution.Campaign,
            Adgroup = nativeAttribution.Adgroup,
            Creative = nativeAttribution.Creative,
            ClickLabel = nativeAttribution.ClickLabel,
            CostType = nativeAttribution.CostType,
            CostAmount = nativeAttribution.CostAmount?.DoubleValue,
            CostCurrency = nativeAttribution.CostCurrency
        };
    }
}

internal class AdjustDelegateAdapter : AdjustSdk.iOSBinding.AdjustDelegate
{
    internal Action<AdjustAttribution>? AttributionChangedDelegate { get; private set; }
    internal Action<AdjustEventSuccess>? EventSuccessDelegate { get; private set; }
    internal Action<AdjustEventFailure>? EventFailureDelegate { get; private set; }
    internal Action<AdjustSessionSuccess>? SessionSuccessDelegate { get; private set; }
    internal Action<AdjustSessionFailure>? SessionFailureDelegate { get; private set; }
    internal Func<string, bool>? DeferredDeeplinkDelegate { get; private set; }
    internal Action<Dictionary<string, string>>? SkanUpdatedDelegate { get; private set; }

    internal static AdjustDelegateAdapter? adaptNative(AdjustConfig adjustConfig)
    {
        if (adjustConfig.AttributionChangedDelegate is null 
        && adjustConfig.EventSuccessDelegate is null
        && adjustConfig.EventFailureDelegate is null
        && adjustConfig.SessionSuccessDelegate is null
        && adjustConfig.SessionFailureDelegate is null
        && adjustConfig.DeferredDeeplinkDelegate is null
        && adjustConfig.SkanUpdatedDelegate is null)
        {
            return null;
        }
        return new()
        {
            AttributionChangedDelegate = adjustConfig.AttributionChangedDelegate,
            EventSuccessDelegate = adjustConfig.EventSuccessDelegate,
            EventFailureDelegate = adjustConfig.EventFailureDelegate,
            SessionSuccessDelegate = adjustConfig.SessionSuccessDelegate,
            SessionFailureDelegate = adjustConfig.SessionFailureDelegate,
            DeferredDeeplinkDelegate = adjustConfig.DeferredDeeplinkDelegate,
            SkanUpdatedDelegate = adjustConfig.SkanUpdatedDelegate,
        };
    }
    public override void AdjustAttributionChanged(AdjustSdk.iOSBinding.ADJAttribution? nativeAttribution)
    {
        if (AttributionChangedDelegate is null)
        {
            return;
        }
        
        if (AdjustAttribution.fromNative(nativeAttribution) is AdjustAttribution adjustAttribution)
        {
            AttributionChangedDelegate(adjustAttribution);
        }
    }
    public override void AdjustEventTrackingSucceeded(AdjustSdk.iOSBinding.ADJEventSuccess? eventSuccessResponse)
    {
        if (EventSuccessDelegate is null)
        {
            return;
        }

        if (AdjustEventSuccess.fromNative(eventSuccessResponse) is AdjustEventSuccess result)
        {
            EventSuccessDelegate(result);
        }
    }

	public override void AdjustEventTrackingFailed(AdjustSdk.iOSBinding.ADJEventFailure? eventFailureResponse)
    {
        if (EventFailureDelegate is null)
        {
            return;
        }

        if (AdjustEventFailure.fromNative(eventFailureResponse) is AdjustEventFailure result)
        {
            EventFailureDelegate(result);
        }
    }

    public override void AdjustSessionTrackingSucceeded(AdjustSdk.iOSBinding.ADJSessionSuccess? sessionSuccessResponse)
    {
        if (SessionSuccessDelegate is null)
        {
            return;
        }

        if (AdjustSessionSuccess.fromNative(sessionSuccessResponse) is AdjustSessionSuccess result)
        {
            SessionSuccessDelegate(result);
        }
    }

    public override void AdjustSessionTrackingFailed(AdjustSdk.iOSBinding.ADJSessionFailure? sessionFailureResponse)
    {
        if (SessionFailureDelegate is null)
        {
            return;
        }

        if (AdjustSessionFailure.fromNative(sessionFailureResponse) is AdjustSessionFailure result)
        {
            SessionFailureDelegate(result);
        }
    }

	public override bool AdjustDeferredDeeplinkReceived(NSUrl? nativeDeeplink)
    {
        if (DeferredDeeplinkDelegate is null)
        {
            return false;
        }

        if (nativeDeeplink?.ToString() is string deeplink)
        {
            return DeferredDeeplinkDelegate(deeplink);
        }

        return false;
    }

	public override void AdjustSkanUpdatedWithConversionData(NSDictionary<NSString, NSString> nativeData)
    {
        if (SkanUpdatedDelegate is null)
        {
            return;
        }

        Dictionary<string, string> data = new ();
        foreach (KeyValuePair<NSObject, NSObject> kvp in nativeData)
        {
            data.Add(kvp.Key.ToString(), kvp.Value.ToString());
        }

        SkanUpdatedDelegate(data);
    }
}

public partial class AdjustEventSuccess
{
    public NSDictionary? JsonResponse { get; private set; }

    internal static AdjustEventSuccess? fromNative(
        AdjustSdk.iOSBinding.ADJEventSuccess? nativeAdjustEventSuccess)
    {
        if (nativeAdjustEventSuccess is null)
        {
            return null;
        }

        return new()
        {
            Adid = nativeAdjustEventSuccess.Adid,
            Message = nativeAdjustEventSuccess.Message,
            Timestamp = nativeAdjustEventSuccess.Timestamp,
            EventToken = nativeAdjustEventSuccess.EventToken,
            CallbackId = nativeAdjustEventSuccess.CallbackId,
            JsonResponse = nativeAdjustEventSuccess.JsonResponse,
        };
    }
}

public partial class AdjustEventFailure
{
    public NSDictionary? JsonResponse { get; private set; }

    internal static AdjustEventFailure? fromNative(
        AdjustSdk.iOSBinding.ADJEventFailure? nativeAdjustEventFailure)
    {
        if (nativeAdjustEventFailure is null)
        {
            return null;
        }

        return new()
        {
            Adid = nativeAdjustEventFailure.Adid,
            Message = nativeAdjustEventFailure.Message,
            Timestamp = nativeAdjustEventFailure.Timestamp,
            EventToken = nativeAdjustEventFailure.EventToken,
            WillRetry = nativeAdjustEventFailure.WillRetry,
            CallbackId = nativeAdjustEventFailure.CallbackId,
            JsonResponse = nativeAdjustEventFailure.JsonResponse,
        };
    }
}


public partial class AdjustSessionSuccess
{
    public NSDictionary? JsonResponse { get; private set; }

    internal static AdjustSessionSuccess? fromNative(
        AdjustSdk.iOSBinding.ADJSessionSuccess? nativeAdjustSessionSuccess)
    {
        if (nativeAdjustSessionSuccess is null)
        {
            return null;
        }

        return new()
        {
            Adid = nativeAdjustSessionSuccess.Adid,
            Message = nativeAdjustSessionSuccess.Message,
            Timestamp = nativeAdjustSessionSuccess.Timestamp,
            JsonResponse = nativeAdjustSessionSuccess.JsonResponse,
        };
    }
}

public partial class AdjustSessionFailure
{
    public NSDictionary? JsonResponse { get; private set; }

    internal static AdjustSessionFailure? fromNative(
        AdjustSdk.iOSBinding.ADJSessionFailure? nativeAdjustSessionFailure)
    {
        if (nativeAdjustSessionFailure is null)
        {
            return null;
        }

        return new()
        {
            Adid = nativeAdjustSessionFailure.Adid,
            Message = nativeAdjustSessionFailure.Message,
            Timestamp = nativeAdjustSessionFailure.Timestamp,
            WillRetry = nativeAdjustSessionFailure.WillRetry,
            JsonResponse = nativeAdjustSessionFailure.JsonResponse,
        };
    }
}
