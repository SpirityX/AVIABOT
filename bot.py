import requests
import time

# === CONFIGURATION ===
TOKEN = "7697856704:AAERMlnyRYA9TR_U-F1EDcqwgW0M8pbH3yA"
API_URL = f"https://api.telegram.org/bot{TOKEN}"
CHANNEL_USERNAME = "@spiritychannel"
ACCESS_CODE = "12345678"
APP_URL = "https://spirityx.github.io/Ghostpqqb-/"

user_states = {}

# === ENVOI DE MESSAGES ===
def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=payload)

def get_updates(offset=None):
    response = requests.get(f"{API_URL}/getUpdates", params={"timeout": 100, "offset": offset})
    return response.json()

def check_user_in_channel(user_id):
    res = requests.get(f"{API_URL}/getChatMember", params={
        "chat_id": CHANNEL_USERNAME,
        "user_id": user_id
    }).json()
    status = res.get("result", {}).get("status")
    return status in ["member", "creator", "administrator"]

# === MAIN BOT ===
def main():
    print("🤖 Bot lancé.")
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
                                {"text": "✅ 𝙰𝚅𝙰𝙽𝙲𝙴𝚁😈", "callback_data": "continue"}
                            ]]
                        }
                        welcome_message = (
                            "<b>👋 Bienvenue dans ton nouveau QG Aviator !</b>\n"
                            "🎮 <b>Ici, c’est pas du hasard… c’est de la stratégie.</b> 🧠💥\n\n"
                            "<b>🎯 Objectif ?</b>\n"
                            "🚀 Jouer plus malin\n"
                            "📊 Prédire les bons coups\n"
                            "🛑 Éviter les mauvaises séries\n"
                            "💸 Et choper des multiplicateurs propres 🔥\n\n"
                            "<b>🤖 Ce bot, c’est pas un mythe.</b>\n"
                            "C’est de l’analyse intelligente et hybride :\n"
                            "🔍 Lecture du seed\n"
                            "🔁 Reconnaissance de motifs\n"
                            "📈 Détection des cycles\n"
                            "💡 Résultat ? Des prédictions nettes, calibrées, puissantes.\n\n"
                            "<b>⚙️ 3 modes adaptés à ton flow :</b>\n"
                            "⚡ Rapide – pour aller droit au but\n"
                            "⚖️ Standard – le bon équilibre, simple et fiable\n"
                            "🔬 Approfondi – ultra précis pour ceux qui veulent tout analyser\n\n"
                            "<b>🎚️ Et tu choisis ton niveau de risque :</b>\n"
                            "🟢 Faible — sécurisé\n"
                            "🟡 Moyen — équilibré\n"
                            "🔴 Élevé — agressif\n\n"
                            "🚫 À savoir :\n"
                            "<b>Ce bot n’est pas magique.</b> ❌\n"
                            "Il te donne un avantage, pas une garantie.\n"
                            "👉 Joue avec la tête. Gère tes mises. Sois smart. 💼🧠\n\n"
                            "🔥 <b>Prêt à passer en mode joueur stratège ?</b>\n"
                            "Alors installe-toi...\n"
                            "<b>T’es officiellement dans le game.</b> 🎮💣"
                        )
                        send_message(chat_id, welcome_message, reply_markup=keyboard)

                    elif state == "awaiting_join":
                        if check_user_in_channel(user_id):
                            send_message(chat_id,
                                "✅ <b>Tu as bien rejoint le canal !</b>\n\n"
                                "💸 <b>Étape suivante :</b> Pour débloquer l’accès complet au bot, tu dois activer ton accès officiel.\n\n"
                                "📲 <b>Contacte ce WhatsApp :</b> +22603996469\n"
                                "👤 <b>Ou envoie un message sur Telegram :</b> @@ANonyXMousHack\n\n"
                                "🧾 Une fois le paiement validé, tu recevras ton <b>code d'accès privé</b>.\n"
                                "🔐 <b>Envoie ce code ici pour activer le bot.</b>\n\n"
                                "🚀 Let’s go, c’est maintenant que tout commence."
                            )
                            user_states[user_id] = "awaiting_code"
                        else:
                            send_message(chat_id,
                                "🚨 <b>Accès réservé aux vrais stratèges.</b>\n\n"
                                "Tu veux débloquer le bot ? Voici la prochaine étape :\n\n"
                                "📲 <b>Étape cruciale :</b> rejoins maintenant le QG tactique :\n"
                                "👉 <b>@spiritychannel</b>\n\n"
                                "🎯 C’est là que tout commence :\n"
                                "🔐 Accès prioritaire aux prédictions\n"
                                "📡 Signaux en temps réel\n"
                                "🧠 Conseils d’experts\n\n"
                                "<b>⚠️ Obligatoire pour activer le bot.</b>\n\n"
                                "✅ Une fois dans le QG, reviens ici et envoie n’importe quel message pour lancer la machine.\n\n"
                                "💡 Pas de canal = pas d’analyse = pas de stratégie.\n"
                                "🔥 Tu veux rester random, ou passer en mode contrôle total ?\n"
                                "Le choix est à toi."
                            )

                    elif state == "awaiting_code":
                        if text == ACCESS_CODE:
                            send_message(chat_id,
                                "🔓 <b>Accès validé !</b>\n\n"
                                "🚀 Tu viens officiellement de débloquer l’outil stratégique ultime.\n"
                                "🎯 Place au vrai game maintenant : cycles, prédictions, précision chirurgicale.\n\n"
                                "🔥 Appuie sur le bouton ci-dessous et entre dans l’arène."
                            )

                            menu_keyboard = {
                                "inline_keyboard": [[
                                    {"text": "🚀 𝙾𝚄𝚅𝚁𝙸𝚁 𝙻𝙰 𝙱𝙾𝙼𝙱𝙴", "web_app": {"url": APP_URL}}
                                ]]
                            }
                            send_message(chat_id,
                                "✅ <b>Accès accordé !</b>\nClique sur le bouton ci-dessous pour ouvrir l’application :",
                                reply_markup=menu_keyboard
                            )
                            user_states[user_id] = "granted"
                        else:
                            send_message(chat_id,
                                "❌ <b>Code incorrect.</b>\n\n"
                                "💡 Ce code n’est pas valide ou n’a pas encore été activé.\n"
                                "👉 Pour obtenir ton accès officiel, contacte :\n"
                                "📲 WhatsApp : +22603996469\n"
                                "📩 Telegram : @ANonyXMousHack \n\n"
                                "🧾 Une fois le paiement validé, tu recevras ton <b>code privé</b> ici."
                            )

                elif callback:
                    chat_id = callback["message"]["chat"]["id"]
                    user_id = callback["from"]["id"]
                    data = callback["data"]

                    requests.post(f"{API_URL}/answerCallbackQuery", json={"callback_query_id": callback["id"]})

                    if data == "continue":
                        user_states[user_id] = "awaiting_join"
                        send_message(chat_id,
                            "📢 Pour continuer, suis bien cette étape :\n\n"
                            "➡️ Rejoins le canal officiel : @spiritychannel\n\n"
                            "✅ Ensuite, reviens ici et envoie n’importe quel message pour activer le bot.\n\n"
                            "🛠️ C’est obligatoire pour débloquer les prédictions.\n\n"
                            "🔥 Let’s go — on passe au niveau supérieur ! t.me/spiritychannel"
                        )

        time.sleep(1)

# === DÉMARRAGE ===
if __name__ == "__main__":
    main()
