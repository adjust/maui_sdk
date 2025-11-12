namespace AdjustSdk;

public partial record AdjustStoreInfo {
    internal Com.Adjust.Sdk.AdjustStoreInfo toNative()
    {
        Com.Adjust.Sdk.AdjustStoreInfo nativeStoreInfo = new(StoreName);

        if (StoreAppId is not null)
        {
            nativeStoreInfo.SetStoreAppId(StoreAppId);
        }

        return nativeStoreInfo;
    }
}