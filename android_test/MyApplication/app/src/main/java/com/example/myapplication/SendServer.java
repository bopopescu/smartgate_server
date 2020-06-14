package com.example.myapplication;

import android.os.AsyncTask;

import java.net.MalformedURLException;
import java.net.URL;

public class SendServer extends AsyncTask<String, Void, Void> {

    @Override
    protected Void doInBackground(String... params) {

        StringBuilder output = new StringBuilder();

        try {
            URL url = new URL("www.localhost:8000/");
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        return null;
    }
}
