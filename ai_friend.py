import streamlit as st
from openai import OpenAI
import json
import os

st.set_page_config(page_title="Гаражный Кореш ИИ", page_icon="⚙️", layout="centered")
st.title("⚙️ Твой ИИ-Кореш на связи")
st.caption("Чистый разум, честное железо, Саракташ 2026")

# 📥 Загружаем системный промт из JSON-файла с жестким указанием UTF-8 кодировки
try:
    with open("context.json", "r", encoding="utf-8") as f:
        context_data = json.load(f)
    SYSTEM_PROMPT = context_data["system_prompt"]
except Exception as e:
    st.error(f"Косяк загрузки базы знаний: {e}")
    SYSTEM_PROMPT = "Ты просто ИИ-помощник."

# 🔌 Настройка подключения к нейросети (API) из секретов облака
API_KEY = st.secrets["API_KEY"]
BASE_URL = st.secrets.get("BASE_URL", "https://proxyapi.ru")
MODEL_NAME = st.secrets.get("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 🧠 Работа с оперативной памятью чата
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Отображаем историю чата
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 💬 Обработка ввода от пользователя
if user_input := st.chat_input("Здорова! Че по машинам или по жизни?"):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Запрос к нейросети
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=st.session_state.messages
        )
        reply = response.choices.message.content
        
        with st.chat_message("assistant"):
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Бро, косяк в коде или с сетью (ошибка API): {e}")