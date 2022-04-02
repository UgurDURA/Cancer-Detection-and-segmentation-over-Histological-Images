package com.example.microsphone;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureException;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.PreviewView;
import androidx.core.content.ContextCompat;
import androidx.lifecycle.LifecycleOwner;

import android.content.Context;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.HandlerThread;
import android.util.Size;
import android.util.SparseIntArray;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.common.util.concurrent.ListenableFuture;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executor;

public class MainActivity<stastic> extends AppCompatActivity implements View.OnClickListener {

    private ListenableFuture<ProcessCameraProvider> cameraProviderFuture;


    private TextureView mTextureView;
    public static ArrayList<String> logList = new ArrayList<>();
    public  static String text2 = "App Started";
    public static int i;

    private TextureView.SurfaceTextureListener mSurfaceTextureListener = new TextureView.SurfaceTextureListener()
    {
        @Override
        public void onSurfaceTextureAvailable(@NonNull SurfaceTexture surface, int width, int height)
        {
            Toast.makeText(MainActivity.this, "Texture view is available", Toast.LENGTH_SHORT).show();

            try {
                setupCamera(width,height);
            } catch (CameraAccessException e) {
                e.printStackTrace();
            }


        }

        @Override
        public void onSurfaceTextureSizeChanged(@NonNull SurfaceTexture surface, int width, int height) {

        }

        @Override
        public boolean onSurfaceTextureDestroyed(@NonNull SurfaceTexture surface) {
            return false;
        }

        @Override
        public void onSurfaceTextureUpdated(@NonNull SurfaceTexture surface) {

        }
    };

    Button bTakePicture, bRecording;
    private ImageCapture imageCapture;
    private Object LifecycleOwner;
    private TextView nameText;
    private CameraDevice mCameraDevice;
    private CameraDevice.StateCallback mCameraDeviceStateCallback = new CameraDevice.StateCallback() {
        @Override
        public void onOpened(@NonNull CameraDevice camera)
        {
            mCameraDevice = camera;


        }

        @Override
        public void onDisconnected(@NonNull CameraDevice camera)
        {
            camera.close();
            mCameraDevice = null;
        }

        @Override
        public void onError(@NonNull CameraDevice camera, int error)
        {
            camera.close();
            mCameraDevice = null;

        }
    };

    private  String mcameraID;
    private Size mPreviewSize;
    private HandlerThread mBackgroundHandlerThread;
    private Handler mBackgroundHandler;
    private static SparseIntArray ORIENTATIONS = new SparseIntArray();
    static
    {
        ORIENTATIONS.append(Surface.ROTATION_0,0);
        ORIENTATIONS.append(Surface.ROTATION_90,90);
        ORIENTATIONS.append(Surface.ROTATION_180,180);
        ORIENTATIONS.append(Surface.ROTATION_270,270);
    }

    private static class CompareSizeByArea implements Comparator<Size>{
        @Override
        public int compare(Size lhs, Size rhs) {
            return (int) (Long.signum((long) lhs.getWidth() * lhs.getHeight()) / (long) rhs.getWidth() * rhs.getHeight());
        }
    }


    @Override
    public void onWindowFocusChanged(boolean hasFocus)
    {
        super.onWindowFocusChanged(hasFocus);
        View decorView = getWindow().getDecorView();
        if(hasFocus){
            decorView.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                    | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    | View.SYSTEM_UI_FLAG_FULLSCREEN
                    | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            );
        }
    }

    private void closeCamera()
    {
        if(mCameraDevice != null)
        {
            mCameraDevice.close();
            mCameraDevice = null;
        }
    }

    private void startBackgroundThread()
    {
        mBackgroundHandlerThread = new HandlerThread("camea2VideoImage");
        mBackgroundHandlerThread.start();
        log("Thread Started");
        mBackgroundHandler = new Handler(mBackgroundHandlerThread.getLooper());
    }

    private void stopBackgroundThread() throws InterruptedException {
        mBackgroundHandlerThread.quitSafely();
        mBackgroundHandlerThread.join();
        mBackgroundHandlerThread = null;
        mBackgroundHandler = null;
        log("Thread Stopped");
    }

    private static int sensorTodeviceRotation(CameraCharacteristics cameraCharacteristics, int deviceOrientation)
    {
        int sensorOrientation = cameraCharacteristics.get(CameraCharacteristics.SENSOR_ORIENTATION);
        deviceOrientation = ORIENTATIONS.get(deviceOrientation);
        return (sensorOrientation + deviceOrientation +360) % 360;

    }

    private static Size optimalSize(Size[] choices, int width, int height)
    {
        List<Size> bigEnough = new ArrayList<Size>();
        for(Size option : choices)
        {
            if(option.getHeight() == option.getWidth() * height / width &&
            option.getWidth() >= width && option.getHeight() >= height)
            {
                bigEnough.add(option);
            }
        }

        if(bigEnough.size() >0)
        {
            return Collections.min(bigEnough, new CompareSizeByArea());
        }
        else
        {
           return choices[0];
        }
    }

    private void setupCamera(int width, int height) throws CameraAccessException {
        CameraManager cameraManager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);


        for(String cameraID : cameraManager.getCameraIdList())
        {
            CameraCharacteristics cameraCharacteristics = cameraManager.getCameraCharacteristics(cameraID);

            if(cameraCharacteristics.get(CameraCharacteristics.LENS_FACING)==
            CameraCharacteristics.LENS_FACING_BACK)
            {
                continue;
            }

            StreamConfigurationMap map = cameraCharacteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);


            int deviceOrientation = getWindowManager().getDefaultDisplay().getRotation();
            int totalRotation = sensorTodeviceRotation(cameraCharacteristics, deviceOrientation);
            boolean swapRotation = totalRotation == 90 || totalRotation ==270;
            int rotateWidth = width;
            int rotateHeight = height;

            if(swapRotation)
            {
                rotateWidth = height;
                rotateHeight = width;
            }

            mPreviewSize = optimalSize(map.getOutputSizes(SurfaceTexture.class),rotateWidth, rotateHeight);

            mcameraID = cameraID;

            log("Camera ID is: "+cameraID);
            log("Camera ID is: "+cameraID);





            return;

        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        mTextureView = (TextureView) findViewById(R.id.textureView);



        bTakePicture = findViewById(R.id.bCapture);
        bRecording = findViewById(R.id.bRecord);
        nameText = findViewById(R.id.logView);



        bTakePicture.setOnClickListener(this);
        bRecording.setOnClickListener(this);







    }
    @Override
    protected void onResume()
    {
        super.onResume();

        startBackgroundThread();

        if(mTextureView.isAvailable())
        {
            try {
                setupCamera(mTextureView.getWidth(),mTextureView.getHeight());
            } catch (CameraAccessException e) {
                e.printStackTrace();
            }

        }
        else
        {
            mTextureView.setSurfaceTextureListener(mSurfaceTextureListener);
        }

    }
    protected void onPause()
    {
        closeCamera();
        try {
            stopBackgroundThread();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        super.onPause();


    }

    private Executor getExecutor()
    {
        return ContextCompat.getMainExecutor(this);
    }


    private void capturePhoto()
    {
        File photoDir = new File("/storage/emulated/0/DCIM");

        if(!photoDir.exists())
            photoDir.mkdir();

        Date date = new Date();
        String timestamp = String.valueOf(date.getTime());
        String photoFilePath = photoDir.getAbsolutePath()+"/"+timestamp+".png";
        
        File photoFile = new File(photoFilePath);
        File path = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        String path2 = path.toString();
        
        imageCapture.takePicture(
                new ImageCapture.OutputFileOptions.Builder(photoFile).build(),
                getExecutor(),
                new ImageCapture.OnImageSavedCallback() {
                    @Override
                    public void onImageSaved(@NonNull ImageCapture.OutputFileResults outputFileResults) 
                    {
                        Toast.makeText(MainActivity.this, "Photo has been saved succesfully ", Toast.LENGTH_SHORT).show();
                        
                    }

                    @Override
                    public void onError(@NonNull ImageCaptureException exception)
                    {
                        Toast.makeText(MainActivity.this, "Error while saving photo : "+photoFilePath, Toast.LENGTH_SHORT).show();

                    }
                }
        );


    }

    @Override
    public void onClick(View v)
    {
        switch (v.getId())
        {
            case R.id.bCapture:
                capturePhoto();
                break;
            case R.id.bRecord:
                break;
        }



    }

    public void log(String text)
    {
        logList.add(text);

        int range = i;


        for (int i = range; logList.size()>i; i++)
        {
            text2= text2 + "\n" + "[LOG]: "+ logList.get(i);
            range++;

        }

        nameText.setText(text2);
        i++;

    }
}