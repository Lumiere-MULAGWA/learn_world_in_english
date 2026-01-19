import time

# Récupération des secrets
#TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
#CHAT_ID = os.getenv("CHAT_ID", "").strip()
import os
import random
import requests
import nltk
from nltk.corpus import wordnet as wn

def ensure_wordnet() -> None:
    try:
        wn.synsets("test")
    except LookupError:
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        
def get_random_words_with_definitions(count: int) -> list[tuple[str, str]]:
    synsets = list(wn.all_synsets("n"))
    random.shuffle(synsets)

    results: list[tuple[str, str]] = []
    seen_words: set[str] = set()

    for synset in synsets:
        if len(results) >= count:
            break

        lemmas = synset.lemmas()
        definition = synset.definition()

        if not lemmas or not definition:
            continue

        word = lemmas[0].name().replace("_", " ")

        if word in seen_words:
            continue

        seen_words.add(word)
        results.append((word, definition))

    if len(results) < count:
        raise RuntimeError("Not enough unique words found")

    return results

def send_to_telegram(message: str) -> None:
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown"
}

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

def main() -> None:
    ensure_wordnet()

    words = get_random_words_with_definitions(WORDS_PER_DAY)

    lines = ["📘 *10 English Words of the Day*\n"]

    for i, (word, definition) in enumerate(words, start=1):
        lines.append(f"{i}. 🔤 *{word}*\n   📖 {definition}\n")

    message = "\n".join(lines)

    send_to_telegram(message)

if __name__ == "__main__":
    main()

