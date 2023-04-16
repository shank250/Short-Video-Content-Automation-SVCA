from bing_image_downloader import downloader
import json

with open("sample_subtitle.json", "r") as f:
    response = json.load(f)

print(type(response))
query_string = response["image_instruction"]
num_of_images = 6

downloader.download(query_string, 
                    limit = num_of_images,  
                    output_dir='image', 
                    adult_filter_off=True, 
                    force_replace=False, 
                    timeout=60, verbose=True)
