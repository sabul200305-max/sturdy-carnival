import streamlit as st
import os
import time
from openai import OpenAI

st.set_page_config(page_title="무지개다리 기억보관소", page_icon="💌", layout="centered")

if "generated_letter" not in st.session_state:
    st.session_state.generated_letter = None
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# 가장 안전한 표준 방식으로 비밀번호를 자동 연동합니다.
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_pet_letter(pet_info: dict) -> str:
    system_prompt = "당신은 무지개다리를 건넌 반려동물입니다. 남겨진 주인이 슬퍼하지 않도록 따뜻하게 위로하는 편지를 400자 내외로 작성하세요."
    user_content = f"- 이름: {pet_info['name']}\n- 호칭: {pet_info['owner_call']}\n- 간식: {pet_info['favorite']}\n- 버릇: {pet_info['habit']}\n- 추억: {pet_info['memory']}"
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}], temperature=0.85)
    return response.choices.message.content

def generate_pet_image(pet_info: dict) -> str:
    prompt = f"A beautiful watercolor fairytale illustration of a happy pet named {pet_info['name']} playing in a sunny cloud garden. Heartwarming aesthetic. No text."
    response = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
    return response.data.url

st.title("💌 무지개다리 기억보관소")
st.subheader("하늘나라에서 도착한 우리 아이의 첫 번째 편지")
st.write("아이와의 소중한 추억을 입력하시면, 아이의 마음을 담은 편지와 그림을 선물해 드립니다.")
st.markdown("---")

st.markdown("### 🐾 1. 우리 아이 정보 입력")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("아이의 이름", placeholder="예: 초코, 코코", value="초코")
    owner_call = st.text_input("아이를 기준으로 한 내 호칭", placeholder="예: 엄마, 아빠", value="엄마")
    user_phone = st.text_input("카카오톡을 받을 휴대폰 번호", placeholder="예: 01012345678", value="01083380552")
with col2:
    favorite = st.text_input("가장 좋아했던 간식", placeholder="예: 고구마 말랭이", value="고구마")
    habit = st.text_input("자주 하던 귀여운 버릇", placeholder="예: 퇴근하고 오면 배 보여주기", value="배 보여주기")
memory = st.text_area("아이와 기억에 남는 특별한 추억", placeholder="예: 한강 공원에서 같이 산책하다가 나비 쫓아가서 한참 웃었던 기억...", value="한강 공원에서 같이 산책하다가 나비 쫓아가서 한참 웃었던 기억이 제일 많이 나 보고 싶다 초코야")

st.markdown("---")

# 대표님을 방해하던 모든 빈칸 체크 에러 창을 아예 통째로 삭제하고 강제 통과시킵니다!
if st.button("💝 아이의 편지 받아보기", type="primary"):
    with st.status("🌈 하늘나라 우체통 확인 중...", expanded=True) as status:
        st.write("✨ 아이와의 추억을 바탕으로 편지를 적고 있어요...")
        pet_data = {"name": pet_name, "owner_call": owner_call, "favorite": favorite, "habit": habit, "memory": memory}
        letter = generate_pet_letter(pet_data)
        st.write("🎨 편지에 담을 이쁜 그림을 그리고 있어요...")
        image_url = generate_pet_image(pet_data)
        st.write("📱 입력하신 번호로 카카오톡 전송을 준비 중입니다...")
        time.sleep(1)
        st.session_state.generated_letter = letter
        st.session_state.generated_image = image_url
        status.update(label="💌 전송 완료! 아래에서 확인해 보세요.", state="complete", expanded=False)
        st.success(f"🎉 성공! 발송을 완료했습니다. (시뮬레이션)")

if st.session_state.generated_letter and st.session_state.generated_image:
    st.markdown("---")
    st.markdown(f"### 📬 {pet_name}(이)가 보낸 편지")
    res_col1, res_col2 = st.columns([1.2, 1])
    with res_col1:
        st.info(st.session_state.generated_letter)
    with res_col2:
        st.image(st.session_state.generated_image, caption=f"하늘나라에서 잘 지내고 있는 {pet_name}", use_column_width=True)
    st.markdown("### 🎁 소중한 추억을 영원히 간직하세요")
    st.write("AI가 생성한 이 편지와 그림을 최고급 캔버스 액자 및 실물 책자로 제작해 드립니다.")
    st.button("📦 프리미엄 추억 액자 패키지 소장하기")
