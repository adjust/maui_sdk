namespace AdjustSdk;

public enum AdjustLogLevel
{
    VERBOSE,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    ASSERT,
    SUPPRESS
}

public enum AdjustEnvironment
{
    Sandbox,
    Production
}

public partial record AdjustConfig(string AppToken, AdjustEnvironment Environment, bool AllowSuppressLogLevel = false) {
    public string? DefaultTracker { get; set; }
    public string? ExternalDeviceId { get; set; }
    public bool? IsCoppaComplianceEnabled { get; set; }
    public bool? IsSendingInBackgroundEnabled { get; set; }
    public bool? IsCostDataInAttributionEnabled { get; set; }
    public bool? IsDeviceIdsReadingOnceEnabled { get; set; }
    public bool? IsDataResidency { get; private set; }
    public bool? ShouldUseSubdomains { get; private set; }
    public int? EventDeduplicationIdsMaxSize { get; set; }
    public List<string>? UrlStrategyDomains { get; private set; }
    public AdjustLogLevel? LogLevel { get; set; }
    public Action<AdjustAttribution>? AttributionChangedDelegate { get; set; }

    public Action<AdjustEventSuccess>? EventSuccessDelegate { get; set; }
    public Action<AdjustEventFailure>? EventFailureDelegate { get; set; }
    public Action<AdjustSessionSuccess>? SessionSuccessDelegate { get; set; }
    public Action<AdjustSessionFailure>? SessionFailureDelegate { get; set; }
    public Func<string, bool>? DeferredDeeplinkDelegate { get; set; }

    internal const string SdkPrefix = "maui5.1.0";

    public void SetUrlStrategy(
        List<string> urlStrategyDomains,
        bool shouldUseSubdomains,
        bool isDataResidency)
    {
        this.UrlStrategyDomains = urlStrategyDomains;
        this.ShouldUseSubdomains = shouldUseSubdomains;
        this.IsDataResidency = isDataResidency;
    }
}

public partial class AdjustAttribution
{
    public string? TrackerToken { get; private set; }
    public string? TrackerName { get; private set; }
    public string? Network { get; private set; }
    public string? Campaign { get; private set; }
    public string? Adgroup { get; private set; }
    public string? Creative { get; private set; }
    public string? ClickLabel { get; private set; }
    public string? CostType { get; private set; }
    public double? CostAmount { get; private set; }
    public string? CostCurrency { get; private set; }
}

public partial class AdjustEventSuccess
{
    public string? Adid { get; private set; }
    public string? Message { get; private set; }
    public string? Timestamp { get; private set; }
    public string? EventToken { get; private set; }
    public string? CallbackId { get; private set; }
}

public partial class AdjustEventFailure
{
    public string? Adid { get; private set; }
    public string? Message { get; private set; }
    public string? Timestamp { get; private set; }
    public string? EventToken { get; private set; }
    public bool WillRetry { get; private set; }
    public string? CallbackId { get; private set; }

}

public partial class AdjustSessionSuccess
{
    public string? Adid { get; private set; }
    public string? Message { get; private set; }
    public string? Timestamp { get; private set; }
}

public partial class AdjustSessionFailure
{
    public string? Adid { get; private set; }
    public string? Message { get; private set; }
    public string? Timestamp { get; private set; }
    public bool WillRetry { get; private set; }
}
