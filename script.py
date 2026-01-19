import requests
import os
import time
import random

# Récupération des secrets GitHub
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_word_details(word):
    url = f"https://api.dictionaryapi.dev{word}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Structure de l'API Dictionary en 2026
            entry = data[0]
            word_name = entry.get('word', word)
            phonetic = entry.get('phonetic', 'N/A')
            meanings = entry.get('meanings', [])
            if meanings:
                definition = meanings[0].get('definitions', [{}])[0].get('definition', 'No definition')
                return f"🇬🇧 *{word_name.upper()}* [{phonetic}]\n📖 {definition}"
    except:
        return None

def main():
    # Vérification de sécurité pour le token
    if not TOKEN or "VOTRE" in TOKEN:
        print("ERREUR : Le TELEGRAM_TOKEN est manquant ou mal configuré dans les Secrets GitHub.")
        return

    words_found = []
    print("Démarrage de la récupération...")

    # Liste de secours au cas où l'API Random-Word crash encore
    backup_words = ["achievement", "belief", "challenge", "discovery", "effort", "freedom", "growth", "happiness", "insight", "journey", "knowledge", "leadership", "motivation", "opportunity", "passion", "quality", "resilience", "success", "thrive", "wisdom"]

    try:
        res = requests.get("https://random-word-api.herokuapp.com", timeout=10)
        potential_words = res.json() if res.status_code == 200 else random.sample(backup_words, 15)
    except:
        print("API Random-Word HS, utilisation de la liste de secours.")
        potential_words = random.sample(backup_words, 15)

    for word in potential_words:
        if len(words_found) >= 10: break
        details = get_word_details(word)
        if details:
            words_found.append(details)
            time.sleep(0.3)

    # Construction du message
    if not words_found:
        message = "⚠️ Erreur technique : impossible de récupérer les définitions."
    else:
        message = "📅 *VOS 10 MOTS DU JOUR*\n\n" + "\n\n".join(words_found)

    # Envoi Telegram sécurisé
    send_url = f"https://api.telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    print(f"Tentative d'envoi à l'ID : {CHAT_ID}")
    r = requests.post(send_url, data=payload)
    if r.status_code == 200:
        print("Message envoyé !")
    else:
        print(f"Erreur Telegram : {r.text}")

if __name__ == "__main__":
    main()
