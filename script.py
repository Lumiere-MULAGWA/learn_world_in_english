import time

# Récupération des secrets
#TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
#CHAT_ID = os.getenv("CHAT_ID", "").strip()
import json
import os
import random
import requests
import nltk
from pathlib import Path
from nltk.corpus import wordnet as wn


WORDS_PER_DAY = 10
USED_WORDS_FILE = Path("used_words.json")


def ensure_wordnet() -> None:
    try:
        wn.synsets("test")
    except LookupError:
        nltk.download("wordnet")
        nltk.download("omw-1.4")


def load_used_words() -> set[str]:
    if not USED_WORDS_FILE.exists():
        return set()

    return set(json.loads(USED_WORDS_FILE.read_text()))


def save_used_words(words: set[str]) -> None:
    USED_WORDS_FILE.write_text(json.dumps(sorted(words), indent=2))


def get_french_definition(synset) -> str | None:
    for lemma in synset.lemmas(lang="fra"):
        if lemma.name():
            return lemma.name().replace("_", " ")
    return None


def get_random_words(count: int) -> list[tuple[str, str, str]]:
    used_words = load_used_words()
    synsets = list(wn.all_synsets("n"))
    random.shuffle(synsets)

    results = []

    for synset in synsets:
        if len(results) >= count:
            break

        lemmas = synset.lemmas()
        if not lemmas:
            continue

        word = lemmas[0].name().replace("_", " ")

        if word in used_words:
            continue

        definition_en = synset.definition()
        definition_fr = get_french_definition(synset)

        if not definition_fr:
            continue

        used_words.add(word)
        results.append((word, definition_en, definition_fr))

    if len(results) < count:
        raise RuntimeError("Not enough unused words left")

    save_used_words(used_words)
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

    words = get_random_words(WORDS_PER_DAY)

    lines = ["📘 *10 English Words of the Day*\n"]

    for i, (word, en, fr) in enumerate(words, start=1):
        lines.append(
            f"{i}. 🔤 *{word}*\n"
            f"   🇬🇧 {en}\n"
            f"   🇫🇷 {fr}\n"
        )

    send_to_telegram("\n".join(lines))


if __name__ == "__main__":
    main()
