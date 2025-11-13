namespace AdjustSdk;

public partial record AdjustDeeplink
{
    internal Com.Adjust.Sdk.AdjustDeeplink toNative()
    {
        Com.Adjust.Sdk.AdjustDeeplink nativeAdjustDeeplink = new(Android.Net.Uri.Parse(Deeplink));

        if (Referrer is string referrerValue)
        {
            nativeAdjustDeeplink.Referrer = Android.Net.Uri.Parse(referrerValue);
        }

        return nativeAdjustDeeplink;
    }
}
