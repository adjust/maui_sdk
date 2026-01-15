namespace AdjustSdk;

public partial record AdjustDeeplink(string Deeplink)
{
    public string? Referrer { get; set; }
}