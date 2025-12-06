import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# 페이지 설정
st.set_page_config(page_title="AI Poet", page_icon="📜")

st.title("📜 인공지능 시인 (AI Poet)")
st.write("주제를 입력하면 시를 써드립니다. (Powered by Gemini)")

# ------------------------------------------------------------------
# [중요] API 키 설정
# Github에 올릴 때는 키를 절대 노출하지 않기 위해 st.secrets를 사용합니다.
# ------------------------------------------------------------------
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Secrets가 설정되지 않았을 때 화면에서 직접 입력받기 (테스트용)
    api_key = st.text_input("Google API Key를 입력하세요", type="password")

# 주제 입력 받기
content = st.text_input("시의 주제를 제시해주세요 (예: 가을, 사랑, 코딩)")

if st.button("시 작성 요청"):
    if not api_key:
        st.error("API Key가 없습니다. Streamlit 배포 설정에서 Secrets를 입력해주세요.")
        st.stop()

    if not content:
        st.warning("주제를 입력해주세요.")
        st.stop()

    with st.spinner("시를 짓고 있습니다..."):
        try:
            # Gemini 모델 설정 (무료 버전인 gemini-1.5-flash 사용)
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
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