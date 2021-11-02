clc
close all
clear all

im1 = imread("glp102_192_1.png"); % read image 
saveas(histogram_extracted(im1,"glp102 192 1.png") ,"h_Result_glp102_192_1.png"); % call the function and save the results as a .png file

im2 = imread("glp102_192_2.png");  
saveas(histogram_extracted(im2,"glp102 192 2.png") ,"h_Result_glp102_192_2.png");

im3 = imread("glp102_192_3.png"); 
saveas(histogram_extracted(im3,"glp102 192 3.png") ,"h_Result_glp102_192_3.png");

im4 = imread("glp102_192_4.png");  
saveas(histogram_extracted(im4,"glp102 192 4.png") ,"h_Result_glp102_192_4.png");

im5 = imread("glp102_192_5.png");  
saveas(histogram_extracted(im5,"glp102 192 5.png") ,"h_Result_glp102_192_5.png");

im6 = imread("glp102_192_6.png");  
saveas(histogram_extracted(im6,"glp102 192 6.png") ,"h_Result_glp102_192_6.png");

im7 = imread("glp102_192_7.png");
saveas(histogram_extracted(im7,"glp102 192 7.png") ,"h_Result_glp102_192_7.png");

im8 = imread("glp102_192_8.png"); 
saveas(histogram_extracted(im8,"glp102 192 8.png") ,"h_Result_glp102_192_8.png");

im9 = imread("glp102_192_9.png"); 
saveas(histogram_extracted(im9,"glp102 192 9.png") ,"h_Result_glp102_192_9.png");

im10 = imread("glp102_192_10.png");  
saveas(histogram_extracted(im10,"glp102 192 10.png") ,"h_Result_glp102_192_10.png");
