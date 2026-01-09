namespace AdjustSdk;

using Foundation;

public partial record AdjustDeeplink
{
    internal AdjustSdk.iOSBinding.ADJDeeplink toNative()
    {
        AdjustSdk.iOSBinding.ADJDeeplink nativeAdjustDeeplink = new(new NSUrl(Deeplink));

        if (Referrer is string referrerValue)
        {
            nativeAdjustDeeplink.SetReferrer(new NSUrl(referrerValue));
        }

        return nativeAdjustDeeplink;
    }
}
