namespace AdjustSdk;

public partial record AdjustThirdPartySharing(bool? IsEnabled)  {
    internal List<GranularOptionsArgs>? GranularOptions { get; set; }
    internal readonly record struct GranularOptionsArgs(
        string PartnerName, string Key, string StringValue) {}
    internal List<PartnerSharingSettingsArgs>? PartnerSharingSettings { get; set; }
    internal readonly record struct PartnerSharingSettingsArgs(
        string PartnerName, string Key, bool BoolValue) {}

    public void AddGranularOption(string partnerName, string key, string value) {
        GranularOptions ??= new();
        GranularOptions.Add(new(partnerName, key, value));
    }

    public void AddPartnerSharingSettings(string partnerName, string key, bool value)
    {
        PartnerSharingSettings ??= new ();
        PartnerSharingSettings.Add(new(partnerName, key, value));
    }
}