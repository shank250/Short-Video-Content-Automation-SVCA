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
from datetime import datetime, timedelta
from youtube_uploader_selenium import YouTubeUploader
import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import random
import string
pyautogui.FAILSAFE = False

change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})
openai.api_key = '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'
discarded_trends = []
Exception_counter = 0
final_key = "0"
video_file_name = "finalvideo.mp4"

def selecting_topic():
    # project log will keep track of the completed projects
    global final_key;
    current_dir = os.getcwd()
    project_log_location = current_dir + r'\other_files\project_log.json'
    with open(project_log_location, 'r') as f:
        log = json.load(f)
    with open("data.json", 'r') as f2:
        data= json.load(f2)
    old_project_topic_list = []
    for topics in log:
        old_project = log[topics]
        old_project_topic_list.append(old_project)
    print("Existing project list : ",old_project_topic_list,"\nTotla no of trends from google trends : ",len(data))
    for i in range(len(data)):
        topic_Trends = data[f'{i}'][0]
        if topic_Trends not in old_project_topic_list:
            final_key = str(f'{i}')
            print("Now working on : ", topic_Trends)
            break
        else:
            print("This trend clip already exits : ",topic_Trends)
    

    final_key = str(final_key)
    print("Final key : ",final_key,type(final_key))

def add_to_completed_project():
    global final_key;
    # structure of project_log
    # keys : "0"
    # values: "trends title"
    current_dir = os.getcwd()
    project_log_location = current_dir + r'\other_files\project_log.json'
    with open("data.json", "r") as f:
        data = json.load(f)
    with open(project_log_location, "r") as f :
        log = json.load(f)
    no_of_topics = len(list(log.keys()))
    log[f'{no_of_topics + 1}'] = data[final_key][0]
    with open(project_log_location, 'w') as f:
        json.dump(log, f)
    print("Sucessfully added the project to log file.")

def trends_extraction():
    global data ;
    data = {}
    # keyword index
    # value details
    # details   0 - title
    #           1 - link 
    #           2 - list of articles

    pytrend = TrendReq()

    trending_today = pytrend.today_searches(pn = 'IN')
    # realtime_trending_searches

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
    
    now = datetime.now()
    now = str(now)
    current_date = now[:10]
    current_hour = now[11:13]

    time_dict = {}
    time_dict["date"] = current_date
    time_dict["hour"] = current_hour
    print(time_dict)

    with open('last_run.json', 'w') as f:
        json.dump(time_dict, f)

def check_trends_extraction():
    now = datetime.now()
    now = str(now)
    current_date = now[:10]
    current_hour = now[11:13]
    print("Current datetime :", now, "\nTodays date:", current_date,"\nCurrent hour :", current_hour)

    with open('last_run.json', 'r') as f:
        trend_last_run = json.load(f)

    if trend_last_run['date'] == current_date :
        if (int(trend_last_run['hour']) + 2) < int(current_hour) :
            # run the trends
            trends_extraction()
        else:
            # no changes in the trends.json and we would not run the trends
            print("Trend is upto date.")
            pass
    else:
        # run the trends
        trends_extraction()

def article_ext_source():
    # # opening the firefox application
    print("opening the firefox application")
    # now loading the data from the trends 
    print("now loading the data from the trends...")
    with open("data.json", "r") as f:
        data = json.load(f)
    # print("data loaded")
    # keyword : index
    # value : details list
    # details   0 - title
    #           1 - link 
    #           2 - list of articles link
    articles = {}
    counter = 0
    # for key in data:
    #     if data[key][0] in discarded_trends : 
    #         pass
    #     else:
    #         final_key = key
    #         break
    # discarded_trends.append(data[final_key][0])
    selecting_topic()
    gui.hotkey('alt', 'tab')
    print(data[final_key][0])
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
    gui.hotkey('alt', 'tab')
    

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
    details = "Using the given article create a script for a youtube 1 min shorts video within 100 words. \n The response should only be in python dictionary format  with title, feelings, image_instruction, tags and script as keys and their values.\n the key feelings should only have one of these values Sadness, Anger, Fear, Love, Excitement, Anxiety, Frustration or None."
    print("now loading the articles from the filtered articles...")
    with open("filtered_articles.json", "r") as f:
        articles = json.load(f)
    print("data loaded")
    response_list = []
    if len(articles) == 0 :
        print("Zero filtered articles found.\nAdding this to completed project and moving to other next topic.")
        add_to_completed_project()
        cleaning()
        do()

    try:
            
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
            if "title" and "feelings" and "image_instruction" and "script" in respoense :
                break
            else :
                print("-------------------------didn't got quality content---------------------------")
                print("-------------------------------retrying---------------------------------------")
                script_creation()
        response_json = eval(respoense)
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!error in open ai request!!!!!!!!!!!!!!!!!!!!!!!!")
        print("-------------------------retrying------------------------------------")
        script_creation()
    with open("sample_subtitle.json", "w") as f:
        json.dump(response_json, f)
    print("Succesfully dumped the  data. :)")

def images_extraction(num_of_images = 30):
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
                if height > 500 and width >= 16*height/9:
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
                elif height > 500 and width > 1000:
                    # 1280 width
                    # aspect_ratio = width / height
                    new_width = 1280
                    new_height = int(new_width / aspect_ratio)
                    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                    # croping
                    height_resized, width_resized, channels_resized = resized_img.shape
                    crop_up = int((height_resized - 720)/2)
                    crop_down = crop_up + 720
                    croped_img = resized_img[crop_up:crop_down, :]
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
        current_dir = os.getcwd()
        abs_image_folder_locarion = r'image_downloads'
        image_folder = os.path.join(current_dir, abs_image_folder_locarion)

        for filename in os.listdir(image_folder):
            os.remove(os.path.join(image_folder, filename))
        images_extraction(90)

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
        x1, y1 = 0, 500
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
                text_clip = TextClip(text, fontsize=23, color="white" ,font = 'Arial-Bold', stroke_color = "white", stroke_width = 1 )
            except:
                text_clip = TextClip(text, fontsize=23, color="white" ,font = 'Arial-Bold', stroke_color = "white", stroke_width = 1)
            
            text_clip = text_clip.set_position((0.11,0.7), relative=True).set_duration(clip_duration/2)
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
    speed_factor = 60/40
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
        
    current_dir = os.getcwd()
    abs_audio_folder_locarion = r'audio'
    audio_folder = os.path.join(current_dir, abs_audio_folder_locarion)
    for checking_possible_feelings in possible_feelings :
        if feeling == checking_possible_feelings:
            try:
                feeling_folder = os.apth.join(audio_folder,feeling)
                audio_folder_content = [os.path.join(feeling_folder, f) for f in os.listdir(feeling_folder) ]
                n = len(audio_folder_content)
                random_index = random.randint(0, n)
                file_name = audio_folder_content[random_index]
                break
            except:
                file_name = f"{feeling}.mp3"
                break
        # else:
        #     print("exception has occured in getting music feeling so default music is taken")
        #     file_name = "Sadness.mp3"
        #     break
    audio_file = AudioFileClip(file_name).subclip(0,40)
    video_final = video45.set_audio(audio_file)

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))

    video_file_name = result_str + ".mp4"
    # video_final.write_videofile(f"{file_name}.mp4", fps =30,codec="libx264")
    video_final.write_videofile(video_file_name, fps =30,codec="libx265")

    add_to_completed_project()

def copying_imaportant_files():
    current_dir = os.getcwd()
    # G:\My Drive\new folder
    dest_dir = 'G:\\My Drive\\new folder' # Replace with the destination directory path

    for filename in os.listdir(current_dir):
        if filename.endswith(video_file_name):
            shutil.move(os.path.join(current_dir, filename), dest_dir)
    print('Moved the file to desiered location.')

def upload_on_youtube():
    # add left click after every mouse move
    with open("sample_subtitle.json", "r") as f:
        data = json.load(f)
    pyautogui.PAUSE = 8
    pyautogui.press('win')
    pyautogui.write('google chrome beta')
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.moveTo(240,62)
    pyautogui.click()
    # pyautogui.mouseInfo()

    pyautogui.write('studio.youtube.com')
    pyautogui.press('enter')

    # create button
    pyautogui.moveTo(1773,125)
    pyautogui.click()
    # upload button
    pyautogui.moveTo(1703,178)
    pyautogui.click()

    # file selection
    pyautogui.moveTo(967,725)
    pyautogui.click()

    # getting the video file
    pyautogui.moveTo(282,222)
    pyautogui.click()

    # selecting the video
    pyautogui.press('enter')
    pyautogui.click()

    # video title
    pyautogui.moveTo(448,459)
    pyautogui.click(clicks=2)

    # video title
    pyautogui.write(data["title"])

    # 2 times tabs
    pyautogui.press('tab')
    pyautogui.press('tab')


    tag_string = "\n#Trends"
    for i in data['tags']:
        tag_string += f' #{i}'
    print(tag_string)
    pyautogui.write(data["script"] + tag_string)


    # # adding  tags to the video
    # pyautogui.PAUSE = 0.1
    # for i in range(13):
    #     pyautogui.press('tab')

    # pyautogui.press('enter')
    # pyautogui.PAUSE = 2
    # for i in range(8):
    #     pyautogui.press('tab')

    # pyautogui.write(data["tags"])

    # next button
    pyautogui.moveTo(1514,974)
    pyautogui.click()

    # next button
    pyautogui.moveTo(1514,974)
    pyautogui.click()

    # next button
    pyautogui.moveTo(1514,974)
    pyautogui.click()

    # next button
    pyautogui.moveTo(1514,974)
    pyautogui.click()
    pyautogui.hotkey("ctrl", "w")

def cleaning():   
    current_dir = os.getcwd()
    abs_image_folder_locarion = r'image_downloads'
    image_folder = os.path.join(current_dir, abs_image_folder_locarion)

    for filename in os.listdir(image_folder):
        os.remove(os.path.join(image_folder, filename)) 
    # current_dir = os.getcwd()
    # with open("sample_subtitle.json", "r") as f:
    #     response = json.load(f)
    # abs_image_folder_locarion = f'image\\{response["image_instruction"]}'
    # image_folder = os.path.join(current_dir, abs_image_folder_locarion)
    # for filename in os.listdir(current_dir):
        # if filename.endswith('.mp4'):
        #     os.remove(os.path.join(current_dir, filename))
        # elif filename.endswith('.json'):
    #     #     os.remove(os.path.join(current_dir, filename))
    # for filename_jpg in os.listdir(image_folder):
    #     if filename_jpg.endswith('.jpg'):
    #         os.remove(os.path.join(image_folder, filename_jpg))
    print("Cleaning process completed.")

def do2():
    check_trends_extraction()
    article_ext_source()
    article_filtration()
    script_creation()
    images_extraction()
    video_generation()
    copying_imaportant_files()
    upload_on_youtube()
    cleaning()
    do()

def do():
    check_trends_extraction()
    article_ext_source()
    article_filtration()
    script_creation()
    images_extraction()
    video_generation()
    copying_imaportant_files()
    upload_on_youtube()
    cleaning()
    do2()
    
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
            do()
            Exception_counter += 1
            if Exception_counter > 5 :
                exit()


    stop_event = threading.Event()
    processing_thread = threading.Thread(target=processing, args=(stop_event,))
    processing_thread.start()

    do_calculation()
    stop_event.set()
    print("\nDone!")
video_generation()