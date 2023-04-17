import os
import json
current_dir = os.getcwd()
print(current_dir)
# with open("sample_subtitle.json", "r") as f:
#     response = json.load(f)
u = '\\image'
all_images = os.path.join(current_dir, u)
# abs_image_folder_locarion = f'image\\{response["image_instruction"]}'
# image_folder = os.path.join(current_dir, abs_image_folder_locarion)
for filename in os.listdir(current_dir):
    if filename.endswith('.mp4'):
        os.remove(os.path.join(current_dir, filename))
    elif filename.endswith('.json'):
        os.remove(os.path.join(current_dir, filename))
# for filename_jpg in os.listdir(image_folder):
#     if filename_jpg.endswith('.jpg'):
#         os.remove(os.path.join(image_folder, filename_jpg))
for folder in os.listdir(all_images):
    os.remove(os.path.join(all_images, folder))
    
