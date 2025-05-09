namespace AdjustSdk;

public partial class AdjustAdRevenue {

    internal AdjustSdk.iOSBinding.ADJAdRevenue toNative() {
        AdjustSdk.iOSBinding.ADJAdRevenue nativeAdRevenue = new (Source);

        if (Revenue is double revenueValue && Currency is not null) {
            nativeAdRevenue.SetRevenue(revenueValue, Currency);
        }

        AdjustUtil.iterateTwoPairList(innerCallbackParameters,
            nativeAdRevenue.AddCallbackParameter);

        AdjustUtil.iterateTwoPairList(innerPartnerParameters,
            nativeAdRevenue.AddPartnerParameter);

        if (AdImpressionsCount is int adImpressionsCountValue) {
            nativeAdRevenue.SetAdImpressionsCount(adImpressionsCountValue);
        }

        if (AdRevenueNetwork is not null) {
            nativeAdRevenue.SetAdRevenueNetwork(AdRevenueNetwork);
        }

        if (AdRevenueUnit is not null) {
            nativeAdRevenue.SetAdRevenueUnit(AdRevenueUnit);
        }
        if (AdRevenuePlacement is not null) {
            nativeAdRevenue.SetAdRevenuePlacement(AdRevenuePlacement);
        }

        return nativeAdRevenue;
    }
}
