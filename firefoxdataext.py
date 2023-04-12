import webbrowser
import pyautogui as gui
import pyperclip as clip
import time

# # opening the firefox application
# print("opening the firefox application")
# gui.press('super')
# time.sleep(1)
# gui.write("Firefox")
# time.sleep(2)
# gui.press('enter')

# # conferming the application is working fine
# time.sleep(2)
# import psutil
# for p in psutil.process_iter(attrs=['pid', 'name']):
#     if p.info['name'] == "firefox.exe":
#         print("yes", (p.info['name']))
#         break
#     else:
#         print("something went wrong...\nFirefox isn't opened.")

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

# setting the target data
# print(data['0'][4])

articles = {}
counter = 0
for link in data['0'][2:]:
    # # mouse position (41,116)
    # gui.write("about:reader?url=" + link)
    # time.sleep(1)
    # gui.press('enter')
    # time.sleep(5)
    # gui.press('f9')
    # testing file

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

# =============================================filtration process========================================
