import os
import requests
import random

# On récupère les secrets
TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()

def main():
    if not TOKEN:
        print("ERREUR : TELEGRAM_TOKEN est vide dans les secrets GitHub.")
        return
    
    # On nettoie le token au cas où vous auriez mis 'bot' dedans par erreur
    clean_token = TOKEN.replace("bot", "")
    
    # Construction de l'URL avec vérification
    # Le format final doit être https://api.telegram.org
    base_url = "https://api.telegram.org"
    endpoint = f"/bot{clean_token}/sendMessage"
    full_url = base_url + endpoint
    
    print(f"Tentative d'envoi...")
    
    payload = {
        "chat_id": CHAT_ID,
        "text": "✅ Test réussi ! Votre automate 2026 est opérationnel.",
        "parse_mode": "Markdown"
    }

    try:
        # On utilise une session pour plus de stabilité
        session = requests.Session()
        r = session.post(full_url, data=payload, timeout=15)
        
        if r.status_code == 200:
            print("SUCCÈS : Message envoyé à Telegram !")
        else:
            print(f"ÉCHEC : Code {r.status_code}")
            print(f"Réponse du serveur : {r.text}")
            
    except Exception as e:
        print(f"ERREUR FATALE : {e}")

if __name__ == "__main__":
    main()
