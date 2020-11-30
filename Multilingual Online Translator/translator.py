import requests
import sys

from bs4 import BeautifulSoup

LANGUAGES = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew",
             7: "Japanese", 8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian",
             12: "Russian", 13: "Turkish"}


def welcome():
    print("Hello, you're welcome to the translator. Translator supports:")
    for k, v in zip(LANGUAGES, LANGUAGES.values()):
        print(f"{k}. {v}")
    _orig = int(input("Type the number of your language:\n"))
    _demanded = int(input("Type the number of a language you want to translate to or '0'"
                          " to translate to all languages:\n"))
    _keyword = input("Type the word you want to translate:\n")
    return _orig, _demanded, _keyword  # returns numbers of languages and word to translate


def make_request(_orig, _demanded, _keyword):
    link = "https://context.reverso.net/translation/" \
           + LANGUAGES[_orig].lower() + '-' + LANGUAGES[_demanded].lower() + '/' + _keyword
    r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})  # sending request to reverso-context
    if r.status_code == 404:
        print(f"Sorry, unable to find {_keyword}")
        sys.exit(-1)
    if not r:  # check for connection
        print("Something wrong with your internet connection")
        sys.exit(-1)
    return r


def get_words_and_examples(r):
    soup = BeautifulSoup(r.content, "html.parser")
    words = soup.find("div", {"id": "translations-content", "class": "wide-container"}).find_all('a')
    translated_words = [a.text.strip() for a in words]  # parsing translated words

    divs = soup.find_all("div", {"class": "src ltr"})
    origin_phrases = [div.text.strip('\n').strip() for div in divs]  # parsing phrases to translate

    divs = soup.find_all("div", {"class": "trg ltr"})
    if not divs:
        divs = soup.find_all("div", {"class": "trg rtl arabic"})
    if not divs:
        divs = soup.find_all("div", {"class": "trg rtl"})
    translated_phrases = [div.text.strip('\n').strip() for div in divs]  # parsing translated phrases
    examples = []
    for i in range(len(translated_phrases)):  # unite both translated and 'to translate' phrases into one list
        if i == 5:
            break
        examples.append(origin_phrases[i])
        examples.append(translated_phrases[i])
    return translated_words[:5], examples


def to_console(_orig, _demanded, _keyword):
    request = make_request(_orig, _demanded, _keyword)
    words, examples = get_words_and_examples(request)
    print()
    print(LANGUAGES[_demanded], "Translations:")
    for x in words:
        print(x)
    print()
    print(LANGUAGES[_demanded], "Example:")
    for i in range(0, len(examples), 2):
        print(examples[i])
        print(examples[i + 1])
        print()


def to_file(_orig, _demanded, _keyword):
    with open(f"{_keyword}.txt", 'a', encoding='utf-8') as f:
        f.write('\n')
        request = make_request(_orig, _demanded, _keyword)
        words, examples = get_words_and_examples(request)
        f.write(f"\n{LANGUAGES[_demanded]} Translations:\n")
        f.write(words[0] + '\n')
        f.write('\n')
        f.write(f"{LANGUAGES[_demanded]} Example:\n")
        if examples:
            f.write(examples[0] + '\n')
            f.write(examples[1] + '\n')
            f.write('\n')


def from_file(_keyword):
    with open(f"{_keyword}.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            print(line.strip('\n'))


def main():
    args = sys.argv
    orig, demanded, keyword = args[1:4]
    if not any(orig.capitalize() in lang for lang in LANGUAGES.values()):
        print(f"Sorry, the program doesn't support {orig}")
        sys.exit(-1)
    if not any(demanded.capitalize() in lang for lang in LANGUAGES.values()) and demanded != "all":
        print(f"Sorry, the program doesn't support {demanded}")
        sys.exit(-1)
    for k in LANGUAGES.keys():
        if LANGUAGES[k].lower() == orig:
            orig = k
            break
    if demanded == "all":
        demanded = 0
    else:
        for k in LANGUAGES.keys():
            if LANGUAGES[k].lower() == demanded:
                demanded = k
                break
    open(f"{keyword}.txt", 'w')
    if demanded == 0:
        for i in range(1, 14, 1):
            if i != orig:
                to_file(orig, i, keyword)
        from_file(keyword)
    else:
        to_file(orig, demanded, keyword)
        from_file(keyword)


if __name__ == '__main__':
    main()
