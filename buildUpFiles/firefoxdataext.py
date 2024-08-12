import webbrowser
import pyautogui as gui
import pyperclip as clip
import time

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

for link in data[key][2:]:
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
