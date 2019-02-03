def get_best_product(self):
    """
    Uses a custom algorithm that will get rid of all adjectives in each title and only use the nouns when
    Choosing the most accurate title FAILED
    """
    non_keywords = [":", "|", ')', '(', 'i', 'a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'com', 'de',
                    'en',
                    'for', 'from', 'how', 'in', 'is', 'it', 'la', 'of', 'on', 'or', 'that', 'the', 'this', 'to',
                    'was', 'what', 'when', 'where', 'who', 'will', 'with', 'und', 'the', 'www']
    non_important = [":", "|", ",", "(", ")", "-", '"']
    noun_amazon_title = self.amazon_title
    noun_titles = {}
    noun_titles_score = {}
    new_noun_titles = {}
    final_scores = {}

    # Gets rid of all of the adjectives and useless words in the amazon_title
    for word in noun_amazon_title.split(" "):
        if word.lower() in non_keywords or word.lower() in self.adjectives["adjs"]:
            noun_amazon_title = noun_amazon_title.replace(word, "")

    # Gets rid of all of the adjectives and useless words in each product title
    for title, link in self.titles_links.items():
        temp = title
        for title_word in temp.split(" "):
            if title_word.lower() in non_keywords or title_word.lower() in self.adjectives["adjs"]:
                temp = temp.replace(title_word, "")
        noun_titles[temp] = title

    for char in non_important:
        noun_amazon_title = noun_amazon_title.replace(char, "")

    for title, other in noun_titles.items():
        new_title = title
        for char in non_important:
            new_title = new_title.replace(char, "")
        new_noun_titles[new_title] = other

    noun_titles = new_noun_titles

    for orig_noun_title, orig_title in noun_titles.items():
        noun_title = orig_noun_title.split(" ")
        for x in noun_title:
            if x == " " or x == "":
                noun_title.remove(x)
        score = 0
        for noun in noun_title:
            if "refurbished" in noun.lower() or "used" in noun.lower() or "like-new" in noun.lower():
                score -= 10
            if noun.strip() in noun_amazon_title.strip():
                if " " in noun or noun == "":
                    pass
                else:
                    score += 1

        noun_titles_score[orig_noun_title] = score

    for noun_title, orig_title in noun_titles.items():
        new_noun_title = noun_title.split(" ")
        for x in new_noun_title:
            if x == " " or x == "":
                new_noun_title.remove(x)

        inefficiency = len(new_noun_title)
        final_scores[orig_title] = noun_titles_score[noun_title] - inefficiency
    self.print_titles_links(final_scores)