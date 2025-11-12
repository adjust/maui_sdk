namespace AdjustSdk;

public partial record AdjustStoreInfo(string StoreName) {
    public string? StoreAppId { get; set; }
}