namespace AdjustMetaReferrer;

public class AdjustMetaReferrer
{
    /*
    public static void allowToReadMetaReferrer() {
        Com.Adjust.Sdk.Meta.AdjustMetaReferrer.ReadMetaReferrer(AppContext);
    }

    public static void doNotAllowToReadMetaReferrer() {
        Com.Adjust.Sdk.Meta.AdjustMetaReferrer.DoNotReadMetaReferrer();
    }

    public static void getMetaInstallReferrer(
        string fbAppId, OnMetaInstallReferrerReadListener listener) 
    {
        Com.Adjust.Sdk.Meta.AdjustMetaReferrer.GetMetaInstallReferrer(
            AppContext, fbAppId, new OnMetaInstallReferrerReadListenerAdapter(listener));
    }

    private static Android.Content.Context AppContext { get { return Android.App.Application.Context; } }
    */
}

/*
public interface OnMetaInstallReferrerReadListener {
    void onInstallReferrerDetailsRead(MetaInstallReferrerDetails referrerDetails);
    void onFail(string? message);
}

public record MetaInstallReferrerDetails(
    string installReferrer,
    long actualTimestampInSec,
    bool isClick
);

internal class OnMetaInstallReferrerReadListenerAdapter(OnMetaInstallReferrerReadListener listener)
    : Java.Lang.Object, Com.Adjust.Sdk.Meta.IOnMetaInstallReferrerReadListener
{
    public void OnInstallReferrerDetailsRead(global::Com.Adjust.Sdk.Meta.MetaInstallReferrerDetails? referrerDetails)
    {
        listener.onInstallReferrerDetailsRead(
            new MetaInstallReferrerDetails(
                referrerDetails!.InstallReferrer,
                referrerDetails!.ActualTimestampInSec,
                referrerDetails!.IsClick));
    }

    public void OnFail(string? message)
    {
        listener.onFail(message);
    }
}
*/