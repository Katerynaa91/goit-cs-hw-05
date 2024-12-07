import requests
import matplotlib.pyplot as plt
import nltk

from string import punctuation
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from mapreduce import MapReduce
 

def get_url(url):
    """Функція для отримання тексту з url-адреси"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None

def get_text(url, end = None, *args):
    """Функція для парсингу тексту, отриманого з url-адреси. """

    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    for word in args:
        stop_words.add(word)

    text = get_url(url)
    if text is None:
        return "No response from the server or text not accessible"
    else:
        soup = BeautifulSoup(text.lower(), "html.parser")
                                      
        text_s = ''.join(word.text for word in soup.find_all('p')[:end]) # мерджимо знайдені параграфи з тегом "p" у рядок
                                                            #не всі параграфи належать до змісту, тому зайве (end index = <p> position) видаляємо
        text_s = text_s.translate(str.maketrans("", "", punctuation+"–"))  #видаляємо пунктуацію та дефіси (не входить до колекції модуля string)
        text = text_s.split()                                                 #перетворюємо текст на список рядків для подальшого підрахунку слів 
        text = [word for word in text if word !='—']                        #видаляємо зайві тире, що залишились
        text = [word for word in text if word not in stop_words] 
        
        return text

def map_reducing_text(text):
    """Функція для застосування методу MapReduce до тексту та сортування отриманого словника за значеннями"""
    text_s = ' '.join(text)
    mp = MapReduce(text_s)
    mp_dict = mp.mpreduce
    sorted_dict = sorted(mp_dict.items(), key=lambda item: item[1], reverse=True)
    return dict(sorted_dict)


def find_top_words(text, top_count = 10):
    """Функція для виведення слів, що найчастіше використовуються у тексті. Повертає словник, де ключ - саме слово, значення - його частота.
     Якщо декілька слів мають однакову частоту, будуть показані всі ці слова (наприклад, 2 слова, які зустрічаються в тексті 12 разів) """
    top_values = sorted(list(set(text.values())), reverse=True)[:top_count]
    print(top_values)
    filtered_dict = dict(filter(lambda item: item[1] in top_values, text.items()))
    return filtered_dict

def visualize_top_words(common_words_dict):
    """Функція для відображення кількості слів у вигляді горизонтальної діаграми"""

    common_words_dict = dict(sorted(common_words_dict.items(), key=lambda x: x[1])) #"перевертаємо" словник, щоб більші значення на графіку були зверху
    # додаємо заголовки для вікна діаграми, самої діаграми, осей Х та У
    fig, ax = plt.subplots(label = "Word Count in the Web Text")   
    ax.set_xlabel("Word Count")
    ax.set_ylabel("Words")
    ax.set_title("Word Count in the Web Text")

    #малюємо діаграму
    Y, X = common_words_dict.keys(), common_words_dict.values()
    plt.barh(Y, X, data = common_words_dict, color= [c for c in plt.cm.Blues(range(100, 100+ len(common_words_dict)*10, 10))])
    x_vals = max(common_words_dict.values()) - max(common_words_dict.values())%10 + 10
    plt.xticks([i for i in range(0, x_vals, 10)])
    plt.yticks(fontsize= 8)
    #додаємо текст до стовпців діаграми
    for k, v in common_words_dict.items():
        plt.text(v+1, k, s=v, fontsize=5, color='#36454F')

    plt.grid(True, alpha = 0.3)
    ax.spines[['left', 'bottom']].set_color('lightgrey')
    ax.spines[['right', 'top']].set_visible(False)

    plt.show()



if __name__ == "__main__":

    url = "https://sppe.lse.ac.uk/articles/40"
    add_stop_words = ['acemoglu', 'robinson', 'authors']
    t = get_text(url, 18, *add_stop_words)
    words_frequency_dict = map_reducing_text(t)
    # print(words_frequency_dict)
    top_words = find_top_words(words_frequency_dict)

    visualize_top_words(top_words)
