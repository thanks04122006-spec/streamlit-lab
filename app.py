# 📋 app.py · [과제 3단계] 나만의 AI API 를 부르는 화면 (프런트엔드) — 고칠 곳 없음 · Secrets 의 API_URL · APP_ACCESS_CODE 만 넣으면 됨 (질문 한 번에 요청 1번)
import requests
import streamlit as st

try:
    API_URL = st.secrets["API_URL"]                  # Community Cloud Secrets — 내 API 의 짧은 vercel.app 주소
except Exception:
    API_URL = "http://localhost:8000"                # Secrets 가 없으면(Colab 점검) 같은 런타임의 API 서버

try:
    ACCESS_CODE = st.secrets["APP_ACCESS_CODE"]      # Vercel 의 APP_ACCESS_CODE 와 같은 값 (코드 · GitHub 에 적지 않음)
except Exception:
    ACCESS_CODE = ""

try:                                                 # GET / · GET /examples — 이름 · 소개 · 예시 질문 (Gemini 요청 없음)
    info = requests.get(f"{API_URL}/", timeout=30).json()
    examples = requests.get(f"{API_URL}/examples", timeout=30).json()["examples"]
except (requests.RequestException, ValueError, KeyError):
    st.error("❌ API 서버에 닿지 못함 — 아래 'API 주소' 가 내 vercel.app 주소인지 확인하세요.")
    st.caption(f"API 주소 : {API_URL}")
    st.stop()

st.title(info.get("name", "나만의 AI"))
st.caption(f"{info.get('description', '')} · API 주소 : {API_URL}")

tone = st.selectbox("말투", ["친근한 존댓말", "씩씩한 반말", "정중한 안내문"])
question = st.text_input("질문", placeholder=examples[0] if examples else "")
if examples:
    st.caption("예시 질문 : " + " / ".join(examples))

if st.button("물어보기", disabled=(question.strip() == "")):
    with st.spinner("API 에 묻는 중..."):
        try:
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question, "tone": tone},
                headers={"X-Access-Code": ACCESS_CODE},
                timeout=90,
            )
        except requests.RequestException:
            st.error("❌ API 서버에 닿지 못함 — 잠시 뒤 다시 눌러 보세요.")
        else:
            if response.status_code == 200:
                data = response.json()
                st.markdown(data["answer"])
                st.caption(f"상태 번호 200 · 토큰 {data['tokens']}")
            else:
                st.error(f"❌ 상태 번호 {response.status_code} : {response.json().get('detail')}")
