%------------------------------------------------------------------%
%This function is used for extract the region of interest 
%This function get rid of the background of the identification card 
%------------------------------------------------------------------%



function [croppedImage] = region_Extraction(imageDestination)
    rgbImage = imread(imageDestination);
    hsvImg=rgb2hsv(rgbImage);
    s = hsvImg(:,:,2);
    foreground = s > 0.2; % Or whatever.
    foreground = bwareaopen(foreground, 1000); % or whatever.
    labeledImage = bwlabel(foreground);
    measurements = regionprops(labeledImage, 'BoundingBox');
    bb = measurements.BoundingBox;
    croppedImage = imcrop(rgbImage, bb);
    imwrite(croppedImage,'E:\4th year 2nd\research\FDDS\Image\source.jpg');
end


