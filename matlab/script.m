cam = webcam(1);

w = preview(cam);
static_image = snapshot(cam);
 
% define color here in hsv
h = 0.66;
s = 0.3;
v = 0.3;

while 1
    img = snapshot(cam);

    hsv_img = rgb2hsv(img);

    lower_h     = hsv_img(:,:,1)>(h-0.1);
    lower_s     = hsv_img(:,:,2)>s;
    lower_v     = hsv_img(:,:,3)>v;

    upper_h     = hsv_img(:,:,1)<(h+0.1);

    mask_h = lower_h.*upper_h;
    mask_s = lower_s;
    mask_v = lower_v;
    
    mask = mask_h.*mask_s.*mask_v;
    
    filter = uint8(mask).*img;

    cloak = img - filter + static_image.*uint8(mask);

%     imshow(filter);
%     imshow(mask);
%     imshow(mask_h);
%     imshow(mask_s);
%     imshow(mask_v);

    imshow(cloak);

    if ishghandle(w) ~= 1
        break;
    end
end

closePreview(cam);
close all;
clear all;