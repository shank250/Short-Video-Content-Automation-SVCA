from bing_image_downloader import downloader
import json
import os
import cv2
import random, string

def images_extraction(num_of_images = 20):
    with open("sample_subtitle.json", "r") as f:
        response = json.load(f)
    query_string = str(response["tags"])
    downloader.download(query_string, 
                        limit = num_of_images,  
                        output_dir='image', 
                        adult_filter_off=True, 
                        force_replace=False, 
                        timeout=60, verbose=True)

    abs_image_folder_locarion = f'image\\{response["tags"]}'
    current_dir = os.getcwd()
    image_folder = os.path.join(current_dir, abs_image_folder_locarion)
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) ]
    print(image_files)
    i = 1
    no_of_filtered_images = 0
    image_details = {}
    for image_path in image_files:
        img = cv2.imread(image_path)
        try :
            height, width, channels = img.shape
            print(f"image no : {i}")
            aspect_ratio = float(width)/height
            MIN_ASPECT_RATIO = 1.3
            MAX_ASPECT_RATIO  = 2.0
            if aspect_ratio >= MIN_ASPECT_RATIO and aspect_ratio <= MAX_ASPECT_RATIO:
                print("File Size is suitable video generation.")
                print("NO of pixels : ", width*height)
                print("height : ",height ,"width : ",width)
                if height > 600 and width > 16*height/9:
                    # images having h = 600px & w = 1066px more than this are qualified
                    # 1. h : 720px+ and w : 12080px then we will we will resize height and width to 720px and 1280 then crop
                    # 2. h : 600px+ and w : 1066px then we will rezize then crop
                    scale_factor = 760 / img.shape[0]
                    new_width = int(img.shape[1] * scale_factor)
                    resized_img = cv2.resize(img, (new_width, 760), interpolation=cv2.INTER_CUBIC)
                    # resized_img = cv2.resize(img, (int(16*height/9), 720))
                    height_resized, width_resized, channels_resized = resized_img.shape
                    crop_left = int((width_resized - 1280)/2)
                    crop_right = crop_left + 1280
                    croped_img = resized_img[:, crop_left:crop_right]
                    print(f"=======Resized image : {resized_img.shape}============")
                    letters = string.ascii_lowercase
                    current_dir = os.getcwd()
                    img_name = ''.join(random.choice(letters) for i in range(5))
                    abs_image_folder_locarion = f'image_downloads\\{img_name}.jpg'
                    img_path = os.path.join(current_dir, abs_image_folder_locarion)
                    

                    cv2.imwrite(img_path, croped_img)
                    no_of_filtered_images += 1
                    print(no_of_filtered_images, " added sucessfully")
                    if no_of_filtered_images == 6 :
                        print("all 6 images have been imported sucessfully. ")                        
                        break
                else:
                    # deleting other images
                    os.remove(image_path)
                    print(f"Image File no {i} daleted.")
            else:
                print('Image dimensions are not suitable for landscape images.')
                os.remove(image_path)
                print(f"Image File no {i} daleted.")
        except:
            os.remove(image_path)
            print(f"Image File no {i} daleted.")
        i += 1
    if no_of_filtered_images != 6:
        print("retring because less images were filtered")
        image_folder = r'/image_downloads/'
        for filename in os.listdir(image_folder):
            os.remove(os.path.join(image_folder, filename))
        images_extraction(30)
