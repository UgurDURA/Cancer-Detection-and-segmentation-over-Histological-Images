clc 
clear all
close all

im = imread("pattern.tif");
[r, c] = size(im);

%15*9

new_image = zeros(r*15, c*9);
[r1, c1] = size(new_image);

for i = 1 : r1
    for j = 1 : c1
        pxr = i;
        pxc = j;
        while (pxr > r )
            pxr = pxr - r;
        end
        while (pxc > c)
            pxc = pxc - c;
        end
        new_image(i,j) = im(pxr,pxc);
    end
end
% 
% imshow(uint8(new_image));

imwrite(new_image,"C:\Users\90534\Desktop\4kpattern.tif")

    