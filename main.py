import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# 페이지 설정
st.set_page_config(page_title="AI Poet", page_icon="📜")

st.title("📜 인공지능 시인")
st.write("주제를 입력하면 시를 써드립니다.")

# API 키 설정
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.text_input("Google API Key를 입력하세요", type="password")

# 주제 입력 받기
content = st.text_input("시의 주제를 제시해주세요 (예: 가을, 사랑, 코딩)")

if st.button("시 작성 요청"):
    if not api_key:
        st.error("설정된 API 키가 없습니다.")
        st.stop()

    if not content:
        st.warning("주제를 입력해주세요.")
        st.stop()

    with st.spinner("시를 짓고 있습니다..."):
        try:
            # Gemini 모델 설정
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro", 
                google_api_key=api_key
            )

            # 프롬프트 템플릿
            template = """
            너는 감성적인 시인이야. 아래 주제에 대해 아름다운 시를 써줘.

            주제: {content}
            """
            prompt = PromptTemplate(
                input_variables=["content"],
                template=template
            )

            # 체인 실행
            chain = prompt | llm
            result = chain.invoke({"content": content})

            # 결과 출력
            st.success("작성 완료!")
            st.write(result.content)

        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")



