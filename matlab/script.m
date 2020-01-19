cam = webcam(1);
% cam = videoinput('macvideo',1);
w = preview(cam);
static_image = snapshot(cam);

while 1
    img = snapshot(cam);
    
    r = round(mean(mean(img(:,:,1))));
    
    gray = rgb2gray(img);
    bw = imbinarize(gray);
    
    red     = img(:,:,1)>180;
    green   = img(:,:,2)<100;
    blue    = img(:,:,3)<100;
    
    mask = red.*green.*blue;
    
    red_filter = uint8(mask).*img;
    
    cloak = img - red_filter + static_image.*uint8(mask);
    
%     imshow(img);
%     imshow(gray);
%     imshow(bw);
%     imshow(mask);
    imshow(cloak);
    
    if ishghandle(w) ~= 1
        break;
    end
end

closePreview(cam);
close all;
clear cam;
