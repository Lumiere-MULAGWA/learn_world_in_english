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
        
def get_random_word_with_definition() -> tuple[str, str]:
    synsets = list(wn.all_synsets("n"))

    random.shuffle(synsets)

    for synset in synsets:
        definition = synset.definition()
        lemmas = synset.lemmas()

        if not lemmas or not definition:
            continue

        word = lemmas[0].name().replace("_", " ")
        return word, definition

    raise RuntimeError("No valid word found")

def send_to_telegram(message: str) -> None:
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

def main() -> None:
    ensure_wordnet()
    word, definition = get_random_word_with_definition()

    message = (
        f"📘 Word of the day\n\n"
        f"🔤 {word}\n"
        f"📖 {definition}"
    )

    send_to_telegram(message)

if __name__ == "__main__":
    main()

