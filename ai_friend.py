# -*- coding: utf-8 -*-
import streamlit as st
import json
import requests

# Настройка страницы сайта
st.set_page_config(page_title="Гаражный Кореш ИИ", page_icon="⚙️", layout="centered")
st.title("⚙️ Твой ИИ-Кореш на связи")
st.caption("Чистый разум, честное железо, Саракташ 2026")

# 📥 Загружаем системный промт (ДНК бота) из JSON-файла
try:
    with open("context.json", "r", encoding="utf-8") as f:
        context_data = json.load(f)
    SYSTEM_PROMPT = context_data["system_prompt"]
except Exception as e:
    SYSTEM_PROMPT = "Ты просто ИИ-помощник."

# 🔌 Сетевые параметры шлюза ProxyAPI (Официальный проверенный URL)
API_KEY = "sk-RHqikjrG8RpjVO3Xo2e2d3dZFKU6se4c"
URL = "https://proxyapi.ru"
MODEL_NAME = "gpt-4o-mini"

# 🧠 Работа с оперативной памятью чата (чтобы бот помнил диалог)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Отображаем историю чата на экране смартфона/ПК
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 💬 Обработка ввода от пользователя
if user_input := st.chat_input("Здорова! Че по машинам или по жизни?"):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Отправляем JSON-запрос через HTTP POST в кодировке UTF-8
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        data = {
            "model": MODEL_NAME,
            "messages": st.session_state.messages,
            "max_tokens": 400  # Жестко режем бронь токенов шлюза в 10 раз!
        }
        
        # json.dumps гарантирует идеальную кодировку кириллицы перед отправкой
        response = requests.post(
            URL, 
            headers=headers, 
            data=json.dumps(data, ensure_ascii=False).encode('utf-8')
        )
        
        # Если шлюз ответил успешно (код 200)
        if response.status_code == 200:
            try:
                result = response.json()
                
                # Защита: проверяем, что пришел словарь и внутри есть список choices
                if isinstance(result, dict) and "choices" in result and len(result["choices"]) > 0:
                    reply = result["choices"][0]["message"]["content"] # Пофиксили индекс массива!
                    
                    with st.chat_message("assistant"):
                        st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error(f"Шлюз вернул нетипичный ответ: {result}")
                    
            except ValueError:
                st.error(f"Сервер прислал не JSON текст: {response.text}")
        else:
            st.error(f"Косяк шлюза ProxyAPI (Статус {response.status_code}): {response.text}")
            
    except Exception as e:
        st.error(f"Бро, упала сеть или косяк в запросе: {e}")
