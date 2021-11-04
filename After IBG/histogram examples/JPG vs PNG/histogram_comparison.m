clear all
close all
clc

im1 = imread("50x.jpg");
im2 = imread("5_10x.png");

gray_scaled = rgb2gray(im1);
gray_scaled1 = rgb2gray(im2);

L = 256; % the gray scale length
h = zeros(1,L);  % histogram array creation
h1 = zeros(1,L);  % histogram array creation

[r , c] = size(gray_scaled); % size of the image extraction
[r2 , c2] = size(gray_scaled1); % size of the image extraction


    for i = 1 : r % for loop for rows
        for j = 1 : c % for loop for columns 

            px = gray_scaled(i, j); % extracting of pixel value
            h(px + 1) = h(px + 1) + 1; % filling the histogram array

        end
    end

    for i = 1 : r2 % for loop for rows
        for j = 1 : c2 % for loop for columns 

            px = gray_scaled1(i, j); % extracting of pixel value
            h1(px + 1) = h1(px + 1) + 1; % filling the histogram array

        end
    end

    subplot(221); % create subplot    
    imshow(gray_scaled); % fill the second subplot
    title("Gray Scale Image_jpg"); % subplot title


    subplot(222); 
    stem(h,"*"); % fill the last subplot
    subtitle("My Histogram Maker"); % subplot title

    subplot(223); 
    imshow(gray_scaled1); % fill the second subplot
    title("Gray Scale Image _ png"); % subplot title

    subplot(224); 
    stem(h1,"*"); % fill the last subplot
    subtitle("My Histogram Maker"); % subplot title