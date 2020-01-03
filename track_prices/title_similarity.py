import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import time

stopwords = stopwords.words('english')

def clean_string(title):
    title = title.lower()
    title = ''.join([word for word in title if word not in string.punctuation])
    title = ' '.join([word for word in title.split() if word not in stopwords])

    return title

# Titles is a list of titles given
def check_similarity(titles):
    cleaned = list(map(clean_string, titles))
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()
    csim = cosine_similarity(vectors)
    return csim

def get_similar_titles(title, item_model_dict):
    all_item_models = []
    all_titles = []

    print(item_model_dict)
    for x in item_model_dict["item_models"]:
        all_item_models.append(list(x.items())[0][0])
        all_titles.append(list(x.items())[0][1])

    cosine_values = check_similarity([title] + all_titles)
    cosine_values_dict = dict(zip(all_item_models, cosine_values[0][1:]))
    sorted_similarity = ({key: value for key, value in sorted(cosine_values_dict.items(), key=lambda item: item[1], reverse=True)})
    title_to_item_model_dict = dict(zip(all_titles, all_item_models))
    return {"sorted_similarity": sorted_similarity, "title_to_item_model": title_to_item_model_dict}