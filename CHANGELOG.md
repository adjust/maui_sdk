### Version 5.5.0 (15th January 2026)

#### Added
- Added `GetAdidWithTimeout` method to the `Adjust` API to allow retrieving the ADID with a specified timeout. If the value is not obtained in time, `null` is returned via the callback.
- Added `GetAttributionWithTimeout` method to the `Adjust` API to allow retrieving the current attribution information with a specified timeout. If the value is not obtained in time, `null` is returned via the callback.
- Added ability to disable the reading of the app set ID on Android. You can do this by setting `IsAppSetIdReadingEnabled` property on your `AdjustConfig` instance to `false`.
- Added ability to disable SDK's interaction with `AppTrackingTransparency.framework` API. You can disable it by setting the `IsAppTrackingTransparencyUsageEnabled` property on your `AdjustConfig` instance to `false`.
- Added ability to initialize the SDK for the first session in delayed mode. You can start the SDK in the delayed mode by setting the `IsFirstSessionDelayEnabled` property on your `AdjustConfig` instance to `true`. To end the delay, make sure to call `EndFirstSessionDelay` method of `Adjust` instance. Additionally, you can use `EnableCoppaComplianceInDelay`, `DisableCoppaComplianceInDelay`, `SetExternalDeviceIdInDelay` methods, and on Android `EnablePlayStoreKidsComplianceInDelay` and `DisablePlayStoreKidsComplianceInDelay` methods.
- Added support for configuring store information via the `AdjustStoreInfo` object. You can now specify the store name and store app ID assigning `StoreInfo` property on your `AdjustConfig` instance. This enables the SDK to record the intended app store source during initialization.
- Added ability to send organic search referrer together with deep link. You can send it by setting the `Referrer` property of the `AdjustDeeplink` instance.
- Added `JsonResponse` field to `AdjustAttribution` where every key-value pair sent by the backend as part of the attribution response can be found.
- Added support for .NET 10 target frameworks for Android and iOS (conditional on the installed .NET SDK).
- Added Android plugin packages for Google License Verification (LVL), Meta Referrer, and OAID.

#### Changed
- Updated the Adjust Signature library version to 3.62.0.
- Improved iOS backoff strategy and Apple Ads flows.

#### Native SDKs
- [iOS@v5.5.1](https://github.com/adjust/ios_sdk/tree/v5.5.1)
- [Android@v5.5.0](https://github.com/adjust/android_sdk/tree/v5.5.0)

---

### Version 5.1.1 (19th September 2025)
#### Changed
- Replaced `Platform.AppContext` with `Android.App.Application.Context` to improve SDK's compatibility with (non MAUI) .NET apps for iOS and Android.

#### Native SDKs
- [iOS@v5.1.1](https://github.com/adjust/ios_sdk/tree/v5.1.1)
- [Android@v5.1.0](https://github.com/adjust/android_sdk/tree/v5.1.0)

---

### Version 5.1.0 (27th May 2025)
#### Added
- Initial release of the Adjust SDK for MAUI.

#### Native SDKs
- [iOS@v5.1.1](https://github.com/adjust/ios_sdk/tree/v5.1.1)
- [Android@v5.1.0](https://github.com/adjust/android_sdk/tree/v5.1.0)
