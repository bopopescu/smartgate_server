package com.example.myapplication;

import android.os.Build;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;
import android.util.Log;

import androidx.annotation.RequiresApi;

import java.io.IOException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.UnrecoverableKeyException;
import java.security.cert.CertificateException;
import java.security.spec.RSAKeyGenParameterSpec;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;

// 성능 저하가 생길 수 있으니 중요한 데이터를 전송할때만 사용해보자
public class MakeKey {
    private final String androidKey;
    // 비대칭 암호화(공개키) 알고리즘 호출 상수
    private static final String ALGORITHM = "RSA/NONE/PKCS1Padding";
    KeyPairGenerator keyPairGenerator;
    KeyPair keyPair;

    public MakeKey(String androidKey){
        this.androidKey = androidKey;
        generate_key();
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    public void generate_key() {
        try {
            keyPairGenerator = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_RSA,"AndroidKeyStore");
            keyPairGenerator.initialize(new KeyGenParameterSpec.Builder("key1",KeyProperties.PURPOSE_DECRYPT | KeyProperties.PURPOSE_DECRYPT)
                    .setBlockModes(KeyProperties.BLOCK_MODE_CBC)
                    .setAlgorithmParameterSpec(new RSAKeyGenParameterSpec(2048, RSAKeyGenParameterSpec.F4))
                    .setDigests(KeyProperties.DIGEST_SHA256, KeyProperties.DIGEST_SHA512)
                    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_RSA_PKCS1)
                    .build());

            keyPair = keyPairGenerator.generateKeyPair();

        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchProviderException e) {
            e.printStackTrace();
        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        }


    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    public byte[] encrypt(final String text){

        byte[] encrypt_bytes = new byte[256];
        for(int i=0; i<encrypt_bytes.length; i++){
            encrypt_bytes[i] = 0;
        }
        Log.e("바이트 배열 내용", new String(encrypt_bytes));

        try {
            // setting environment to encrypt the key
            KeyStore keyStore = KeyStore.getInstance("AndroidKeyStore");
            keyStore.load(null);
            PublicKey publicKey = keyStore.getCertificate("key1").getPublicKey();
            Cipher cipher = Cipher.getInstance(ALGORITHM);

            String user_pubkey = publicKey.getEncoded().toString();
            cipher.init(Cipher.ENCRYPT_MODE, publicKey);
            String user_pubkey_base = Base64.encodeToString(publicKey.getEncoded(), Base64.DEFAULT);
            Log.e("pubkey2","pubkey:"+user_pubkey_base);


//            byte[] pubkey_bytes = Base64.encode(publicKey.getEncoded(), 0);
//            String pubkey = new String(pubkey_bytes);
//            Log.e("pubkey to base64.str",pubkey);

            encrypt_bytes = cipher.doFinal(text.getBytes("utf-8"));
            Log.e("바이트 배열 크기",Integer.toString(encrypt_bytes.length));
            String test_enc = Base64.encodeToString(encrypt_bytes, Base64.DEFAULT);
            Log.e("복호화 된 내용",test_enc);

        } catch (KeyStoreException e) { // keystore exception
            e.printStackTrace();
        } catch (CertificateException e) { // about keystore null (1)
            e.printStackTrace();
        } catch (NoSuchAlgorithmException e) { // about keystore null (2)
            e.printStackTrace();
        } catch (IOException e) { // about keystore null (3)
            e.printStackTrace();
        } catch (NoSuchPaddingException e) { // cipher exception
            e.printStackTrace();
        } catch (InvalidKeyException e) { //cipher key init
            e.printStackTrace();
        } catch (BadPaddingException e) { // padding problem
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) { // problem padding size
            e.printStackTrace();
        }

        Log.e("바이트 배열 내용", new String(encrypt_bytes));
        return encrypt_bytes;
    }

    public String decrypt(final byte[] encrypted_text){
        try {
            KeyStore keyStore = KeyStore.getInstance("AndroidKeyStore");
            keyStore.load(null);
            PrivateKey privateKey = (PrivateKey) keyStore.getKey("key1", null);
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.DECRYPT_MODE, privateKey);
            byte[] decryptedText = cipher.doFinal(encrypted_text);
            Log.e("복호화된 키",new String(decryptedText));
            return new String(decryptedText);
                  //keystore init                                                                       getKey except              cypher padding            cypher init              doFinal
        } catch (KeyStoreException | CertificateException | NoSuchAlgorithmException | IOException | UnrecoverableKeyException | NoSuchPaddingException | InvalidKeyException | BadPaddingException| IllegalBlockSizeException  e) { // keystore declare
            e.printStackTrace();
            String text = new String(encrypted_text);
            return text;
        }
    }

}
