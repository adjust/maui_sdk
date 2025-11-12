namespace AdjustSdk;

public partial record AdjustStoreInfo {
    internal AdjustSdk.iOSBinding.ADJStoreInfo toNative()
    {
        AdjustSdk.iOSBinding.ADJStoreInfo nativeStoreInfo = new(StoreName);

        if (StoreAppId is not null)
        {
            nativeStoreInfo.StoreAppId = StoreAppId;
        }

        return nativeStoreInfo;
    }
}