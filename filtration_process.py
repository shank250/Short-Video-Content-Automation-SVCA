# testing file
import pprint
import json

print("now loading the articles from the trends...")
with open("articles.json", "r") as f:
    articles = json.load(f)
print("data loaded")
# pprint.pprint(articles)

filtered_articles = []
counter = 0 
count = 0
# counting the words in each articles and filitering the use less artiles
for text in articles:
    article_text = articles[text]
    character_count = len(article_text)
    print(character_count)
    if character_count > 500 :
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

