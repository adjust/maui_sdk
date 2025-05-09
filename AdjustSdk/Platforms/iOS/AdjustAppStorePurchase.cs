namespace AdjustSdk;

public record class AdjustAppStorePurchase(string TransactionId, string ProductId)
{
    internal AdjustSdk.iOSBinding.ADJAppStorePurchase toNative() {
        return new (TransactionId, ProductId);
    }
}
