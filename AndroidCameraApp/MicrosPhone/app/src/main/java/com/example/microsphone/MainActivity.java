package com.example.microsphone;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.ImageFormat;
import android.hardware.Camera;
import android.media.tv.TvContract;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity implements SurfaceHolder.Callback, Camera.PreviewCallback {



    Camera camera;
    SurfaceHolder previewHolder;
    byte[] previewBuffer;



    private DatagramSocket udpSocket;
    private InetAddress address;
    private int port;
    private boolean isStreaming = false;
    AvcEncoder encoder;

    private final static String SP_CAM_WIDTH = "cam_width";
    private final static String SP_CAM_HEIGHT = "cam_height";
    private final static String SP_DEST_IP = "dest_ip";
    private final static String SP_DEST_PORT = "dest_port";

    private final static int DEFAULT_FRAME_RATE = 15;
    private final static int DEFAULT_BIT_RATE = 500000;

    ArrayList<byte[]> encDataList = new ArrayList<byte[]>();
    ArrayList<Integer> encDataLengthList = new ArrayList<Integer>();

    Runnable senderRun = new Runnable() {
        @Override
        public void run()
        {
            while (isStreaming)
            {
                boolean empty = false;
                byte[] encData = null;

                synchronized(encDataList)
                {
                    if (encDataList.size() == 0)
                    {
                        empty = true;
                    }
                    else
                        encData = encDataList.remove(0);
                }
                if (empty)
                {
                    try {
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    continue;
                }
                try
                {
                    DatagramPacket packet = new DatagramPacket(encData, encData.length, address, port);
                    udpSocket.send(packet);
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                }
            }
            //TODO:
        }
    };

    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.camera_fragment);

    }

    public void onStartServer (View view)
    {
        this.setContentView(R.layout.activity_main);

        this.findViewById(R.id.btnCamSize).setOnClickListener(
                new View.OnClickListener()
                {
                    @Override
                    public void onClick(View v)
                    {
                        //showSettingsDlg();
                    }
                });

        this.findViewById(R.id.btnStream).setOnClickListener(
                new View.OnClickListener()
                {
                    @Override
                    public void onClick(View v)
                    {
                        if (isStreaming)
                        {
                            ((Button)v).setText("Stream");
                            //stopStream();
                        }
                        else
                        {
                            //showStreamDlg();
                        }
                    }
                });

        SurfaceView svCameraPreview = (SurfaceView) this.findViewById(R.id.svCameraPreview);
        this.previewHolder = svCameraPreview.getHolder();
        this.previewHolder.addCallback((SurfaceHolder.Callback) this);

    }


    @Override
    public void onPreviewFrame(byte[] data, Camera camera) {

    }

    @Override
    public void surfaceCreated(@NonNull SurfaceHolder holder) {

    }

    @Override
    public void surfaceChanged(@NonNull SurfaceHolder holder, int format, int width, int height) {

    }

    @Override
    public void surfaceDestroyed(@NonNull SurfaceHolder holder) {

    }
}
