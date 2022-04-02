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

import android.graphics.SurfaceTexture;
import android.os.Bundle;
import android.os.Environment;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.common.util.concurrent.ListenableFuture;

import java.io.File;
import java.util.ArrayList;
import java.util.Date;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executor;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private ListenableFuture<ProcessCameraProvider> cameraProviderFuture;


    private TextureView mTextureView;

    private TextureView.SurfaceTextureListener mSurfaceTextureListener = new TextureView.SurfaceTextureListener()
    {
        @Override
        public void onSurfaceTextureAvailable(@NonNull SurfaceTexture surface, int width, int height)
        {
            Toast.makeText(MainActivity.this, "Texture view is available", Toast.LENGTH_SHORT).show();
            log("Texture View is available");



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







        cameraProviderFuture = ProcessCameraProvider.getInstance(this);
        cameraProviderFuture.addListener(() -> {
            try {
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();
                startCameraX(cameraProvider);

            }
            catch (ExecutionException e )
            {
                e.printStackTrace();
            }
            catch (InterruptedException e)
            {
                e.printStackTrace();
            }

        }
        ,getExecutor());





    }
    @Override
    protected void onResume()
    {
        super.onResume();

        if(mTextureView.isAvailable())
        {

        }
        else
        {
            mTextureView.setSurfaceTextureListener(mSurfaceTextureListener);
        }

    }

    private Executor getExecutor()
    {
        return ContextCompat.getMainExecutor(this);
    }

    private void startCameraX(ProcessCameraProvider cameraProvider)
    {
        cameraProvider.unbindAll();

        CameraSelector cameraSelector = new CameraSelector.Builder()
                .requireLensFacing(CameraSelector.LENS_FACING_BACK)
                .build();

        Preview preview = new Preview.Builder().build();




        imageCapture = new ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MAXIMIZE_QUALITY)
                .build();

        cameraProvider.bindToLifecycle((LifecycleOwner) this, cameraSelector, preview, imageCapture);


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
        ArrayList<String> logList = new ArrayList<>();
        logList.add(text);

        for (int i = 0; logList.size()>i;i++)
        {
            nameText.setText("\nLog Message: " +logList.get(i));
        }

    }
}