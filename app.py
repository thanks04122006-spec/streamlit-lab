# ============================================================
# [실습 0-2] 앱 셀 도우미 켜기 (요청 없음 · 런타임마다 한 번)
# ------------------------------------------------------------
# 이 셀을 실행한 뒤에는, 첫 줄이 "# 📋 app.py" 로 시작하는 셀을 실행하면
#   ① 셀 내용을 app.py 파일로 저장하고
#   ② 웹 화면 없이 Colab 안에서 앱을 한 번 실행해 (Streamlit AppTest)
#   ③ 화면에 나올 것과 오류를 보여 줍니다
# 오류가 없으면 그 셀 전체를 복사해 GitHub 의 app.py 에 붙여 넣습니다.
# ============================================================
import os
import logging
from streamlit.testing.v1 import AppTest
from google.colab import userdata

# 웹 화면 없이 실행할 때 나오는 'missing ScriptRunContext' 경고 글을 숨김 (동작에는 영향 없음)
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").disabled = True


def open_app():
    """app.py 를 웹 화면 없이 실행할 준비를 하고, 처음 화면까지 실행해 돌려준다"""
    app_test = AppTest.from_file(os.path.abspath("app.py"), default_timeout=120)   # Colab 의 /content/app.py
    app_test.secrets["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")   # Community Cloud 의 Secrets 칸 대신
    return app_test.run()


def show_screen(app_test):
    """AppTest 결과에서 화면에 나올 글 · 위젯을 한 줄씩 보여 준다"""
    groups = [("제목", app_test.title), ("소제목", app_test.header), ("소제목", app_test.subheader),
              ("글", app_test.markdown), ("작은 글", app_test.caption),
              ("입력칸", app_test.text_input), ("고르기", app_test.selectbox), ("고르기", app_test.radio),
              ("슬라이더", app_test.slider), ("체크", app_test.checkbox), ("버튼", app_test.button),
              ("채팅 입력칸", app_test.chat_input), ("숫자", app_test.metric),
              ("✅", app_test.success), ("ℹ️", app_test.info), ("⚠", app_test.warning), ("🟥", app_test.error)]
    for name, elements in groups:
        for element in elements:
            label = getattr(element, "label", None) or getattr(element, "placeholder", None)
            value = getattr(element, "value", "")
            text = f"{label} : {value}" if name == "숫자" else (label if label else value)
            print(f"   · {name} : {str(text)[:70]}")


def last_answer(app_test):
    """가장 마지막 말풍선의 글을 돌려준다 (오류가 났으면 오류 글)"""
    if app_test.error:
        return app_test.error[-1].value
    bubble = app_test.chat_message[-1]
    return bubble.markdown[-1].value if bubble.markdown else ""


def save_and_check_app(source):
    """셀 내용을 app.py 로 저장하고, 웹 화면 없이 한 번 실행해 결과를 보여 준다"""
    with open("app.py", "w", encoding="utf-8") as app_file:
        app_file.write(source)
    try:
        compile(source, "app.py", "exec")             # 먼저 문법(괄호 · 따옴표 · 들여쓰기)만 검사
    except SyntaxError as error:
        print(f"❌ 문법 오류 — {error.lineno}번째 줄 : {error.msg} → 고친 뒤 다시 실행하세요 (GitHub 에 올리지 않음)")
        return
    app_test = open_app()
    if app_test.exception:
        print("❌ 앱 실행 중 오류 — GitHub 에 올리지 말고 고친 뒤 다시 실행하세요")
        print("  ", app_test.exception[0].value)
        return
    print("✅ 오류 없음 — app.py 로 저장했습니다. 처음 화면에 나올 것 :")
    show_screen(app_test)
    print("👉 이 셀 전체를 복사(셀 클릭 → Ctrl+A → Ctrl+C) → GitHub 의 app.py 에 붙여 넣기 → Commit")


def app_cell(lines):
    """첫 줄이 '# 📋 app.py' 인 셀은 실행하는 대신 저장 + 점검으로 바꾼다"""
    if lines and lines[0].startswith("# 📋 app.py"):
        return [f"save_and_check_app({''.join(lines)!r})\n"]
    return lines


transformers = get_ipython().input_transformers_cleanup
transformers[:] = [t for t in transformers if getattr(t, "__name__", "") != "app_cell"]   # 두 번 실행해도 하나만
transformers.append(app_cell)
print("✅ 앱 셀 도우미 준비 완료 — 이제 '# 📋 app.py' 로 시작하는 셀을 실행하면 저장 + 점검이 됩니다")
