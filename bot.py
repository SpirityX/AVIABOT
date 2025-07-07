import requests
import time

# === CONFIGURATION ===
TOKEN = "7697856704:AAERMlnyRYA9TR_U-F1EDcqwgW0M8pbH3yA"
API_URL = f"https://api.telegram.org/bot{TOKEN}"
CHANNEL_USERNAME = "@spiritychannel"
ACCESS_CODE = "P3X7V9Q2L8ZD5NM1KT4J
"
APP_URL = "https://spirityx.github.io/Ghostpqqb-/"

user_states = {}

# === ENVOI DE MESSAGE ===
def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(f"{API_URL}/sendMessage", json=payload)
    except Exception as e:
        print(f"Erreur d'envoi : {e}")

# === RÉCUPÉRATION DES MESSAGES ===
def get_updates(offset=None):
    try:
        response = requests.get(f"{API_URL}/getUpdates", params={"timeout": 100, "offset": offset})
        return response.json()
    except:
        return {}

# === VÉRIFICATION ABONNEMENT ===
def check_user_in_channel(user_id):
    try:
        res = requests.get(f"{API_URL}/getChatMember", params={
            "chat_id": CHANNEL_USERNAME,
            "user_id": user_id
        }).json()
        status = res.get("result", {}).get("status", "")
        return status in ["member", "administrator", "creator"]
    except:
        return False

# === FONCTION PRINCIPALE ===
def main():
    print("✅ Bot lancé avec succès.")
    offset = None

    while True:
        updates = get_updates(offset)
        if updates.get("ok"):
            for update in updates["result"]:
                offset = update["update_id"] + 1
                message = update.get("message")
                callback = update.get("callback_query")

                if message:
                    chat_id = message["chat"]["id"]
                    user_id = message["from"]["id"]
                    text = message.get("text", "")
                    state = user_states.get(user_id)

                    if text == "/start":
                        keyboard = {
                            "inline_keyboard": [[
                                {"text": "✅ 𝙰𝚅𝙰𝙽𝙲𝙴𝚁 😈", "callback_data": "continue"}
                            ]]
                        }
                        welcome = (
                            "<b>👋 Bienvenue dans ton nouveau QG Aviator !</b>\n"
                            "🎯 Objectif : Prédire intelligemment.\n"
                            "📡 Analyse, seed, cycles, signaux = stratégie.\n"
                            "🚀 Prêt à dominer le ciel ? Clique ci-dessous."
                        )
                        send_message(chat_id, welcome, reply_markup=keyboard)

                    elif state == "awaiting_join":
                        if check_user_in_channel(user_id):
                            user_states[user_id] = "awaiting_code"
                            send_message(chat_id,
                                "✅ Tu as bien rejoint <b>@spiritychannel</b> !\n\n"
                                "🔐 Pour activer ton accès au bot :\n"
                                "Envoie ici ton <b>code d'accès privé</b>.\n\n"
                                "📲 Si tu ne l'as pas encore :\n"
                                "WhatsApp : +22603996469\n"
                                "Telegram : @ANonyXMousHack"
                            )
                        else:
                            send_message(chat_id,
                                "🚫 Tu dois rejoindre le canal : <b>@spiritychannel</b>\n\n"
                                "📡 Infos, signaux, stratégies en direct.\n"
                                "✅ Une fois fait, reviens ici et envoie n’importe quel message pour continuer."
                            )

                    elif state == "awaiting_code":
                        if text == ACCESS_CODE:
                            user_states[user_id] = "granted"
                            send_message(chat_id, "🔓 <b>Accès validé !</b> Tu peux maintenant ouvrir l’application.")
                            menu_keyboard = {
                                "inline_keyboard": [[
                                    {"text": "🚀 𝙾𝚄𝚅𝚁𝙸𝚁 𝙻'𝙰𝙿𝙿", "web_app": {"url": APP_URL}}
                                ]]
                            }
                            send_message(chat_id, "👇 Clique ici pour accéder à l'outil :", reply_markup=menu_keyboard)
                        else:
                            send_message(chat_id,
                                "❌ <b>Code incorrect.</b>\n\n"
                                "👉 Pour recevoir le bon code, contacte :\n"
                                "WhatsApp : +22603996469\n"
                                "Telegram : @ANonyXMousHack"
                            )

                elif callback:
                    chat_id = callback["message"]["chat"]["id"]
                    user_id = callback["from"]["id"]
                    data = callback["data"]

                    requests.post(f"{API_URL}/answerCallbackQuery", json={"callback_query_id": callback["id"]})

                    if data == "continue":
                        user_states[user_id] = "awaiting_join"
                        send_message(chat_id,
                            "📢 Étape 1 : Rejoins le canal stratégique @spiritychannel\n\n"
                            "📲 Une fois dedans, reviens ici et envoie n’importe quel message.\n"
                            "🔐 Nécessaire pour débloquer le bot."
                        )

        time.sleep(1)

# === DÉMARRAGE ===
if __name__ == "__main__":
    main()
