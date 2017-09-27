function kurtosis_val = kurtosis_score( imgdestination )
    img = imread(imgdestination);
    kurtosis_input = double(img);
    kurtosis_val = kurtosis(kurtosis_input(:));

end

