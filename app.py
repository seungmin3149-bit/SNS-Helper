import streamlit as st
from google import genai

# 페이지 기본 설정 (모바일 화면 최적화)
st.set_page_config(
    page_title="SNS 마케팅 글 자동 각색기",
    page_icon="📱",
    layout="centered"
)

st.title("📱 SNS 글 자동 각색 도구")
st.caption("하나의 아이디어로 네이버 블로그, 인스타, 스레드 원고를 동시에 생성합니다.")

# --- 1. API 키 설정 (사이드바 또는 상단) ---
with st.sidebar:
    st.header("⚙️ 기본 설정")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy... 로 시작하는 키 입력")
    st.markdown("[무료 API 키 발급받기](https://aistudio.google.com/)")

# --- 2. 메인 입력 폼 ---
st.subheader("1. 내 브랜드 캐릭터 / 톤앤매너")
persona = st.text_input(
    "브랜드 페르소나 설정",
    placeholder="예: 30대 직장인 브랜딩 전문가, 꼼꼼하지만 친근하고 유쾌한 말투",
    label_visibility="collapsed"
)

st.subheader("2. 오늘 작성할 내용 (핵심 메모)")
content = st.text_area(
    "본문 아이디어 입력",
    placeholder="서론-본론-결론 핵심 내용을 작성해주세요.",
    height=150,
    label_visibility="collapsed"
)

# --- 3. 각색 실행 버튼 ---
if st.button("✨ 3개 채널 맞춤 원고 생성하기", use_container_width=True):
    if not api_key:
        st.error("사이드바(또는 설정)에 Gemini API 키를 입력해주세요.")
    elif not content:
        st.warning("작성할 내용을 입력해주세요.")
    else:
        with st.spinner("AI가 각 채널에 맞게 글을 각색하고 있습니다..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
너는 최고의 SNS 마케팅 전문 작가야. 아래 정보와 핵심 메모를 바탕으로 각 채널의 알고리즘과 유저 특성에 맞게 글을 각색해줘.

[브랜드 캐릭터/설정]: {persona if persona else '친근하고 유익한 브랜더'}
[원문 메모/아이디어]:
{content}

다음 3가지 채널용으로 각각 작성해줘. 응답은 반드시 지정된 구분선 형식으로만 출력해.

---BLOG_START---
[네이버 블로그용]
- 캐릭터 설정이 잘 드러나도록 작성
- 서론-본론-결론 구조로 정돈
- 가독성이 좋은 문단 구성
- 하단에 검색용 추천 태그 5~10개 포함
---BLOG_END---

---INSTA_START---
[인스타그램용]
- 시선을 사로잡는 첫 줄 헤드라인
- 가독성 좋은 줄바꿈 및 감성 이모지 활용
- 하단에 도달율을 높이는 인기 해시태그 15~20개 포함
---INSTA_END---

---THREADS_START---
[스레드용]
- 짧고 강렬한 1~3문장 중심의 솔직한 대화체/반말/반반말 톤
- 유저 참여(댓글)를 유도하는 질문으로 마무리
---THREADS_END---
"""
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                res_text = response.text

                # 결과 파싱
                blog_text = res_text.split("---BLOG_START---")[1].split("---BLOG_END---")[0].strip() if "---BLOG_START---" in res_text else ""
                insta_text = res_text.split("---INSTA_START---")[1].split("---INSTA_END---")[0].strip() if "---INSTA_START---" in res_text else ""
                threads_text = res_text.split("---THREADS_START---")[1].split("---THREADS_END---")[0].strip() if "---THREADS_START---" in res_text else ""

                # 결과를 세션에 저장
                st.session_state['blog'] = blog_text
                st.session_state['insta'] = insta_text
                st.session_state['threads'] = threads_text

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# --- 4. 결과 출력 (모바일 탭) ---
if 'blog' in st.session_state:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["네이버 블로그", "인스타그램", "스레드"])

    with tab1:
        st.text_area("블로그 원고", st.session_state['blog'], height=300)
    with tab2:
        st.text_area("인스타 원고", st.session_state['insta'], height=300)
    with tab3:
        st.text_area("스레드 원고", st.session_state['threads'], height=300)