import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import time

stopwords = stopwords.words('english')

test = [{"bx80684i99900k": "intel core i9-9900k desktop processor 8 cores up to 5.0 ghz turbo unlocked lga1151 300 series 95w"}, 
{"bx80684i99900kf": "intel bx80684i99900kf intel core i9-9900kf desktop processor 8 cores up to 5.0 ghz turbo unlocked without processor graphics lga1151 300 series 95w"}, 
{"yd2600bbafbox": "amd ryzen 5 2600 processor with wraith stealth cooler - yd2600bbafbox"}, 
{"yd270xbgafbox": "amd ryzen 7 2700x processor with wraith prism led cooler - yd270xbgafbox"}]

all_item_models = []
all_titles = []

for x in test:
    all_item_models.append(list(x.items())[0][0])
    all_titles.append(list(x.items())[0][1])


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

def get_similar_titles(titles):
    cosine_values = check_similarity(["intel core i9"] + all_titles)
    cosine_values_dict = dict(zip(all_item_models, cosine_values[0][1:]))
    sorted_similarity = ({key: value for key, value in sorted(cosine_values_dict.items(), key=lambda item: item[1], reverse=True)})
    title_to_item_model_dict = dict(zip(all_titles, all_item_models))
    return {"sorted_similarity": sorted_similarity, "title_to_item_model": title_to_item_model_dict}