package com.example.microsphone;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import androidx.core.content.ContextCompat;


import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.ImageFormat;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.CaptureResult;
import android.hardware.camera2.TotalCaptureResult;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.icu.text.SimpleDateFormat;

import android.media.ImageReader;
import android.media.MediaRecorder;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.SystemClock;
import android.util.Size;
import android.util.SparseIntArray;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;
import android.widget.Chronometer;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;

import java.io.IOException;

import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.List;



public class MainActivity extends AppCompatActivity implements View.OnClickListener {


    private static final int REQUEST_CAMERA_PERMISSION_RESULT = 0;
    private static final int REQUEST_WRITE_EXTERNAL_STORAGE_PERMISSION_RESULT = 1;
    private static final int STATE_PREVIEW = 0;
    private static final int STATE_WAIT_LOCK = 1;
    private int mCaptureState = STATE_PREVIEW;
    private static final String IMAGE_FILE_LOCATION = "image_file_location";

    private TextureView mTextureView;
    public static ArrayList<String> logList = new ArrayList<>();
    public static String text2 = "App Started";
    public static int i;
    private String mcameraID;
    private Size mPreviewSize;
    private Size mVideoSize;
    private Size mImageSize;
    private ImageReader mImageReader;

    private ImageView mPhotoCapturedImageView;
    private String mImageFileLocation = "";
    private File mGalleryFolder;
    private static File mImageFile;
    private String GALLERY_LOCATION = "image gallery";

    private File mRawGalleryFolder;
    private static File mRawImageFile;

    private CameraCharacteristics mCameraCharacteristics;

    private Button gallery;




    private final ImageReader.OnImageAvailableListener mOnImageAvailableListener = new ImageReader.OnImageAvailableListener() {
        @Override
        public void onImageAvailable(ImageReader reader)
        {
//            mBackgroundHandler.post(new ImageSaver(mActivity, reader.acquireNextImage(), mUiHandler));

         }
    };
    private MediaRecorder mMediaRecorder;
    private Chronometer mChronometer;
    private HandlerThread mBackgroundHandlerThread;
    private Handler mBackgroundHandler;
    private static SparseIntArray ORIENTATIONS = new SparseIntArray();
    private CaptureRequest.Builder mCaptureRequestBuilder;


    private boolean mIsRecording = false;

    private TextureView.SurfaceTextureListener mSurfaceTextureListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(@NonNull SurfaceTexture surface, int width, int height) {
            Toast.makeText(MainActivity.this, "Texture view is available", Toast.LENGTH_SHORT).show();

            try {
                setupCamera(width, height);
                connectCamera();
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

    Button bTakePicture, bRecording, bSend;
    private TextView nameText, ipText;
    private CameraDevice mCameraDevice;
    EditText sendText;

    private File mVideoFolder;
    private String mVideoFileName;




    private int mTotalRotation;




    private CameraCaptureSession mPreviewCaptureSession;
    private CameraCaptureSession.CaptureCallback mPreviewCaptureCallback = new CameraCaptureSession.CaptureCallback() {

        private void process(CaptureResult captureResult) throws CameraAccessException {
            switch (mCaptureState)
            {
                case STATE_PREVIEW:
                    //Do nothing
                    break;
                case STATE_WAIT_LOCK:
                    mCaptureState = STATE_PREVIEW;
                    Integer afState = captureResult.get(CaptureResult.CONTROL_AF_STATE);
                    if(afState == CaptureResult.CONTROL_AF_STATE_FOCUSED_LOCKED || afState == CaptureResult.CONTROL_AF_STATE_NOT_FOCUSED_LOCKED)
                    {
                        Toast.makeText(getApplicationContext(), "Auto Focus Locked", Toast.LENGTH_SHORT).show();

                    }

                    break;

            }

        }
        @Override
        public void onCaptureCompleted(@NonNull CameraCaptureSession session, @NonNull CaptureRequest request, @NonNull TotalCaptureResult result) {
            super.onCaptureCompleted(session, request, result);
            try {
                process(result);
            } catch (CameraAccessException e) {
                e.printStackTrace();
            }
        }
    };

    private CameraDevice.StateCallback mCameraDeviceStateCallback = new CameraDevice.StateCallback() {
        @Override
        public void onOpened(@NonNull CameraDevice camera)
        {
            mCameraDevice = camera;
            if(mIsRecording)
            {
                try {
                    createVideoFileName();
                    startRecord();
                    mMediaRecorder.start();
                    mChronometer.setBase(SystemClock.elapsedRealtime());
                    mChronometer.setVisibility(View.VISIBLE);
                    mChronometer.start();
                } catch (IOException | CameraAccessException e) {
                    e.printStackTrace();
                }
            }
            else
            {
                try {
                    startPreview();
                } catch (CameraAccessException e) {
                    e.printStackTrace();
                }

            }

        }

        @Override
        public void onDisconnected(@NonNull CameraDevice camera) {
            camera.close();
            mCameraDevice = null;
        }

        @Override
        public void onError(@NonNull CameraDevice camera, int error) {
            camera.close();
            mCameraDevice = null;

        }
    };


    static {
        ORIENTATIONS.append(Surface.ROTATION_0, 0);
        ORIENTATIONS.append(Surface.ROTATION_90, 90);
        ORIENTATIONS.append(Surface.ROTATION_180, 180);
        ORIENTATIONS.append(Surface.ROTATION_270, 270);
    }

    @Override
    public void onClick(View v) {

    }



    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        View decorView = getWindow().getDecorView();
        if (hasFocus) {
            decorView.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                    | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    | View.SYSTEM_UI_FLAG_FULLSCREEN
                    | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            );
        }
    }

    private void closeCamera() {
        if (mCameraDevice != null) {
            mCameraDevice.close();
            mCameraDevice = null;
        }
    }

    private void startBackgroundThread() {
        mBackgroundHandlerThread = new HandlerThread("camera2VideoImage");
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

    private static int sensorTodeviceRotation(CameraCharacteristics cameraCharacteristics, int deviceOrientation) {
        int sensorOrientation = cameraCharacteristics.get(CameraCharacteristics.SENSOR_ORIENTATION);
        deviceOrientation = ORIENTATIONS.get(deviceOrientation);
        return (sensorOrientation + deviceOrientation + 360) % 360;

    }

    private static Size optimalSize(Size[] choices, int width, int height) {
        List<Size> bigEnough = new ArrayList<Size>();
        for (Size option : choices) {
            if (option.getHeight() == option.getWidth() * height / width &&
                    option.getWidth() >= width && option.getHeight() >= height) {
                bigEnough.add(option);
            }
        }

        if (bigEnough.size() > 0) {
            return Collections.min(bigEnough, new CompareSizeByArea());
        } else {
            return choices[0];
        }
    }

    private void setupCamera(int width, int height) throws CameraAccessException {
        CameraManager cameraManager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);

        String[] cameraIds =  cameraManager.getCameraIdList();
        for (int i = 0; i <cameraIds.length;i++){
            log(cameraIds[i]);
        }

        for (String cameraID : cameraManager.getCameraIdList()) {
            CameraCharacteristics cameraCharacteristics = cameraManager.getCameraCharacteristics(cameraID);

                int b = cameraCharacteristics.get(CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL);


            if (cameraCharacteristics.get(CameraCharacteristics.LENS_FACING) ==
                    CameraCharacteristics.LENS_FACING_FRONT) {
                continue;
            }

            StreamConfigurationMap map = cameraCharacteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);


            int deviceOrientation = getWindowManager().getDefaultDisplay().getRotation();
            mTotalRotation = sensorTodeviceRotation(cameraCharacteristics, deviceOrientation);
            boolean swapRotation = mTotalRotation  == 90 || mTotalRotation == 270;
            int rotateWidth = width;
            int rotateHeight = height;

            if (swapRotation) {
                rotateWidth = height;
                rotateHeight = width;
            }

            mPreviewSize = optimalSize(map.getOutputSizes(SurfaceTexture.class), rotateWidth, rotateHeight);
            mVideoSize = optimalSize(map.getOutputSizes(MediaRecorder.class), rotateWidth, rotateHeight);

            mImageSize = optimalSize(map.getOutputSizes(ImageFormat.JPEG), rotateWidth, rotateHeight);
            mImageReader = mImageReader.newInstance(mImageSize.getWidth(), mImageSize.getHeight(), ImageFormat.JPEG,1);

            mImageReader.setOnImageAvailableListener(mOnImageAvailableListener, mBackgroundHandler);
            mPreviewSize = optimalSize(map.getOutputSizes(SurfaceTexture.class), width, height);

            mcameraID = "0"; //Manually provided camera ID

            mCameraCharacteristics = cameraCharacteristics;

            log("Current Camera ID is: " + mcameraID);
            log("Camera ID is: " + cameraID);
            log("Device Camera Hardware Level: " + b);
            return;
        }
    }

    private void connectCamera() {
        CameraManager cameraManager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);

        try {
            if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M)
            {
                if(ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)==
                PackageManager.PERMISSION_GRANTED)
                {
                    cameraManager.openCamera(mcameraID, mCameraDeviceStateCallback, mBackgroundHandler);

                }
                else
                {
                    if(shouldShowRequestPermissionRationale(Manifest.permission.CAMERA))
                    {
                        Toast.makeText(this,"MicrosPhone requires to access to Camera",Toast.LENGTH_SHORT).show();
                    }
                    requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_PERMISSION_RESULT);

                }

            }
            else {
                cameraManager.openCamera(mcameraID, mCameraDeviceStateCallback, mBackgroundHandler);

            }
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void startRecord() throws IOException, CameraAccessException {
        setupMediaRecorder();
        SurfaceTexture surfaceTexture = mTextureView.getSurfaceTexture();
        surfaceTexture.setDefaultBufferSize(mPreviewSize.getWidth(),mPreviewSize.getHeight());
        Surface previewSurface = new Surface(surfaceTexture);
        Surface recordSurface = mMediaRecorder.getSurface();
        mCaptureRequestBuilder = mCameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_RECORD);
        mCaptureRequestBuilder.addTarget(previewSurface);
        mCaptureRequestBuilder.addTarget(recordSurface);

        mCameraDevice.createCaptureSession(Arrays.asList(previewSurface, recordSurface),
                new CameraCaptureSession.StateCallback() {
                    @Override
                    public void onConfigured(@NonNull CameraCaptureSession session)
                    {
                        try {
                            session.setRepeatingRequest(
                                    mCaptureRequestBuilder.build(),null,null
                            );
                        } catch (CameraAccessException e) {
                            e.printStackTrace();
                        }


                    }

                    @Override
                    public void onConfigureFailed(@NonNull CameraCaptureSession session) {

                    }
                },null);

    }

    private void startPreview() throws CameraAccessException {
        SurfaceTexture surfaceTexture = mTextureView.getSurfaceTexture();
        surfaceTexture.setDefaultBufferSize(mPreviewSize.getWidth(),mPreviewSize.getHeight());
        Surface previewSurface = new Surface(surfaceTexture);

        mCaptureRequestBuilder = mCameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);
        mCaptureRequestBuilder.addTarget(previewSurface); //Check this part

        mCameraDevice.createCaptureSession(Arrays.asList(previewSurface, mImageReader.getSurface()),
                new CameraCaptureSession.StateCallback() {
                    @Override
                    public void onConfigured(@NonNull CameraCaptureSession session)
                    {
                        mPreviewCaptureSession = session;
                        try {
                            mPreviewCaptureSession.setRepeatingRequest(mCaptureRequestBuilder.build(),  //Use this part for UDP
                                    null, mBackgroundHandler);
                        } catch (CameraAccessException e) {
                            e.printStackTrace();
                        }

                    }

                    @Override
                    public void onConfigureFailed(@NonNull CameraCaptureSession session)
                    {
                        Toast.makeText(getApplicationContext(), "Unable to setup Cameraview on Texture view", Toast.LENGTH_SHORT).show();

                    }
                }, null);

    }







    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        gallery = findViewById(R.id.bGallery);

        gallery.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                Intent intent = new Intent(MainActivity.this, Gallery_Layout.class);
                startActivity(intent);
            }
        });


        createVideoFolder();
        createImageGallery();


        mMediaRecorder = new MediaRecorder();




        mTextureView = (TextureView) findViewById(R.id.textureView);
        bTakePicture = findViewById(R.id.bCapture);
        mChronometer = (Chronometer) findViewById(R.id.chronometer);
        bRecording = findViewById(R.id.bRecord);
        nameText = findViewById(R.id.logView);
        bSend = findViewById(R.id.bSend);
        sendText = (EditText) findViewById(R.id.textMessage);
        ipText = (TextView) findViewById(R.id.ipText);



        bTakePicture.setBackgroundColor(Color.BLUE);
        bRecording.setBackgroundColor(Color.BLUE);

        bSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SocketToPc send = new SocketToPc();
                send.execute(sendText.getText().toString());
            }
        });

        bRecording.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                if(mIsRecording)
                {
                    mChronometer.stop();
                    mChronometer.setVisibility(View.INVISIBLE);
                    mIsRecording = false;
                    bRecording.setBackgroundColor(Color.BLUE);
                    mMediaRecorder.stop();
                    mMediaRecorder.reset();
                    try {
                        startPreview();
                    } catch (CameraAccessException e) {
                        e.printStackTrace();
                    }
                }

                else
                {
                    try {
                        checkWritePermission();
                    } catch (IOException | CameraAccessException e) {
                        e.printStackTrace();
                    }

                }

            }
        });

        bTakePicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    lockFocus();
                } catch (CameraAccessException e) {
                    e.printStackTrace();
                }
            }
        });

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
                connectCamera();
            } catch (CameraAccessException e) {
                e.printStackTrace();
            }

        }
        else
        {
            mTextureView.setSurfaceTextureListener(mSurfaceTextureListener);
        }

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if(requestCode == REQUEST_CAMERA_PERMISSION_RESULT)
        {
            if(grantResults[0] != PackageManager.PERMISSION_GRANTED)
            {
                Toast.makeText(getApplicationContext(),"Application will not run without camera services",Toast.LENGTH_SHORT).show();
                log("Application requires camera permission");
            }
        }
        if (requestCode == REQUEST_WRITE_EXTERNAL_STORAGE_PERMISSION_RESULT)
        {
            if(grantResults[0] == PackageManager.PERMISSION_GRANTED)
            {
                Toast.makeText(getApplicationContext(),"Application will not run without external storage access",Toast.LENGTH_SHORT).show();
                log("Application requires storage access permission");

                mIsRecording = true;
                bRecording.setBackgroundColor(Color.RED);
                log("External storage access permission succesfully granted");


                try {
                    createVideoFileName();
                } catch (IOException e) {
                    e.printStackTrace();
                }




            }
            else
            {
                log("App requires storage permission ");
            }
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


    private void createVideoFolder()
    {
        File movieFile = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES);

        mVideoFolder = new File(movieFile, "MicrosPhone_Videos");

        if(!mVideoFolder.exists())
        {
            mVideoFolder.mkdirs();
        }
    }

    private File createVideoFileName() throws IOException {
        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String prepend = "VIDEO_"+timestamp + "_" ;
        File videoFile = File.createTempFile(prepend, ".mp4",mVideoFolder);
        mVideoFileName = videoFile.getAbsolutePath();
        return videoFile;

    }


    private void checkWritePermission() throws IOException, CameraAccessException {
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M)
        {
            if(ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
            == PackageManager.PERMISSION_GRANTED)
            {
                mIsRecording = true;
                bRecording.setBackgroundColor(Color.RED);
                createVideoFileName();
                startRecord();
                mMediaRecorder.start();
                mChronometer.setBase(SystemClock.elapsedRealtime());
                mChronometer.setVisibility(View.VISIBLE);
                mChronometer.start();


            }
            else
            {
                if(shouldShowRequestPermissionRationale(Manifest.permission.WRITE_EXTERNAL_STORAGE))
                {
                    Toast.makeText(this, "App needs to be able to access save storage", Toast.LENGTH_SHORT).show();
                }
                requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},REQUEST_WRITE_EXTERNAL_STORAGE_PERMISSION_RESULT);
            }
        }
        else
        {
            mIsRecording = true;
            bRecording.setBackgroundColor(Color.RED);
            createVideoFileName();
            startRecord();

            mMediaRecorder.start();
            mChronometer.setBase(SystemClock.elapsedRealtime());
            mChronometer.setVisibility(View.VISIBLE);
            mChronometer.start();

        }
    }

    private void setupMediaRecorder() throws IOException {
        mMediaRecorder.setVideoSource(MediaRecorder.VideoSource.SURFACE);
        mMediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
        mMediaRecorder.setOutputFile(mVideoFileName);
        mMediaRecorder.setVideoEncodingBitRate(10000000);
        mMediaRecorder.setVideoFrameRate(30);
        mMediaRecorder.setVideoSize(mVideoSize.getWidth(), mVideoSize.getHeight());
        mMediaRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);
        mMediaRecorder.setOrientationHint(mTotalRotation);
        mMediaRecorder.prepare();
    }

    private void lockFocus() throws CameraAccessException
    {
        mCaptureState = STATE_WAIT_LOCK;
        mCaptureRequestBuilder.set(CaptureRequest.CONTROL_AF_TRIGGER,CaptureRequest.CONTROL_AF_TRIGGER_START); //Check for zoom
        mPreviewCaptureSession.capture(mCaptureRequestBuilder.build(), mPreviewCaptureCallback, mBackgroundHandler);//Check for UDO
    }

    private static class CompareSizeByArea implements Comparator<Size> {
        @Override
        public int compare(Size lhs, Size rhs) {
            return (int) (Long.signum((long) lhs.getWidth() * lhs.getHeight()) / (long) rhs.getWidth() * rhs.getHeight());
        }
    }


    private static Boolean cotains(int[] modes, int mode)
    {
        if(modes == null)
        {
            return false;
        }
        for(int i : modes)
        {
            if(i == mode)
            {
                return true;
            }
        }
        return false;
    }

    private void createImageGallery()
    {
        File storageDirectory = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
        mGalleryFolder = new File(storageDirectory, "JPEG Images");
        mRawGalleryFolder = new File(storageDirectory, "Raw Images");
        if(!mGalleryFolder.exists())
        {
            mGalleryFolder.mkdirs();
        }
        if(!mRawGalleryFolder.exists())
        {
            mRawGalleryFolder.mkdirs();
        }


    }

    File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_"+timeStamp+"_";

        File image = File.createTempFile(imageFileName, ".jpg", mGalleryFolder);
        return image;
    }

    File createRawImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "RAW_"+timeStamp+"_";

        File image = File.createTempFile(imageFileName, ".dng", mRawGalleryFolder);
        return image;
    }


    public void send( View view)
    {
        SocketToPc send = new SocketToPc();
        send.execute(sendText.getText().toString());

    }

    class SocketToPc extends AsyncTask <String, Void, String>
    {


        @Override
        protected String doInBackground(String... strings)
        {
            Socket msocket;
            InputStreamReader minputStreamReader;
            BufferedReader mBufferReader;
            PrintWriter mprintWriter;
            String result;

            try
            {
                msocket = new Socket("192.168.1.8",5555);
                minputStreamReader = new InputStreamReader(msocket.getInputStream());
                mBufferReader = new BufferedReader(minputStreamReader);

                mprintWriter = new PrintWriter(msocket.getOutputStream());

                mprintWriter.println(strings[0]);
                mprintWriter.flush();

                result = mBufferReader.readLine();

                return result;
            } catch (Exception e) {
                e.printStackTrace();
                return "anan";
            }



        }

        @Override
        protected void onPostExecute(String s)
        {
            super.onPostExecute(s);
            ipText.setText(s);
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