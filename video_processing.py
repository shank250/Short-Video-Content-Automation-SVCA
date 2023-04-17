import os
import json
from moviepy.editor import *
from moviepy.config import change_settings
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
import cv2
import numpy as np
# import conf.py
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})

with open("sample_subtitle.json", "r") as f:
    response = json.load(f)

abs_image_folder_locarion = f'image\\{response["image_instruction"]}'

current_dir = os.getcwd()
image_folder = os.path.join(current_dir, abs_image_folder_locarion)
video_file = f'test{response["title"]}'

image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]
no_of_images = len(image_files)
# script_file = os.path.join(current_dir, 'script\\test.txt')

# 120 word
# 20 words per clip for 10 sec
# 10 words per 5 sec
# 6 words per 3 sec
# 2 words per sec 
# 3 sec break point

# calculating the time for short
words_list = response["script"].split(" ")
total_no_of_words = len(words_list)
avg_words = total_no_of_words // 12
remaining_words = total_no_of_words % 12
# 12 cuts
no_of_cuts = 12
words_utilised_index = 0
for i in range(no_of_cuts) :
    globals()[f"cut{i}"] = []
    cut = globals()[f"cut{i}"]
    if remaining_words != 0 :
        for j in range(avg_words + 1):
            cut.append(words_list[words_utilised_index])
            words_utilised_index += 1
        remaining_words -= 1
    else :
        for j in range(avg_words):
            cut.append(words_list[words_utilised_index])
            words_utilised_index += 1
    globals()[f"cut_text{i}"] = " ".join(cut)
 
# for i in range(no_of_cuts) :
#     cut = globals()[f"cut{i}"]
#     print(len(cut), "\t", cut)


# value = (len(words_list) / 200) * 60
# if value > 60 :
#     video_duration = 60
# elif value < 30 :
#     video_duration = 30
# else:
#     video_duration = value
video_duration = 60
clip_duration = video_duration / no_of_images

clips_list = []
cuts_counter = 0
pixels_left_on_sides_padding = 20
# height = 1080
# width = int(height * 9 / 16)

for i in range(1,7):
    img = image_files[i-1]
    globals()[f"clip{i}"] = ImageClip(image_files[i-1], duration = clip_duration)
    clip = globals()[f"clip{i}"]
    height = clip.size[1]
    width = clip.size[0]
    if width > height: 
        new_height = height
        new_width = int(new_height * 9 / 16)
        print(new_width, width, clip.size[0],clip.size[1],new_height,height )
        clip = clip.crop(x1 = width - new_width - (pixels_left_on_sides_padding/2), x2 = width).resize((new_width, height))
    else:
        new_width = width
        new_height = height 
        clip = clip.resize((width, height))
    
    clip = clip.set_position(lambda t:( t * (width-new_width-pixels_left_on_sides_padding)/clip_duration, 'center') )
    clip = CompositeVideoClip([clip], size=clip.size)
    for j in range(2):
        if j == 0:
            # cuti0
            globals()[f"cut{i}{j}"] = clip.subclip(0, clip_duration / 2)
        else :
            # cuti1
            globals()[f"cut{i}{j}"] = clip.subclip(clip_duration / 2 , clip_duration)
        main_cut = globals()[f"cut{i}{j}"]
        # globals()[f"cut_video_processed{i}{j}.mp4"] = current_dir
        print(current_dir)
        filename = f"cut_video_processed{i}{j}.mp4"
        main_cut.write_videofile(filename  , fps =30, codec="libx264")
        print("done")
        text_clip = VideoFileClip(filename=filename )

        text = globals()[f"cut_text{cuts_counter}"]
        # print(text)
        # print(text_list)
        text_list = text.split(" ")
        n = len(text_list)
        mid = n // 2
        suttitle_line_1_list = text_list[:mid]
        suttitle_line_2_list = text_list[mid:]
        suttitle_line_1_list.append("\n")
        even = 0
        subtitle_text_list = []
        for words in text_list:
                subtitle_text_list.append(words)
                if even%2 == 0:
                    subtitle_text_list.append("\n")
                even += 1
        # print(subtitle_text_list)
        # subtitle_text_list = suttitle_line_1_list + suttitle_line_2_list
        text = " ".join(subtitle_text_list)
        # selecting the color
        # Load image
        img = cv2.imread(img)
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Compute color histogram
        hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
        # Find dominant color(s)
        max_idx = np.argmax(hist)
        hue, sat = np.unravel_index(max_idx, hist.shape)
        # Choose complementary color
        complement_hue = (hue + 90) % 180
        complement_sat = 255 - sat
        complement_val = 255
        # Convert complementary color back to RGB
        complement_hsv = np.array([[complement_hue, complement_sat, complement_val]], dtype=np.uint8)
        complement_rgb = cv2.cvtColor(complement_hsv, cv2.COLOR_HSV2BGR)[0][0]

        text_clip = TextClip(text, fontsize=25, color=complement_rgb ,font = 'Arial-Bold', )
        text_clip = text_clip.set_position("center","center").set_duration(clip_duration/2)
        # print(TextClip.list('font'))
#         subtitle = [((0,2.5)," ".join(suttitle_line_1_list)),
#                     ((2.5, 5)," ".join(suttitle_line_2_list))]
        
#         image_clip = text_clip.to_ImageClip()
# # bg_img=image_clip
#         subtitle_clip = SubtitlesClip(subtitle)
#         subtitle_clip.set_position("center","ceter")
#         # text_clip = SubtitlesClip(subtitle, fontsize=30, align='center' )
        globals()[f"cut_final{i}{j}"] = CompositeVideoClip([main_cut, text_clip]) 
        cuts_counter += 1
        # globals()[f"cut{i}{j}"] = main_cut

    globals()[f"clip{i}"] = concatenate_videoclips([ globals()[f"cut_final{i}0"], globals()[f"cut_final{i}1"] ])

i = 1
video = CompositeVideoClip([globals()[f"clip{i}"],
                            globals()[f"clip{i + 1}"].set_start(10).set_position("center"),
                            globals()[f"clip{i + 2}"].set_start(20).set_position("center"),
                            globals()[f"clip{i + 3}"].set_start(30).set_position("center"),
                            globals()[f"clip{i + 4}"].set_start(40).set_position("center"),
                            globals()[f"clip{i + 5}"].set_start(50).set_position("center")])

# =======================================adding audio============================================
feeling = response["feelings"]
possible_feelings = ["Happiness",
"Sadness",
"Anger",
"Fear",
"Love",
"Excitement",
"Anxiety",
"Frustration"]

for check_feeling in possible_feelings :
    if feeling == check_feeling:
        file_name = f"{feeling}.mp3"
        break
    else:
        file_name = "Excitement.mp3"
audio_file = AudioFileClip(file_name).subclip(0,60)
video_final = video.set_audio(audio_file)
file_name = response["title"]
video_final.write_videofile(f"{file_name}.mp4", fps =30)