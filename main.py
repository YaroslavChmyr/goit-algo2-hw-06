import requests
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor
import re

def fetch_text(url):
    """Завантажує текст із вказаної URL-адреси."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def clean_text(text):
    """Очищає текст від спеціальних символів і перетворює його в нижній регістр."""
    return re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', text).lower()

def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    return {key: sum(values) for key, values in shuffled_values}

def map_reduce(text):
    """Виконує MapReduce аналіз тексту."""
    with ThreadPoolExecutor() as executor:
        mapped_values = executor.map(map_function, [text])
    mapped_values = list(mapped_values)[0]
    shuffled_values = shuffle_function(mapped_values)
    return reduce_function(shuffled_values)

def visualize_top_words(word_freq, top_n=10):
    """Візуалізує топ N слів за частотою використання."""
    top_words = Counter(word_freq).most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.title(f"Топ {top_n} найчастіших слів")
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    try:
        text = fetch_text(url)
        cleaned_text = clean_text(text)
        word_frequencies = map_reduce(cleaned_text)
        visualize_top_words(word_frequencies)
    except requests.RequestException as e:
        print(f"Помилка завантаження тексту: {e}")