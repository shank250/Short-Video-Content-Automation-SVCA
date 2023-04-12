import openai
import json
openai.api_key = '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'

details = "Using the given article try to  create a script for a youtube, 1 min shorts video around 100 words. also try to give the feeling with the kind of news it is  Also give a clicky title to the clip. Give the instructions of video clips and background images in [] brakets. These video clips do not requires to be specific give a general description of images and videos whaih can be use in the whaole clip any where.\n"

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
            {"role": "user", "content": details + article_body},

        ]

    )

    respoense = response["choices"][0]["message"]["content"]
    print("request send sucessfully")
    print(respoense)
    response_list.append(respoense)

with open("sample_subtitle.json", "w") as f:
    json.dump(response_list, f)
print("Succesfully dumped the  data. :)")