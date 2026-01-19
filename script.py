import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_word_details(word):
    url = f"https://api.dictionaryapi.dev{word}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            word_name = data.get('word', word)
            phonetic = data.get('phonetic', 'N/A')
            definition = data['meanings'][0]['definitions'][0]['definition']
            return f"🇬🇧 *{word_name.upper()}* [{phonetic}]\n📖 {definition}"
    except:
        return None

def main():
    words_found = []
    while len(words_found) < 10:
        res = requests.get("https://random-word-api.herokuapp.com")
        for word in res.json():
            if len(words_found) >= 10: break
            details = get_word_details(word)
            if details: words_found.append(details)
    
    message = "📅 *VOS 10 MOTS DU JOUR*\n\n" + "\n\n".join(words_found)
    requests.post(f"https://api.telegram.org{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    main()
