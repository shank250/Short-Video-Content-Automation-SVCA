import os
import json
from moviepy.editor import *
from moviepy.config import change_settings
from moviepy.video.io.VideoFileClip import VideoFileClip
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})\

current_dir = os.getcwd()
image_folder = os.path.join(current_dir, 'image')
video_file = 'output3.mp4'
script_file = os.path.join(current_dir, 'script\\test.txt')

with open("sample_subtitle.json", "r") as f:
    response = json.load(f)
# calculating the time for short
words_list = response["script"].split(" ")
total_no_of_words = len(words_list)
avg_words = total_no_of_words // 12
remaining_words = total_no_of_words % 12
# 12 cuts
clip_duration = 10
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

clip = VideoFileClip("clip1.mp4").subclip(0,10)
text_clip = TextClip("ye raj h ieska", fontsize = 40, color = 'white', method='caption' ,font='Amiri-Bold')
text_clip = text_clip.set_duration(10).set_position("bottom", "center")
clip_final = CompositeVideoClip([clip, text_clip])

with open("sample_subtitle.json", "r") as f:
    response = json.load(f)

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
clip_final_music = clip_final.set_audio(audio_file)

# Write the final video clip to a file
clip_final_music.write_videofile('my_video.mp4', fps=24)

