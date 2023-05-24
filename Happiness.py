import os
import json
from moviepy.editor import *
from moviepy.config import change_settings
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
import cv2
import numpy as np
# import conf.py
import random
import string
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})

def video_generation(): 
    global video_file_name;

    # -----------------subtitle----------------------
    global file_name
    

    with open("sample_subtitle.json", "r") as f:
        response = json.load(f)
    current_dir = os.getcwd()
    abs_image_folder_locarion = r'image_downloads'
    image_folder = os.path.join(current_dir, abs_image_folder_locarion)

    # abs_image_folder_locarion = f'image\\{response["tags"]}'

    current_dir = os.getcwd()
    image_folder = os.path.join(current_dir, abs_image_folder_locarion)
    video_file = f'test{response["title"]}'

    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) ]
    # if f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.png') or f.endswith('.PNG')or f.endswith('.jpeg') or f.endswith('.JPEG')
    no_of_images = len(image_files)

    # 120 word
    # 20 words per clip for 10 sec
    # 10 words per 5 sec
    # 6 words per 3 sec
    # 2 words per sec 
    # 3 sec break point
    # 12 cuts

    # calculating the time for short
    words_list = response["script"].split(" ")
    total_no_of_words = len(words_list)
    avg_words = total_no_of_words // 12
    remaining_words = total_no_of_words % 12
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
    print(len(image_files))
    # ------------------image clips 1-6-----------------------
    for i in range(1,7):
        current_image_file_path = image_files[i-1]
        globals()[f"clip{i}"] = ImageClip(current_image_file_path, duration = clip_duration)
        clip = globals()[f"clip{i}"]
        height = clip.size[1]
        width = clip.size[0]
        new_height = height
        new_width = int(new_height * 9 / 16)
        clip = clip.set_position(lambda t:( t * (width-new_width-pixels_left_on_sides_padding)/clip_duration, 'center') )
        clip = CompositeVideoClip([clip], size=clip.size)
        if width > height: 
            new_height = height
            new_width = int(new_height * 9 / 16)
            print(new_width, width, clip.size[0],clip.size[1],new_height,height )
            clip = clip.crop(x1 = width - new_width - (pixels_left_on_sides_padding/2), x2 = width).resize((new_width, height))
        else:
            clip = clip.resize((width, height))
            new_height = height
            new_width = int(new_height * 9 / 16)

        # ========================textclip color selection=================================
        try:
            img = ImageClip(current_image_file_path)
            most_common_color = img.get_average_color()
            opposite_color = tuple(255 - c for c in most_common_color)
        except:
            opposite_color = "grey"
        print(opposite_color)
                # ==================
        x1, y1 = 0, 540
        x2, y2 = 450, 760

        # Create a black clip with the specified size
        rect_clip = ColorClip(size=(x2-x1, y2-y1), color=(0, 0, 0))

        # Set the opacity of the clip to 0.5 (50% transparent)
        rect_clip = rect_clip.set_opacity(0.5)

        # Create a CompositeVideoClip with the rectangle clip positioned at (x1, y1)
        clip = CompositeVideoClip([clip, rect_clip.set_pos((x1, y1))])
    # ----------------------------------adding subtitle-------------------------------------
        for j in range(2):
            if j == 0:
                # cuti0
                globals()[f"cut{i}{j}"] = clip.subclip(0, clip_duration / 2)
            else :
                # cuti1
                globals()[f"cut{i}{j}"] = clip.subclip(clip_duration / 2 , clip_duration)
            main_cut = globals()[f"cut{i}{j}"]
            print(current_dir)
            filename = f"cut_video_processed{i}{j}.mp4"
            main_cut.write_videofile(filename  , fps =30, codec="libx264")
            print("done")





            # ==================
            text_clip = VideoFileClip(filename=filename )
            text = globals()[f"cut_text{cuts_counter}"]
            text_list = text.split(" ")
            n = len(text_list)
            mid = n // 2
            suttitle_line_1_list = text_list[:mid]
            suttitle_line_2_list = text_list[mid:]
            suttitle_line_1_list.append("\n")
            suttitle_line_2_list.append("...")
            subtitle_text_list = suttitle_line_1_list + suttitle_line_2_list

            #//////////////// older logic with 2 words////////////////////
            # even = 0
            # for words in text_list:
            #         subtitle_text_list.append(words)
            #         if even%2 == 0:
            #             subtitle_text_list.append("\n")
            #         even += 1
            text = " ".join(subtitle_text_list)
            try:
                text_clip = TextClip(text, fontsize=23, color="white" ,font = 'Arial-Bold', stroke_color = "yellow", stroke_width = 1 )
            except:
                text_clip = TextClip(text, fontsize=23, color="white" ,font = 'Arial-Bold', stroke_color = "yellow", stroke_width = 1)

            text_clip = text_clip.set_position((0.25,0.8), relative=True).set_duration(clip_duration/2)
            globals()[f"cut_final{i}{j}"] = CompositeVideoClip([main_cut, text_clip]) 
            cuts_counter += 1

        globals()[f"clip{i}"] = concatenate_videoclips([ globals()[f"cut_final{i}0"], globals()[f"cut_final{i}1"] ])

    i = 1
    video = CompositeVideoClip([globals()[f"clip{i}"],
                                globals()[f"clip{i + 1}"].set_start(10).set_position("center"),
                                globals()[f"clip{i + 2}"].set_start(20).set_position("center"),
                                globals()[f"clip{i + 3}"].set_start(30).set_position("center"),
                                globals()[f"clip{i + 4}"].set_start(40).set_position("center"),
                                globals()[f"clip{i + 5}"].set_start(50).set_position("center")])
    # =================================60sec - 45sec video=================================
    speed_factor = 60/45
    video45 = video.speedx(factor = speed_factor )
    # =======================================adding audio============================================
    try : 
        feeling = response["feelings"]
    except :
        feeling = response["feeling"]

    print(feeling)
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
    audio_file = AudioFileClip(file_name).subclip(0,45)
    video_final = video45.set_audio(audio_file)

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))

    video_file_name = result_str + ".mp4"
    # video_final.write_videofile(f"{file_name}.mp4", fps =30,codec="libx264")
    video_final.write_videofile(video_file_name, fps =30,codec="libx264")

    add_to_completed_project()
video_generation()