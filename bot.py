#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой Telegram-бот без внешних зависимостей.
Реагирует на ключевые фразы на русском и отвечает нужным сообщением.
"""

import os
import sys
import time
import json
import logging
import urllib.request
import urllib.parse

# --- Настройки: либо запиши токен сюда, либо установи переменную окружения TG_BOT_TOKEN ---
TOKEN = os.environ.get("TG_BOT_TOKEN") or "REPLACE_WITH_YOUR_TOKEN"
if TOKEN == "REPLACE_WITH_YOUR_TOKEN":
    print("ERROR: Установите токен в переменной окружения TG_BOT_TOKEN или вставьте токен в файл.")
    sys.exit(1)

API = f"https://api.telegram.org/bot{TOKEN}/"

# Список ключевых фраз (нижний регистр)
KEYWORDS = [
    "как получить плейлист",
    "дайте плейлист",
    "я хочу плейлист",
    "я хочу получить плейлист",
]

# Ответ бота
REPLY = (
    "Уважаемый подписчик! Все сервисы с плейлистами находятся в главном меню "
    "в разделе «Каналы» — https://t.me/polzafre/22"
)

# Логирование (в файл bot.log и в консоль)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s",
                    handlers=[
                        logging.FileHandler("bot.log", encoding="utf-8"),
                        logging.StreamHandler()
                    ])

def api_request(method: str, params: dict = None, timeout: int = 90):
    """Универсальный вызов Telegram API (POST form)."""
    params = params or {}
    data = urllib.parse.urlencode(params).encode("utf-8")
    url = API + method
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        logging.exception("API request failed (%s %s)", method, e)
        return None

def get_updates(offset: int = None, timeout: int = 60):
    p = {"timeout": timeout}
    if offset:
        p["offset"] = offset
    return api_request("getUpdates", p, timeout=timeout+10)

def send_message(chat_id: int, text: str, reply_to: int = None):
    p = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_to:
        p["reply_to_message_id"] = reply_to
    return api_request("sendMessage", p)

def normalize(text: str) -> str:
    return text.lower()

def main_loop():
    logging.info("Bot started")
    offset = None
    while True:
        updates = get_updates(offset=offset, timeout=60)
        if not updates:
            # сетевые проблемы — подождём и повторим
            time.sleep(1)
            continue
        if not updates.get("ok"):
            logging.error("getUpdates returned not ok: %s", updates)
            time.sleep(5)
            continue

        for upd in updates.get("result", []):
            offset = upd["update_id"] + 1  # подтвердим апдейт
            msg = upd.get("message") or upd.get("edited_message")
            if not msg:
                continue
            # не отвечаем ботам
            if msg.get("from", {}).get("is_bot"):
                continue
            text = msg.get("text") or msg.get("caption") or ""
            if not text:
                continue
            txt = normalize(text)
            # если есть любое вхождение ключевой фразы — отвечаем
            if any(k in txt for k in KEYWORDS):
                chat_id = msg["chat"]["id"]
                reply_to = msg.get("message_id")
                logging.info("Matched: chat=%s user=%s text=%s", chat_id, msg.get("from", {}).get("username"), text)
                res = send_message(chat_id, REPLY, reply_to=reply_to)
                if res and res.get("ok"):
                    logging.info("Replied successfully")
                else:
                    logging.error("Failed to send reply: %s", res)
        # цикл повторится (getUpdates использует long polling, так что CPU не загружается)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info("Stopped by user (KeyboardInterrupt)")
    except Exception:
        logging.exception("Fatal error - exiting")
