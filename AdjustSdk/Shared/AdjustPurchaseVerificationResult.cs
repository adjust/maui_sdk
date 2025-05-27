namespace AdjustSdk;

public partial record AdjustPurchaseVerificationResult (
    string? VerificationStatus,
    int Code,
    string? Message) {}