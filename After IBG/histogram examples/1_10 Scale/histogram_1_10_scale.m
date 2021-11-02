clc
close all
clear all

im1 = imread("1,03.png"); % read image 
saveas(histogram_extracted(im1,"1,03.png") ,"h_Result_1,03.png"); % call the function and save the results as a .png file

im2 = imread("2.png");
saveas(histogram_extracted(im2, "2.png"),"h_Result_2.png");

im3 = imread("3,05.png");
saveas(histogram_extracted(im3, "3,05.png"),"h_Result_3,05.png");

im4 = imread("4,02.png");
saveas(histogram_extracted(im4, "4,02.png"),"h_Result_4,02.png");

im5 = imread("4,97.png");
saveas(histogram_extracted(im5, "4,97.png"),"h_Result_4,97.png");

im6 = imread("6,13.png");
saveas(histogram_extracted(im6, "6,13.png"),"h_Result_6,13.png");

im7 = imread("7,05.png");
saveas(histogram_extracted(im7, "7,05.png"),"h_Result_7,05.png");

im8 = imread("8.11.png");
saveas(histogram_extracted(im8, "8.11.png"),"h_Result_8.11.png");

im9 = imread("9.png");
saveas(histogram_extracted(im9, "img 9.png"),"h_Result_9.png");

im10 = imread("10.png");
saveas(histogram_extracted(im10, "10.png"),"h_Result_10.png");