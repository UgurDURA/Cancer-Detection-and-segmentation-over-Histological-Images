clc
close all
clear all

im1 = imread("h_918_1.png"); % read image 
saveas(histogram_extracted(im1,"h 918 1.png") ,"h_Result_h_918_1.png"); % call the function and save the results as a .png file

im2 = imread("h_918_2.png");
saveas(histogram_extracted(im2, "h 918 2.png"),"h_Result_h_918_2.png");

im3 = imread("h_918_3.png");
saveas(histogram_extracted(im3, "h 918 3.png"),"h_Result_h_918_3.png");

im4 = imread("h_918_4.png");
saveas(histogram_extracted(im4, "h 918 4.png"),"h_Result_h_918_4.png");

im5 = imread("h_918_5.png");
saveas(histogram_extracted(im5, "h 918 5.png"),"h_Result_h_918_5.png");

im6 = imread("h_918_6.png");
saveas(histogram_extracted(im6, "h 918 6.png"),"h_Result_h_918_6.png");

im7 = imread("h_918_7.png");
saveas(histogram_extracted(im7, "h 918 7.png"),"h_Result_h_918_7.png");

im8 = imread("h_918_8.png");
saveas(histogram_extracted(im8, "h 918 8.png"),"h_Result_h_918_8.png");

im9 = imread("h_918_9.png");
saveas(histogram_extracted(im9, "h 918 9.png"),"h_Result_h_918_9.png");

im10 = imread("h_918_10.png");
saveas(histogram_extracted(im10, "h 918 10.png"),"h_Result_h_918_10.png");

im11 = imread("h_918_11.png");
saveas(histogram_extracted(im11, "h 918 11.png"),"h_Result_h_918_11.png");