clc
close all
clear

im1 = imread("1,03.png"); 
saveas(nlm(im1, "1,03.png"),"processed_1,03.png");

im2 = imread("2.png"); 
saveas(nlm(im2, "2.png"),"processed_2.png");

im3 = imread("3,05.png"); 
saveas(nlm(im3, "3,05.png"),"processed_3,05.png");

im4 = imread("4,02.png"); 
saveas(nlm(im4, "4,02.png"),"processed_4,02.png");

im5 = imread("4,97.png"); 
saveas(nlm(im5, "4,97.png"),"processed_4,97.png");

im6 = imread("6,13.png"); 
saveas(nlm(im6, "6,13.png"),"processed_6,13.png");

im7 = imread("7,05.png"); 
saveas(nlm(im7, "7,05.png"),"processed_7,05.png");

im8 = imread("8.11.png"); 
saveas(nlm(im8, "8.11.png"),"processed_8.11.png");

im9 = imread("9.png"); 
saveas(nlm(im9, "9.png"),"processed_9.png");

im10 = imread("10.png"); 
saveas(nlm(im10, "10.png"),"processed_10.png");
