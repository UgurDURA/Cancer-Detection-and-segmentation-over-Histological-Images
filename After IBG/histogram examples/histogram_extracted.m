function y = histogram_extracted(im,name)
    
    % gray scale transition
    gray_scaled = rgb2gray(im);
   
    % my own histogram extracting method
    
    L = 256; % the gray scale length
    h = zeros(1,L);  %
    [r , c] = size(gray_scaled);

    for i = 1 : r
        for j = 1 : c
            px = gray_scaled(i, j);
            h(px + 1) = h(px + 1) + 1;
        end
    end

    % built-in image histogram maker
    [counts, gLevels] = imhist(gray_scaled);
    

    y = figure('Position', get(0, 'Screensize'));
    sgtitle(name);

    subplot(221); 
    imshow(im); 
    title("Imput Image");

    subplot(222); 
    imshow(gray_scaled);
    title("Gray Scale Image");

    subplot(223); 
    bar(gLevels, counts); 
    xlim([0, max(gLevels)]);
    ylim([0, max(counts)])
    subtitle("Built-In Histogram Maker");

    subplot(224); 
    stem(h,"*"); 
    xlim([0, max(gLevels)]);
    ylim([0, max(counts)])
    subtitle("My Histogram Maker");
 
end