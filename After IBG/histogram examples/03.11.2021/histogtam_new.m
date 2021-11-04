clc 
close all
clear all

for i = 1:35

    im = imread(int2str(i)+".png");
    saveas(histogram_extracted(im,"03.11.2021"+ int2str(i) + ".png") ,"03.11.2021_h_"+ int2str(i) + ".png");

end