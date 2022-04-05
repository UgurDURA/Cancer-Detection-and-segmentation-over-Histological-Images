package com.example.microsphone;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;


public class Gallery_Layout extends AppCompatActivity {

    private Button mainPageButton;
    private TextureView mTextureView;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gallery_layout);
        mainPageButton = findViewById(R.id.bcamera_navigator);

        mTextureView = findViewById(R.id.m2textureView);


        mainPageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                Intent intent = new Intent(Gallery_Layout.this, MainActivity.class);
                startActivity(intent);

            }
        });


    }
}