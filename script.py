import os
import requests
import random
import time

# Nettoyage des variables
TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()

def get_word_details(word):
    url = f"https://api.dictionaryapi.dev{word}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()[0]
            word_name = data.get('word', word)
            phonetic = data.get('phonetic', 'N/A')
            # Extraction sécurisée de la définition
            definition = data['meanings'][0]['definitions'][0]['definition']
            return f"🇬🇧 *{word_name.upper()}* [{phonetic}]\n📖 {definition}"
    except:
        return None

def main():
    if not TOKEN or not CHAT_ID:
        print("ERREUR : Secrets manquants.")
        return

    words_found = []
    backup_words = ["achievement", "belief", "challenge", "discovery", "effort", "freedom", "growth", "happiness", "insight", "journey"]
    
    try:
        res = requests.get("https://random-word-api.herokuapp.com", timeout=5)
        potential_words = res.json() if res.status_code == 200 else backup_words
    except:
        potential_words = backup_words

    for word in potential_words:
        if len(words_found) >= 10: break
        details = get_word_details(word)
        if details:
            words_found.append(details)
            time.sleep(0.2)

    message = "📅 *VOS 10 MOTS DU JOUR*\n\n" + "\n\n".join(words_found)

    # CORRECTION DE L'URL : On ajoute le / explicitement entre 'bot' et le TOKEN
    api_url = f"https://api.telegram.org{TOKEN}/sendMessage"
    
    print(f"Tentative d'envoi à Telegram...")
    try:
        response = requests.post(api_url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        if response.status_code == 200:
            print("Succès ! Message envoyé.")
        else:
            print(f"Erreur Telegram : {response.text}")
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")

if __name__ == "__main__":
    main()
