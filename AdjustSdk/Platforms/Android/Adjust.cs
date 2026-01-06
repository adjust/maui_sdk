namespace AdjustSdk;

// All the code in this file is only included on Android.
public partial class Adjust
{
    #region Platform common
    public static partial void InitSdk(AdjustConfig adjustConfig)
    {
        Com.Adjust.Sdk.Adjust.InitSdk(adjustConfig.toNative());
    }

    public static partial void TrackEvent(AdjustEvent adjustEvent)
    {
        Com.Adjust.Sdk.Adjust.TrackEvent(adjustEvent.toNative());
    }

    public static partial void Enable()
    {
        Com.Adjust.Sdk.Adjust.Enable();
    }

    public static partial void Disable()
    {
        Com.Adjust.Sdk.Adjust.Disable();
    }

    public static partial void IsEnabled(Action<bool> callback)
    {
        Com.Adjust.Sdk.Adjust.IsEnabled(AppContext, new OnIsEnabledListenerAdapter(callback));
    }

    public static partial void SwitchToOfflineMode()
    {
        Com.Adjust.Sdk.Adjust.SwitchToOfflineMode();
    }

    public static partial void SwitchBackToOnlineMode()
    {
        Com.Adjust.Sdk.Adjust.SwitchBackToOnlineMode();
    }

    public static partial void SetPushToken(string pushToken)
    {
        Com.Adjust.Sdk.Adjust.SetPushToken(pushToken, AppContext);
    }

    public static partial void GdprForgetMe()
    {
        Com.Adjust.Sdk.Adjust.GdprForgetMe(AppContext);
    }

    public static partial void ProcessDeeplink(AdjustDeeplink deeplink)
    {
        Com.Adjust.Sdk.Adjust.ProcessDeeplink(deeplink.toNative(), AppContext);
    }

    public static partial void AddGlobalPartnerParameter(string key, string value)
    {
        Com.Adjust.Sdk.Adjust.AddGlobalPartnerParameter(key, value);
    }

    public static partial void AddGlobalCallbackParameter(string key, string value)
    {
        Com.Adjust.Sdk.Adjust.AddGlobalCallbackParameter(key, value);
    }

    public static partial void RemoveGlobalPartnerParameter(string key)
    {
        Com.Adjust.Sdk.Adjust.RemoveGlobalPartnerParameter(key);
    }

    public static partial void RemoveGlobalCallbackParameter(string key)
    {
        Com.Adjust.Sdk.Adjust.RemoveGlobalCallbackParameter(key);
    }

    public static partial void RemoveGlobalPartnerParameters()
    {
        Com.Adjust.Sdk.Adjust.RemoveGlobalPartnerParameters();
    }

    public static partial void RemoveGlobalCallbackParameters()
    {
        Com.Adjust.Sdk.Adjust.RemoveGlobalCallbackParameters();
    }

    public static partial void TrackAdRevenue(AdjustAdRevenue adRevenue)
    {
        Com.Adjust.Sdk.Adjust.TrackAdRevenue(adRevenue.toNative());
    }

    public static partial void TrackThirdPartySharing(AdjustThirdPartySharing thirdPartySharing)
    {
        Com.Adjust.Sdk.Adjust.TrackThirdPartySharing(thirdPartySharing.toNative());
    }

    public static partial void TrackMeasurementConsent(bool measurementConsent)
    {
        Com.Adjust.Sdk.Adjust.TrackMeasurementConsent(measurementConsent);
    }

    public static partial void GetAdid(Action<string> callback)
    {
        Com.Adjust.Sdk.Adjust.GetAdid(new OnAdidReadListenerAdapter(callback));
    }

    public static partial void GetAdidWithTimeout(long timeout, Action<string?> callback)
    {
        Com.Adjust.Sdk.Adjust.GetAdidWithTimeout(AppContext, timeout, new OnAdidReadListenerAdapterNullable(callback));
    }

    public static partial void GetAttribution(Action<AdjustAttribution> callback)
    {
        Com.Adjust.Sdk.Adjust.GetAttribution(new OnAttributionReadListenerAdapter(callback));
    }

    public static partial void GetAttributionWithTimeout(long timeout, Action<AdjustAttribution?> callback)
    {
        Com.Adjust.Sdk.Adjust.GetAttributionWithTimeout(AppContext, timeout, new OnAttributionReadListenerAdapterNullable(callback));
    }

    public static partial void GetSdkVersion(Action<string> callback)
    {
        Com.Adjust.Sdk.Adjust.GetSdkVersion(new OnSdkVersionReadListenerAdapter(callback));
    }

    public static partial void GetLastDeeplink(Action<string?> callback)
    {
        Com.Adjust.Sdk.Adjust.GetLastDeeplink(
            AppContext, new OnLastDeeplinkReadListenerAdapter(callback));
    }

    public static partial void ProcessAndResolveDeeplink(
        AdjustDeeplink deeplink, Action<string> callback)
    {
        Com.Adjust.Sdk.Adjust.ProcessAndResolveDeeplink(
            deeplink.toNative(),
            AppContext,
            new OnDeeplinkResolvedListenerAdapter(callback));
    }

    public static partial void SetTestOptions(Dictionary<string, object> testOptions)
    {
        Com.Adjust.Sdk.Adjust.SetTestOptions(TestOptionsToNative(testOptions));
    }

    public static partial void Resume()
    {
        Com.Adjust.Sdk.Adjust.OnResume();
    }

    public static partial void Pause()
    {
        Com.Adjust.Sdk.Adjust.OnPause();
    }

    public static partial void EndFirstSessionDelay()
    {
        Com.Adjust.Sdk.Adjust.EndFirstSessionDelay();
    }

    public static partial void EnableCoppaComplianceInDelay()
    {
        Com.Adjust.Sdk.Adjust.EnableCoppaComplianceInDelay();
    }

    public static partial void DisableCoppaComplianceInDelay()
    {
        Com.Adjust.Sdk.Adjust.DisableCoppaComplianceInDelay();
    }

    public static partial void SetExternalDeviceIdInDelay(string? externalDeviceId)
    {
        Com.Adjust.Sdk.Adjust.SetExternalDeviceIdInDelay(externalDeviceId);
    }
    #endregion

    #region Android specific
    public static partial void TrackPlayStoreSubscription(AdjustPlayStoreSubscription subscription)
    {
        Com.Adjust.Sdk.Adjust.TrackPlayStoreSubscription(subscription.toNative());
    }

    public static partial void GetGoogleAdId(Action<string> callback)
    {
        Com.Adjust.Sdk.Adjust.GetGoogleAdId(
            AppContext, new OnGoogleAdIdReadListenerAdapter(callback));
    }

    public static partial void GetAmazonAdId(Action<string?> callback)
    {
        Com.Adjust.Sdk.Adjust.GetAmazonAdId(
            AppContext, new OnAmazonAdIdReadListenerAdapter(callback));
    }

    public static partial void VerifyPlayStorePurchase(
        AdjustPlayStorePurchase purchase,
        Action<AdjustPurchaseVerificationResult> verificationResultCallback)
    {
        Com.Adjust.Sdk.Adjust.VerifyPlayStorePurchase(purchase.toNative(),
            new OnPurchaseVerificationFinishedListenerAdapter(verificationResultCallback));
    }

    public static partial void VerifyAndTrackPlayStorePurchase(
        AdjustEvent adjustEvent,
        Action<AdjustPurchaseVerificationResult> verificationResultCallback)
    {
        Com.Adjust.Sdk.Adjust.VerifyAndTrackPlayStorePurchase(adjustEvent.toNative(),
            new OnPurchaseVerificationFinishedListenerAdapter(verificationResultCallback));
    }

    public static partial void EnablePlayStoreKidsComplianceInDelay()
    {
        Com.Adjust.Sdk.Adjust.EnablePlayStoreKidsComplianceInDelay();
    }

    public static partial void DisablePlayStoreKidsComplianceInDelay()
    {
        Com.Adjust.Sdk.Adjust.DisablePlayStoreKidsComplianceInDelay();
    }
    #endregion

    internal static Android.Content.Context AppContext { get { return Android.App.Application.Context; } }

    private static Nullable<TValue> OptionVal<TValue>(Dictionary<string, object> options, string key)
        where TValue : struct
    {
        if (options.TryGetValue(key, out object? objectValue)
            && objectValue is TValue value)
        {
            return value;
        }
        return null;
    }

    private static TValue? OptionRef<TValue>(Dictionary<string, object> options, string key)
        where TValue : class
    {
        if (options.TryGetValue(key, out object? objectValue)
            && objectValue is TValue value)
        {
            return value;
        }
        return null;
    }

    private static Com.Adjust.Sdk.AdjustTestOptions TestOptionsToNative(
        Dictionary<string, object> testOptions)
    {
        Com.Adjust.Sdk.AdjustTestOptions nativeTestOptions = new ();
        nativeTestOptions.BaseUrl = OptionRef<string>(testOptions, "baseUrl");
        nativeTestOptions.GdprUrl = OptionRef<string>(testOptions, "gdprUrl");
        nativeTestOptions.SubscriptionUrl = OptionRef<string>(testOptions, "subscriptionUrl");
        nativeTestOptions.PurchaseVerificationUrl = OptionRef<string>(testOptions, "purchaseVerificationUrl");

        if (OptionRef<string>(testOptions, "extraPath") is string extraPath)
        {
            nativeTestOptions.BasePath = extraPath;
            nativeTestOptions.GdprPath = extraPath;
            nativeTestOptions.SubscriptionPath = extraPath;
            nativeTestOptions.PurchaseVerificationPath = extraPath;
        }

        if (OptionVal<bool>(testOptions, "deleteState") is true)
        {
            nativeTestOptions.Context = AppContext;
        }

        if (OptionVal<long>(testOptions, "timerIntervalInMilliseconds") is long timerIntervalInMilliseconds)
        {
            nativeTestOptions.TimerIntervalInMilliseconds =
                Java.Lang.Long.ValueOf(timerIntervalInMilliseconds);
        }

        if (OptionVal<long>(testOptions, "timerStartInMilliseconds")
            is long timerStartInMilliseconds)
        {
            nativeTestOptions.TimerStartInMilliseconds =
                Java.Lang.Long.ValueOf(timerStartInMilliseconds);
        }

        if (OptionVal<long>(testOptions, "sessionIntervalInMilliseconds")
            is long sessionIntervalInMilliseconds)
        {
            nativeTestOptions.SessionIntervalInMilliseconds =
                Java.Lang.Long.ValueOf(sessionIntervalInMilliseconds);
        }

        if (OptionVal<long>(testOptions, "subsessionIntervalInMilliseconds")
            is long subsessionIntervalInMilliseconds)
        {
            nativeTestOptions.SubsessionIntervalInMilliseconds =
                Java.Lang.Long.ValueOf(subsessionIntervalInMilliseconds);
        }

        if (OptionVal<bool>(testOptions, "teardown") is bool teardown)
        {
            nativeTestOptions.Teardown = Java.Lang.Boolean.ValueOf(teardown);
        }

        if (OptionVal<bool>(testOptions, "noBackoffWait") is bool noBackoffWait)
        {
            nativeTestOptions.NoBackoffWait = Java.Lang.Boolean.ValueOf(noBackoffWait);
        }

        if (OptionVal<bool>(testOptions, "ignoreSystemLifecycleBootstrap")
            is bool ignoreSystemLifecycleBootstrap)
        {
            nativeTestOptions.IgnoreSystemLifecycleBootstrap =
                Java.Lang.Boolean.ValueOf(ignoreSystemLifecycleBootstrap);
        }

        return nativeTestOptions;
    }
}
