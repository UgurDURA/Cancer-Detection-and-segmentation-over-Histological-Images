clc
close all
clear all

im1 = imread("10_oppo.jpg"); % read image 
saveas(histogram_extracted(im1,"10 oppo.jpg") ,"h_Result_10_oppo.png"); % call the function and save the results as a .png file

im2 = imread("20_oppo.jpg");
saveas(histogram_extracted(im2, "20 oppo.jpg"),"h_Result_20_oppo.png");

im3 = imread("30_oppo.jpg");
saveas(histogram_extracted(im3, "30 oppo.jpg"),"h_Result_30_oppo.png");

im4 = imread("40_oppo.jpg");
saveas(histogram_extracted(im4, "40 oppo.jpg"),"h_Result_40_oppo.png");

im5 = imread("50_oppo.jpg");
saveas(histogram_extracted(im5, "50 oppo.jpg"),"h_Result_50_oppo.png");

im6 = imread("60_oppo.jpg");
saveas(histogram_extracted(im6, "60 1 oppo.jpg"),"h_Result_60_oppo.png");

im7 = imread("60_2_oppo.jpg");
saveas(histogram_extracted(im7, "60 2 oppo.jpg"),"h_Result_60_2_oppo.png");

im8 = imread("60_3_oppo.jpg");
saveas(histogram_extracted(im8, "60 3 oppo.jpg"),"h_Result_60_3_oppo.png")