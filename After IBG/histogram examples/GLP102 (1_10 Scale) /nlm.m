function y = nlm(im,name) 
% make a function with input rgb image and the name of the image for plot
    
    gray_im = rgb2gray(im); % gray scale transition
   
    
    nlm_im = imnlmfilt(gray_im); % non-local means filtered image
    histeq_im = histeq(nlm_im);
    % built-in image histogram maker
    [counts,gLevels] = imhist(gray_im);
    [c2, g2] = imhist(nlm_im); % nlm image histogram
    [c3, g3] = imhist(histeq_im);

    y = figure('Position', get(0, 'Screensize')); % make the plot full screen
    sgtitle(name); % title of the plot

    subplot(231); 
    imshow(gray_im); 
    title("Input"); 

    subplot(232); 
    imshow(nlm_im); 
    title("Output - Non-local means"); 
    
    subplot(233); 
    imshow(histeq_im); 
    title("Output - Histogram Equalization"); 

    subplot(234); 
    bar(gLevels, counts); 
    xlim([0, max(gLevels)]); 
    ylim([0, max(counts)])
    subtitle("Input Histogram");
    
    subplot(235); 
    bar(g2,c2); 
    xlim([0, max(g2)]);
    ylim([0, max(c2)])
    subtitle("Non-local Means Histogram"); 
    
    subplot(236); 
    bar(g3,c3); 
    xlim([0, max(g3)]);
    ylim([0, max(c3)])
    subtitle("Histeq Histogram"); 

end
