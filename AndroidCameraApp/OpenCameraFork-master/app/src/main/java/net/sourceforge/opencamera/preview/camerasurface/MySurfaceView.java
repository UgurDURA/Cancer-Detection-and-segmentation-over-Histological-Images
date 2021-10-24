package net.sourceforge.opencamera.preview.camerasurface;

import net.sourceforge.opencamera.MyDebug;
import net.sourceforge.opencamera.cameracontroller.CameraController;
import net.sourceforge.opencamera.cameracontroller.CameraControllerException;
import net.sourceforge.opencamera.preview.Preview;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.media.MediaRecorder;
import android.os.Handler;
import android.util.Log;
import android.view.MotionEvent;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

/** Provides support for the surface used for the preview, using a SurfaceView.
 */
public class MySurfaceView extends SurfaceView implements CameraSurface {
    private static final String TAG = "MySurfaceView";

    private final Preview preview;
    private final int [] measure_spec = new int[2];
    private final Handler handler = new Handler();
    private final Runnable tick;

    public
    MySurfaceView(Context context, final Preview preview) {
        super(context);
        this.preview = preview;
        if( MyDebug.LOG ) {
            Log.d(TAG, "new MySurfaceView");
        }

        // Install a SurfaceHolder.Callback so we get notified when the
        // underlying surface is created and destroyed.
        getHolder().addCallback(preview);
        // deprecated setting, but required on Android versions prior to 3.0
        //getHolder().setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS); // deprecated

        tick = new Runnable() {
            public void run() {
				/*if( MyDebug.LOG )
					Log.d(TAG, "invalidate()");*/
                preview.test_ticker_called = true;
                invalidate();
                handler.postDelayed(this, preview.getFrameRate());
            }
        };
    }

     public class MyServerFeeder implements Runnable
     {
         ServerSocket ss;
         Socket s;
         DataInputStream dis;
         int len;
         byte[] data;


         @Override
         public void run() {


                 try {
                     ss = new ServerSocket(9999);
                 } catch (IOException e) {
                     e.printStackTrace();
                 }
                 handler.post(()->
                 {
                     Toast.makeText(getContext().getApplicationContext(), "Listening", Toast.LENGTH_LONG).show();
                 });

                 while(true)
                 {
                     try {
                         s = ss.accept();
                     } catch (IOException e) {
                         e.printStackTrace();
                     }
                     InputStream in = null;
                     try {
                         in = s.getInputStream();
                     } catch (IOException e) {
                         e.printStackTrace();
                     }
                     dis = new DataInputStream(in);

                     try {
                         len = dis.readInt();
                     } catch (IOException e) {
                         e.printStackTrace();
                     }
                     data = new byte[len];
                     if(len > 0)
                     {
                         try {
                             dis.readFully(data, 0, data.length);
                         } catch (IOException e) {
                             e.printStackTrace();
                         }

                     }
                 }
             }

         }
     }

    @Override
    public View getView() {
        return this;
    }

    @Override
    public void setPreviewDisplay(CameraController camera_controller) {
        if( MyDebug.LOG )
            Log.d(TAG, "setPreviewDisplay");
        try {
            camera_controller.setPreviewDisplay(this.getHolder());
        }
        catch(CameraControllerException e) {
            if( MyDebug.LOG )
                Log.e(TAG, "Failed to set preview display: " + e.getMessage());
            e.printStackTrace();
        }
    }

    @Override
    public void setVideoRecorder(MediaRecorder video_recorder) {
        video_recorder.setPreviewDisplay(this.getHolder().getSurface());
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        return preview.touchEvent(event);
    }

    @Override
    public void onDraw(Canvas canvas) {
        preview.draw(canvas);
    }

    @Override
    protected void onMeasure(int widthSpec, int heightSpec) {
        if( MyDebug.LOG )
            Log.d(TAG, "onMeasure: " + widthSpec + " x " + heightSpec);
        preview.getMeasureSpec(measure_spec, widthSpec, heightSpec);
        super.onMeasure(measure_spec[0], measure_spec[1]);
    }

    @Override
    public void setTransform(Matrix matrix) {
        if( MyDebug.LOG )
            Log.d(TAG, "setting transforms not supported for MySurfaceView");
        throw new RuntimeException();
    }

    @Override
    public void onPause() {
        if( MyDebug.LOG )
            Log.d(TAG, "onPause()");
        handler.removeCallbacks(tick);
    }

    @Override
    public void onResume() {
        if( MyDebug.LOG )
            Log.d(TAG, "onResume()");
        tick.run();
    }
}
