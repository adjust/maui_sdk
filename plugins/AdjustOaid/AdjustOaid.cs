namespace AdjustOaid;

public class AdjustOaid
{
    public static void allowToReadOaid() {
        Com.Adjust.Sdk.Oaid.AdjustOaid.ReadOaid();
    }

    public static void doNotAllowToReadOaid() {
        Com.Adjust.Sdk.Oaid.AdjustOaid.DoNotReadOaid();
    }

    public static void readOaid() {
        Com.Adjust.Sdk.Oaid.AdjustOaid.ReadOaid(AppContext);
    }
/*
    public static void getOaid(OnOaidReadListener listener) {
        Com.Adjust.Sdk.Oaid.AdjustOaid.GetOaid(AppContext,
            new OnOaidReadListenerAdapter(listener));
    }
*/
    private static Android.Content.Context AppContext { get { return Android.App.Application.Context; } }
}
/*
public interface OnOaidReadListener {
    void onOaidRead(string? oaid);
    void onFail(string? message);
}

internal class OnOaidReadListenerAdapter(OnOaidReadListener listener)
    : Java.Lang.Object, Com.Adjust.Sdk.Oaid.IOnOaidReadListener
{
    public void OnOaidRead(string? oaid)
    {
        listener.onOaidRead(oaid);
    }
    public void OnFail(string? message)
    {
        listener.onFail(message);
    }
}
*/