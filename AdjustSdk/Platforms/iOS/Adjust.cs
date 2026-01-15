namespace AdjustSdk;

using System;
using Foundation;

// All the code in this file is only included on iOS.
public partial class Adjust
{
    #region Platform common
    public static partial void InitSdk(AdjustConfig adjustConfig)
    {
        AdjustSdk.iOSBinding.Adjust.InitSdk(adjustConfig.toNative());
    }

    public static partial void TrackEvent(AdjustEvent adjustEvent)
    {
        AdjustSdk.iOSBinding.Adjust.TrackEvent(adjustEvent.toNative());
    }

    public static partial void Enable()
    {
        AdjustSdk.iOSBinding.Adjust.Enable();
    }

    public static partial void Disable()
    {
        AdjustSdk.iOSBinding.Adjust.Disable();
    }

    public static partial void IsEnabled(Action<bool> callback)
    {
        AdjustSdk.iOSBinding.Adjust.IsEnabledWithCompletionHandler((bool isEnabled) =>
        {
            callback(isEnabled);
        });
    }

    public static partial void SwitchToOfflineMode()
    {
        AdjustSdk.iOSBinding.Adjust.SwitchToOfflineMode();
    }

    public static partial void SwitchBackToOnlineMode()
    {
        AdjustSdk.iOSBinding.Adjust.SwitchBackToOnlineMode();
    }

    public static partial void SetPushToken(string pushToken)
    {
        AdjustSdk.iOSBinding.Adjust.SetPushTokenAsString(pushToken);
    }

    public static partial void GdprForgetMe()
    {
        AdjustSdk.iOSBinding.Adjust.GdprForgetMe();
    }

    public static partial void ProcessDeeplink(AdjustDeeplink deeplink)
    {
        AdjustSdk.iOSBinding.Adjust.ProcessDeeplink(deeplink.toNative());
    }

    public static partial void AddGlobalPartnerParameter(string key, string value)
    {
        AdjustSdk.iOSBinding.Adjust.AddGlobalPartnerParameter(value, key);
    }

    public static partial void AddGlobalCallbackParameter(string key, string value)
    {
        AdjustSdk.iOSBinding.Adjust.AddGlobalCallbackParameter(value, key);
    }

    public static partial void RemoveGlobalPartnerParameter(string key)
    {
        AdjustSdk.iOSBinding.Adjust.RemoveGlobalPartnerParameterForKey(key);
    }

    public static partial void RemoveGlobalCallbackParameter(string key)
    {
        AdjustSdk.iOSBinding.Adjust.RemoveGlobalCallbackParameterForKey(key);
    }

    public static partial void RemoveGlobalPartnerParameters()
    {
        AdjustSdk.iOSBinding.Adjust.RemoveGlobalPartnerParameters();
    }

    public static partial void RemoveGlobalCallbackParameters()
    {
        AdjustSdk.iOSBinding.Adjust.RemoveGlobalCallbackParameters();
    }

    public static partial void TrackAdRevenue(AdjustAdRevenue adRevenue)
    {
        AdjustSdk.iOSBinding.Adjust.TrackAdRevenue(adRevenue.toNative());
    }

    public static partial void TrackThirdPartySharing(AdjustThirdPartySharing thirdPartySharing)
    {
        AdjustSdk.iOSBinding.Adjust.TrackThirdPartySharing(thirdPartySharing.toNative());
    }

    public static partial void TrackMeasurementConsent(bool measurementConsent)
    {
        AdjustSdk.iOSBinding.Adjust.TrackMeasurementConsent(measurementConsent);
    }

    public static partial void GetAdid(Action<string> callback)
    {
        AdjustSdk.iOSBinding.Adjust.AdidWithCompletionHandler((string? adid) =>
        {
            if (adid is not null)
            {
                callback(adid);
            }
        });
    }

    public static partial void GetAdidWithTimeout(long timeout, Action<string?> callback)
    {
        AdjustSdk.iOSBinding.Adjust.AdidWithTimeout((nint)timeout, (string? adid) =>
        {
            callback(adid);
        });
    }

    public static partial void GetAttribution(Action<AdjustAttribution> callback)
    {
        AdjustSdk.iOSBinding.Adjust.AttributionWithCompletionHandler(
            (AdjustSdk.iOSBinding.ADJAttribution? attribution) =>
        {
            AdjustAttribution? adjustAttribution = AdjustAttribution.fromNative(attribution);

            if (adjustAttribution is null)
            {
                return;
            }

            callback(adjustAttribution);
        });
    }

    public static partial void GetAttributionWithTimeout(long timeout, Action<AdjustAttribution?> callback)
    {
        AdjustSdk.iOSBinding.Adjust.AttributionWithTimeout((nint)timeout, (AdjustSdk.iOSBinding.ADJAttribution? attribution) =>
        {
            callback(AdjustAttribution.fromNative(attribution));
        });
    }

    public static partial void GetSdkVersion(Action<string> callback)
    {
        AdjustSdk.iOSBinding.Adjust.SdkVersionWithCompletionHandler((string? sdkVersion) =>
        {
            if (sdkVersion is not null)
            {
                callback($"{AdjustConfig.SdkPrefix}@{sdkVersion}");
            }
        });
    }

    public static partial void GetLastDeeplink(Action<string?> callback)
    {
        AdjustSdk.iOSBinding.Adjust.LastDeeplinkWithCompletionHandler((NSUrl? deeplink) =>
        {
            callback(deeplink?.ToString());
        });
    }

    public static partial void ProcessAndResolveDeeplink(
        AdjustDeeplink deeplink, Action<string> callback)
    {
        AdjustSdk.iOSBinding.Adjust.ProcessAndResolveDeeplink(deeplink.toNative(),
            (string? resolvedLink) =>
            {
                if (resolvedLink is not null)
                {
                    callback(resolvedLink);
                }
            });
    }

    public static partial void SetTestOptions(Dictionary<string, object> testOptions)
    {
        AdjustSdk.iOSBinding.Adjust.SetTestOptions(NSDictionary.FromObjectsAndKeys(
            testOptions.Values.ToArray(),
            testOptions.Keys.ToArray()
        ));
    }

    public static partial void Resume()
    {
        AdjustSdk.iOSBinding.Adjust.TrackSubsessionStart();
    }

    public static partial void Pause()
    {
        AdjustSdk.iOSBinding.Adjust.TrackSubsessionEnd();
    }

    public static partial void EndFirstSessionDelay()
    {
        AdjustSdk.iOSBinding.Adjust.EndFirstSessionDelay();
    }

    public static partial void EnableCoppaComplianceInDelay()
    {
        AdjustSdk.iOSBinding.Adjust.EnableCoppaComplianceInDelay();
    }

    public static partial void DisableCoppaComplianceInDelay()
    {
        AdjustSdk.iOSBinding.Adjust.DisableCoppaComplianceInDelay();
    }

    public static partial void SetExternalDeviceIdInDelay(string? externalDeviceId)
    {
        AdjustSdk.iOSBinding.Adjust.SetExternalDeviceIdInDelay(externalDeviceId);
    }
    #endregion

    #region iOS specific
    public static partial void RequestAppTrackingAuthorization(Action<int> callback)
    {
        AdjustSdk.iOSBinding.Adjust
            .RequestAppTrackingAuthorizationWithCompletionHandler(
                (nuint status) => callback((int) status));
    }

    public static partial void TrackAppStoreSubscription(AdjustAppStoreSubscription subscription)
    {
        AdjustSdk.iOSBinding.Adjust.TrackAppStoreSubscription(subscription.toNative());
    }

    public static partial void UpdateSkanConversionValue(
        int conversionValue,
        string coarseValue,
        bool lockWindow,
        Action<string> callback)
    {
        AdjustSdk.iOSBinding.Adjust.UpdateSkanConversionValue(
            (nint)conversionValue,
            coarseValue,
            NSNumber.FromBoolean(lockWindow),
            (NSError nsError) => callback(nsError.ToString())
        );
    }

    public static partial int GetAppTrackingAuthorizationStatus()
    {
        return AdjustSdk.iOSBinding.Adjust.AppTrackingAuthorizationStatus;
    }

    public static partial void GetIdfa(Action<string> callback)
    {
        AdjustSdk.iOSBinding.Adjust.IdfaWithCompletionHandler((string? idfa) =>
        {
            if (idfa is not null)
            {
                callback(idfa);
            }
        });
    }

    public static partial void GetIdfv(Action<string> callback)
    {
        AdjustSdk.iOSBinding.Adjust.IdfvWithCompletionHandler((string? idfv) =>
        {
            if (idfv is not null)
            {
                callback(idfv);
            }
        });
    }

    public static partial void VerifyAppStorePurchase(
        AdjustAppStorePurchase purchase,
        Action<AdjustPurchaseVerificationResult> callback)
    {
        AdjustSdk.iOSBinding.Adjust.VerifyAppStorePurchase(
            purchase.toNative(),
            (AdjustSdk.iOSBinding.ADJPurchaseVerificationResult result) =>
            {
                callback(new (result.VerificationStatus, result.Code, result.Message));
            }
        );
    }

    public static partial void VerifyAndTrackAppStorePurchase(
        AdjustEvent adjustEvent,
        Action<AdjustPurchaseVerificationResult> callback)
    {
        AdjustSdk.iOSBinding.Adjust.VerifyAndTrackAppStorePurchase(
            adjustEvent.toNative(),
            (AdjustSdk.iOSBinding.ADJPurchaseVerificationResult result) =>
            {
                callback(new (result.VerificationStatus, result.Code, result.Message));
            }
        );
    }
    #endregion
}
