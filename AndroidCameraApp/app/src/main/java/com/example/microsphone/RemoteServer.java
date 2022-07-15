package com.example.microsphone;

import fi.iki.elonen.NanoHTTPD;
public class RemoteServer extends NanoHTTPD
{
    private MainActivity mainActivity;
    public RemoteServer(MainActivity mainActivity, int port) {
        super(port);
        this.mainActivity = mainActivity;
    }

    @Override
    public Response serve(IHTTPSession session) {
        return newFixedLengthResponse("Hello");
    }
}
