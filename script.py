import requests
import os
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_word_details(word):
    """Récupère la définition d'un mot avec gestion d'erreur."""
    url = f"https://api.dictionaryapi.dev{word}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                word_name = entry.get('word', word)
                phonetic = entry.get('phonetic', 'N/A')
                # Accès sécurisé à la définition
                meanings = entry.get('meanings', [])
                if meanings:
                    definition = meanings[0].get('definitions', [{}])[0].get('definition', 'Pas de définition')
                    return f"🇬🇧 *{word_name.upper()}* [{phonetic}]\n📖 {definition}"
    except Exception as e:
        print(f"Erreur dictionnaire pour {word}: {e}")
    return None

def main():
    words_found = []
    attempts = 0
    
    print("Démarrage de la récupération...")

    while len(words_found) < 10 and attempts < 5:
        attempts += 1
        try:
            # Source de mots aléatoires
            res = requests.get("https://random-word-api.herokuapp.com", timeout=15)
            
            if res.status_code == 200:
                potential_words = res.json()
                for word in potential_words:
                    if len(words_found) >= 10:
                        break
                    details = get_word_details(word)
                    if details:
                        words_found.append(details)
                        print(f"Trouvé: {word}")
                        time.sleep(0.5) # Pause pour respecter l'API
            else:
                print(f"L'API de mots a répondu avec le code: {res.status_code}")
        except Exception as e:
            print(f"Erreur lors de l'appel API: {e}")
            time.sleep(2) # Attendre avant de réessayer

    if not words_found:
        message = "⚠️ Désolé, impossible de récupérer les mots aujourd'hui (Erreur API)."
    else:
        message = "📅 *VOS 10 MOTS DU JOUR*\n\n" + "\n\n".join(words_found)

    # Envoi Telegram
    print("Envoi vers Telegram...")
    send_url = f"https://api.telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    final_res = requests.post(send_url, data=payload)
    if final_res.status_code == 200:
        print("Succès !")
    else:
        print(f"Échec de l'envoi Telegram: {final_res.text}")

if __name__ == "__main__":
    main()
