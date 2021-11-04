function y = histogram_extracted(im,name) 
% make a function with input rgb image and the name of the image for plot
    
    gray_scaled = rgb2gray(im); % gray scale transition
   
    % my own histogram extracting method (ZOY)
    L = 256; % the gray scale length
    h = zeros(1,L);  % histogram array creation
    [r , c] = size(gray_scaled); % size of the image extraction

    for i = 1 : r % for loop for rows
        for j = 1 : c % for loop for columns 

            px = gray_scaled(i, j); % extracting of pixel value
            h(px + 1) = h(px + 1) + 1; % filling the histogram array

        end
    end

    % built-in image histogram maker
    [counts, gLevels] = imhist(gray_scaled);
    

    y = figure('Position', get(0, 'Screensize')); % make the plot full screen
    sgtitle(name); % title of the plot

    subplot(221); % create subplot
    imshow(im); % fill the first subplot
    title("Imput Image"); % subplot title

    subplot(222); 
    imshow(gray_scaled); % fill the second subplot
    title("Gray Scale Image"); % subplot title

    subplot(223); 
    bar(gLevels, counts); % fill the third subplot
    xlim([0, max(gLevels)]); % x and y axis limits
    ylim([0, max(counts)])
    subtitle("Built-In Histogram Maker"); % subplot title

    subplot(224); 
    stem(h,"*"); % fill the last subplot
    xlim([0, max(gLevels)]); % x and y axis limits
    ylim([0, max(counts)])
    subtitle("My Histogram Maker"); % subplot title
 
end