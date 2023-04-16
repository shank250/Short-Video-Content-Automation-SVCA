import openai
import json
openai.api_key = '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'

details = "Using the given article create a script for a youtube, 1 min shorts video within 100 words. \n The response should only be in python dictionary format  with title, feelings, image_instruction and script as keys and their values.\n the key feelings should only have one of these values Happiness, Sadness, Anger, Fear, Love, Excitement, Anxiety, Frustration or None."

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