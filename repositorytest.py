from functools import lru_cache

from nltk.stem import PorterStemmer

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

stemmer = PorterStemmer()

# imported from nltk
en_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
                'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
                'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
                'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
                'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
                'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
                'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't",
                'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
                "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
                'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
                'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

dict_greetings = {"hi": "Hi there!", "hello": "Hello!", "how are you": "Thanks, I'm good",
                  "how is it going": "Going quite well, thanks.", "what up": "Wuz up baby!"}

domains = {

    "ai": ["ai business consultant", "ai", "business", "consultant", "aibc", "artificial intelligence",
           "digital", "business intelligence", "bi translator", "ai career", "career in ai"],
    "bd": ["business innovation", "business developer", "business model", "business", "build solution",
           "solution", "business challenges", "user experience", "project management", "management",
           "leading people", "project", "leadership", "exploring data", "brand", "business design", "development",
           "developing", "develop", "testing product"],
    "cd": ["content", "developer", "storytelling", "content creation", "video production", "writing", "strategy",
           "planning", "production", "digital channels", "marketing", "communication", "sales", "technical",
           "business", "knowledge", "creativity", "text", "images", "movies", "sound", "legal", "distribution",
           "communications", "PR", "social media", "startup", "agencies", "organizations", "computer", "software",
           "brands"]
}

suggestions_domains_dict = {
    "ai": 'AI Business Consultant',
    "bd": 'Business Developer',
    "cd": 'Content Developer'
}


@lru_cache(maxsize=128)
def stem(word):
    """
    It takes a word and returns the stem of that word

    Args:
      word: The word that the user wishes to convert into its root form.

    Returns:
      The stem of the word.
    """
    return stemmer.stem(word)


def check_keywords(word, keywords):
    """
    It checks if a word is in the list of stopwords, and if not, it checks if the word is in the list of
    keywords. If it is, it returns the keyword, otherwise it returns False

    Args:
      word: the word to be checked
      keywords: a list of keywords to search for

    Returns:
      the keyword if the word is in the list of keywords.
    """
    if word in en_stopwords:
        return False
    word = stemmer.stem(word)
    for key in keywords:
        keys = [stemmer.stem(k) for k in key.split()]
        if word in keys:
            return key
    return False


def suggest(input_phrase):
    suggestions = []
    split_input = input_phrase.split()
    for word in split_input:
        for domain, keywords in domains.items():
            key = check_keywords(word, keywords)
            if key:
                logging.debug(f"{word} is in {key} -> {domain}")
                suggestions.append(suggestions_domains_dict[domain])
    if not suggestions:
        key = check_keywords(word, dict_greetings.keys())
        if key:
            logging.debug(f"{word} is in {key} -> 'Greetings'")
            re_greet = dict_greetings.get(key)
            return re_greet

    if len(suggestions) > 0:
        suggestions = list(set(suggestions))
        if len(suggestions) > 1:
            suggestions_str = ", ".join(
                suggestions[:-1]) + " and " + suggestions[-1]
        else:
            suggestions_str = " and ".join(suggestions)
        suggestions_str = "You might be interested in " + suggestions_str + "."
        return suggestions_str
    else:
        return "Please try again."


def main():
    input_phrase = input(
        "HI! How can we help you today?: ").lower().replace("?", "")

    while True:
        response = suggest(input_phrase)
        print(response)

        more_input = input(
            "Is there anything else? (yes/no) ").lower().replace("?", "")
        if more_input == "no":
            print("Thank you for your interest. Hope to see you again!")
            break
        elif more_input == "yes":
            input_phrase = input(
                "Great! What else can I help with?: ").lower().replace("?", "")


if __name__ == "__main__":
    main()
