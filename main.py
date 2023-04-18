import os
import json
import pytrends
import pprint
import pandas as pd
import json
from pytrends.request import TrendReq
import webbrowser
import pyautogui as gui
import pyperclip as clip
import time
import openai
import json
import os
from moviepy.editor import *
from moviepy.config import change_settings
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from bing_image_downloader import downloader
import json
import shutil
import threading
import time
import sys
import cv2
import numpy as np
import webcolors

change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})
openai.api_key = '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'
discarded_trends = []
Exception_counter = 0

def trends_extraction():
    data = {}
    # keyword index
    # value details
    # details   0 - title
    #           1 - link 
    #           2 - list of articles

    pytrend = TrendReq()
    trending_today = pytrend.today_searches(pn = 'IN')
    df_trending_today = pd.DataFrame(trending_today)

    links =[]
    i = 0
    for path in trending_today:
        details = []
        url = "https://trends.google.com" + path
        title_uf = url[43:]
        title_uf_2 = title_uf.split("&")
        # adding details
        details.append(title_uf_2[0])
        details.append("https://trends.google.com" + path)
        data[i] = details
        print("Working on ", data[i][0], " ...")
        from googlesearch import search
        from googlesearch import SearchResult
        url_list = list(search(data[i][0]))
        data[i] = data[i] + url_list
        print(data[i])
        i += 1
    print("Sucessfully got the trends. [",len(data),"]")
    # got the  trending for the day sucessfully
    with open("data.json", "w") as f:
        json.dump(data, f)
    print("Succesfully dumped the trends data.")

def article_ext_source():
    # # opening the firefox application
    print("opening the firefox application")
    # now loading the data from the trends 
    print("now loading the data from the trends...")
    import json
    with open("data.json", "r") as f:
        data = json.load(f)
    print("data loaded")
    # keyword : index
    # value : details list
    # details   0 - title
    #           1 - link 
    #           2 - list of articles link
    articles = {}
    counter = 0
    for key in data:
        if data[key][0] in discarded_trends : 
            pass
        else:
            final_key = key
            break
    discarded_trends.append(data[final_key][0])
    
    for link in data[final_key][2:]:
        url = 'about:reader?url=' + link
        webbrowser.register('firefox',
            None,
            webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))
        webbrowser.get('firefox').open(url)
        time.sleep(3)
        # clicking point (x=439, y=127)
        gui.hotkey('ctrl', 'a')
        time.sleep(1)
        gui.hotkey('ctrl', 'c')
        time.sleep(1)
        clipboard_text = clip.paste()
        article = str(clipboard_text)
        # print(article)
        articles[counter] = article
        print("Dumped article no [",counter,"]")
        counter += 1

    with open("articles.json", "w") as f:
        json.dump(articles, f)
    print("Succesfully dumped  all the  articles. \n:)")
    # one mare feature is to be add thata the open tabs will automatically get deleted
    # =============================================filtration process========================================
    for i in range(counter):
        time.sleep(1)
        gui.hotkey('ctrl', 'w')

def article_filtration():
    print("now loading the articles from the trends...")
    with open("articles.json", "r") as f:
        articles = json.load(f)
    print("data loaded")
    filtered_articles = []
    counter = 0 
    count = 0
    # counting the words in each articles and filitering the use less artiles
    for text in articles:
        article_text = articles[text]
        character_count = len(article_text)
        print(character_count)
        if character_count > 500 and character_count < 4000 :
            filtered_articles.append(article_text)
            print("added")
            count += 1
        else:
            pass
        counter += 1

    final_article = list(set(filtered_articles))
    print(count," articles filitered.")
    print(len(final_article)," articles filitered.")
    # pprint.pprint(filtered_articles)
    final_articles = {}
    i = 0 
    for article in final_article :
        final_articles[i] = article
        i += 1
    with open("filtered_articles.json", "w") as f:
        json.dump(final_articles, f)
    print("Succesfully dumped  all the  articles. \n:)")

def script_creation():
    details = "Using the given article create a script for a youtube, 1 min shorts video within 100 words. \n The response should only be in python dictionary format  with title, feelings, image_instruction and script as keys and their values.\n the key feelings should only have one of these values     ness, Sadness, Anger, Fear, Love, Excitement, Anxiety, Frustration or None."
    print("now loading the articles from the filtered articles...")
    with open("filtered_articles.json", "r") as f:
        articles = json.load(f)
    print("data loaded")
    response_list = []
    for article in articles: 
        article_content = articles[article]
        splitted_article = article_content.split("minute", 1)
        article_body = splitted_article[1]
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a journalist and content creator"},
                {"role": "assistant", "content": details },
                {"role": "user", "content": article_body},
            ]
        )

        respoense = response["choices"][0]["message"]["content"]
        print("request send sucessfully")
        print(respoense)
    response_json = eval(respoense)

    with open("sample_subtitle.json", "w") as f:
        json.dump(response_json, f)
    print("Succesfully dumped the  data. :)")

def images_extraction():
    with open("sample_subtitle.json", "r") as f:
        response = json.load(f)

    query_string = response["image_instruction"]
    num_of_images = 6

    downloader.download(query_string, 
                        limit = num_of_images,  
                        output_dir='image', 
                        adult_filter_off=True, 
                        force_replace=False, 
                        timeout=60, verbose=True)

def get_closest_color(rgb):
    # convert the RGB values to the nearest web color
    closest_color = webcolors.rgb_to_name(rgb)
    
    # keep looking for lighter colors until we find one
    while closest_color.lower() == "black" or closest_color.lower() == "white":
        rgb = tuple(c + 25 for c in rgb)
        closest_color = webcolors.rgb_to_name(rgb)
    
    return closest_color

def video_generation():
# import conf.py
    global file_name
    
    with open("sample_subtitle.json", "r") as f:
        response = json.load(f)

    abs_image_folder_locarion = f'image\\{response["image_instruction"]}'

    current_dir = os.getcwd()
    image_folder = os.path.join(current_dir, abs_image_folder_locarion)
    video_file = f'test{response["title"]}'

    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]
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

    for i in range(1,7):
        current_image_file_path = image_files[i-1]
        globals()[f"clip{i}"] = ImageClip(current_image_file_path, duration = clip_duration)
        clip = globals()[f"clip{i}"]
        height = clip.size[1]
        width = clip.size[0]
        clip = clip.set_position(lambda t:( t * (width-new_width-pixels_left_on_sides_padding)/clip_duration, 'center') )
        clip = CompositeVideoClip([clip], size=clip.size)
        if width > height: 
            new_height = height
            new_width = int(new_height * 9 / 16)
            print(new_width, width, clip.size[0],clip.size[1],new_height,height )
            clip = clip.crop(x1 = width - new_width - (pixels_left_on_sides_padding/2), x2 = width).resize((new_width, height))
        else:
            clip = clip.resize((width, height))
        
        # ========================textclip color selection=================================
        try:

            img = cv2.imread(current_image_file_path)

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
            complement_hsv = complement_hsv.reshape((1, 1, 3)) # Add a third dimension to the array
            complement_rgb = cv2.cvtColor(complement_hsv, cv2.COLOR_HSV2BGR)[0][0]

            complement_color = tuple(complement_rgb)
            text_color_name = get_closest_color(complement_color)
        except:
            text_color_name = "grey"

# =============================================================================================
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
            text_clip = VideoFileClip(filename=filename )
            text = globals()[f"cut_text{cuts_counter}"]
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
            text = " ".join(subtitle_text_list)
            try:
                text_clip = TextClip(text, fontsize=25, color=text_color_name ,font = 'Arial-Bold', )
            except:
                text_clip = TextClip(text, fontsize=25, color="grey" ,font = 'Arial-Bold', )

            text_clip = text_clip.set_position("center","center").set_duration(clip_duration/2)
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

def copying_imaportant_files():
    current_dir = os.getcwd()
    dest_dir = 'C:\\Users\\980ar\\Dropbox\\youtube-backupfiles' # Replace with the destination directory path

    for filename in os.listdir(current_dir):
        if filename.endswith(f'{file_name}.mp4'):
            shutil.copy(os.path.join(current_dir, filename), dest_dir)

def cleaning():    
    current_dir = os.getcwd()
    with open("sample_subtitle.json", "r") as f:
        response = json.load(f)
    abs_image_folder_locarion = f'image\\{response["image_instruction"]}'
    image_folder = os.path.join(current_dir, abs_image_folder_locarion)
    for filename in os.listdir(current_dir):
        if filename.endswith('.mp4'):
            os.remove(os.path.join(current_dir, filename))
        # elif filename.endswith('.json'):
        #     os.remove(os.path.join(current_dir, filename))
    for filename_jpg in os.listdir(image_folder):
        if filename_jpg.endswith('.jpg'):
            os.remove(os.path.join(image_folder, filename_jpg))

def do2():
    article_ext_source()
    article_filtration()
    script_creation()
    images_extraction()
    video_generation()
    do2()

def do():
    trends_extraction()
    article_ext_source()
    article_filtration()
    script_creation()
    images_extraction()
    video_generation()
    do2()
    # copying_imaportant_files()
    # cleaning()

def run():
    def processing(stop_event):
        while not stop_event.is_set():
            for c in "\ /":
                sys.stdout.write('\r' + "Processing " + c)
                sys.stdout.flush()
                time.sleep(0.1)

    def do_calculation():
        # here is the program structure
        print("Started")
        try:
            do()
        except:
            print("!!!!!!!!!!!!!!!!!!Something went wrong!!!!!!!!!!!!!!!!!!!!!!!!!")
            cleaning()
            # do()
            Exception_counter += 1
            if Exception_counter > 5 :
                exit()


    stop_event = threading.Event()
    processing_thread = threading.Thread(target=processing, args=(stop_event,))
    processing_thread.start()

    do_calculation()
    stop_event.set()
    print("\nDone!")

do()