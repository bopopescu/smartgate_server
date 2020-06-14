package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.nfc.NfcAdapter;
import android.os.Bundle;
import android.provider.Settings;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    private TextView tv1, tv2, tv3, tv4;
    private NfcAdapter nfcAdapter;
    private PendingIntent pendingIntent;
    private final int MY_PERMISSIONS_REQUEST_PHONE_STATE = 1000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tv1 = (TextView) findViewById(R.id.nfctagtest01);
        tv2 = (TextView) findViewById(R.id.nfctagtest02);
        nfcAdapter = NfcAdapter.getDefaultAdapter(this);
        if (nfcAdapter == null) {
            Toast.makeText(this, "nfc 안킨거 아니냐?", Toast.LENGTH_LONG).show();
            String android_id = Settings.Secure.getString(this.getContentResolver(), Settings.Secure.ANDROID_ID); //안드로이드 고유 아이디라는데 잘 모르겠네
            tv1.setText(android_id);
            tv2.setText(GetDeviceUUID(MainActivity.this));
            TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_SMS) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_NUMBERS) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_STATE) != PackageManager.PERMISSION_GRANTED) {
                // TODO: Consider calling
                //    ActivityCompat#requestPermissions
                // here to request the missing permissions, and then overriding
                //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to handle the case where the user grants the permission. See the documentation
                // for ActivityCompat#requestPermissions for more details.
                return;
            }
            String phone_number = tm.getLine1Number();
            Log.e("phone_numver", phone_number);

//            int a = "ffffffff-b5cd-c730-ffff-ffff99d603a9".hashCode();
//            tv3.setText(a);
            MakeKey mk = new MakeKey(GetDeviceUUID(MainActivity.this));
            String test_dec = mk.decrypt(mk.encrypt(GetDeviceUUID(MainActivity.this)));
            tv4.setText(test_dec);
        } else if (!nfcAdapter.isEnabled()) {
            Log.d("뭐야", "왜그래");
            startActivity(new Intent("android.settings.NFC_SETTINGS"));
        }
//        else{
//            Intent intent = new Intent(this, getClass()).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
//            pendingIntent = PendingIntent.getActivity(this, 0 ,intent, 0);
//
//        }


    }
    // Universally Unique IDentifier get
    private String GetDeviceUUID(Context context) {
        final TelephonyManager tm = (TelephonyManager) context.getSystemService(context.TELEPHONY_SERVICE);
        final String tmDevice, tmSerial, androidID;
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_STATE) != PackageManager.PERMISSION_GRANTED) {

            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.

            if(ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.READ_PHONE_STATE)){
                // Show an explanation to the user *asynchronously* -- don't block
                // this thread waiting for the user's response! After the user
                // sees the explanation, try again to request the permission.
            }
            else{
                // No explanation needed; request the permission
                ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.READ_PHONE_STATE},MY_PERMISSIONS_REQUEST_PHONE_STATE);
                // MY_PERMISSIONS_REQUEST_READ_CONTACTS is an
                // app-defined int constant. The callback method gets the
                // result of the request.
            }

        }
        else{
            // Permission has already been granted
            tmDevice = tm.getDeviceId();
            Log.d("tmDevice",tmDevice);
            tmSerial = tm.getSimSerialNumber();
            Log.d("tmSerial", tmSerial);
            androidID = android.provider.Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
            Log.d("androidID", androidID);
            UUID deviceUUID = new UUID(androidID.hashCode(), ((long)tmDevice.hashCode() << 32) | tmSerial.hashCode());
            String deviceID= deviceUUID.toString();
            Log.d("deviceUUID",deviceID);
            return deviceID;
        }
        return "error";
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grandResults){

    }
}
