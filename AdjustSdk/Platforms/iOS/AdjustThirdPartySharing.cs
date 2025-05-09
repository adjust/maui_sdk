namespace AdjustSdk;

public partial class AdjustThirdPartySharing  {
    internal AdjustSdk.iOSBinding.ADJThirdPartySharing toNative() {
        AdjustSdk.iOSBinding.ADJThirdPartySharing nativeAdjustThirdPartySharing = new(IsEnabled);
        
        if (GranularOptions is not null) {
            foreach (var element in GranularOptions) {
                nativeAdjustThirdPartySharing.AddGranularOption(
                    element.PartnerName, element.Key, element.StringValue);
            }
        }

        if (PartnerSharingSettings is not null) {
            foreach (var element in PartnerSharingSettings) {
                nativeAdjustThirdPartySharing.AddPartnerSharingSetting(
                    element.PartnerName, element.Key, element.BoolValue);
            }
        }

        return nativeAdjustThirdPartySharing;
    }

}