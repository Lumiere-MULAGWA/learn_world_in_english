import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")

def main():
    print(f"--- DEBUG CONFIGURATION ---")
    print(f"Token présent : {'OUI' if TOKEN else 'NON (VIDE)'}")
    print(f"Chat ID présent : {'OUI' if CHAT_ID else 'NON (VIDE)'}")
    
    if not TOKEN:
        print("ERREUR : Le script s'arrête car le token est vide.")
        return

    # On force l'ajout de 'bot' devant le token si vous l'avez oublié
    clean_token = TOKEN if TOKEN.startswith("bot") else f"bot{TOKEN}"
    api_url = f"https://api.telegram.org{clean_token}/sendMessage"
    
    print(f"Test d'envoi à Telegram...")
    try:
        r = requests.post(api_url, data={"chat_id": CHAT_ID, "text": "Test de connexion GitHub Actions ✅"})
        print(f"Réponse Telegram : {r.status_code}")
        if r.status_code != 200:
            print(f"Détail erreur : {r.text}")
    except Exception as e:
        print(f"Erreur fatale : {e}")

if __name__ == "__main__":
    main()
