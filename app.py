# 📋 app.py · [실습 3-1] 따라 말하기 봇 — 채팅 화면 부품 익히기 (요청 없음)
import streamlit as st

st.title("🦜 따라 말하기 봇")

if "messages" not in st.session_state:      # 이 탭에서 처음 열었을 때만 빈 기록을 만듦
    st.session_state.messages = []          # [{"role": "user" 또는 "assistant", "text": 글}, ...]

for message in st.session_state.messages:   # 다시 실행될 때마다 지금까지의 대화를 말풍선으로 다시 그림
    st.chat_message(message["role"]).markdown(message["text"])

if text := st.chat_input("아무 말이나 입력하세요"):   # 입력하고 Enter 를 누른 그 실행에서만 글이 들어옴
    st.chat_message("user").markdown(text)
    answer = f"🦜 {text}"                   # AI 대신 그대로 따라 말함
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "user", "text": text})
    st.session_state.messages.append({"role": "assistant", "text": answer})
