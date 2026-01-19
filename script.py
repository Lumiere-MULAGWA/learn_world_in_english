import os
import requests
import random
import time

# Récupération des secrets
TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()

def get_word_details(word):
    """Récupère la définition d'un mot."""
    url = f"https://api.dictionaryapi.dev{word}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            # On prend la première entrée et la première définition
            entry = data[0]
            word_name = entry.get('word', word)
            phonetic = entry.get('phonetic', 'N/A')
            meanings = entry.get('meanings', [])
            if meanings:
                definition = meanings[0]['definitions'][0]['definition']
                return f"🇬🇧 *{word_name.upper()}* [{phonetic}]\n📖 {definition}"
    except:
        return None
    return None

def main():
    if not TOKEN or not CHAT_ID:
        print("Erreur : Secrets manquants.")
        return

    words_found = []
    # Liste de secours au cas où l'API de mots aléatoires est en panne
    backup_words = ["achievement", "belief", "challenge", "discovery", "effort", "freedom", 
                    "growth", "happiness", "insight", "journey", "knowledge", "leadership", 
                    "motivation", "opportunity", "passion", "quality", "resilience", "success"]

    print("Récupération des mots...")
    
    # 1. Tentative de récupération de mots aléatoires
    try:
        res = requests.get("https://random-word-api.herokuapp.com", timeout=10)
        potential_words = res.json() if res.status_code == 200 else random.sample(backup_words, 15)
    except:
        potential_words = random.sample(backup_words, 15)

    # 2. On cherche les définitions pour en avoir exactement 10
    for word in potential_words:
        if len(words_found) >= 10:
            break
        details = get_word_details(word)
        if details:
            words_found.append(details)
            print(f"Mot ajouté : {word}")
            time.sleep(0.3) # Pause pour ne pas saturer l'API du dictionnaire

    # 3. Construction du message final
    if not words_found:
        message = "⚠️ Désolé, impossible de récupérer les mots aujourd'hui."
    else:
        message = "📅 *VOS 10 MOTS DU JOUR (2026)*\n" + "─" * 20 + "\n\n"
        message += "\n\n".join(words_found)

    # 4. Envoi sécurisé
    clean_token = TOKEN.replace("bot", "")
    api_url = f"https://api.telegram.org{clean_token}/sendMessage"
    
    try:
        response = requests.post(api_url, data={
            "chat_id": CHAT_ID, 
            "text": message, 
            "parse_mode": "Markdown"
        })
        if response.status_code == 200:
            print("Succès : Les 10 mots ont été envoyés !")
        else:
            print(f"Erreur Telegram : {response.text}")
    except Exception as e:
        print(f"Erreur d'envoi : {e}")

if __name__ == "__main__":
    main()
