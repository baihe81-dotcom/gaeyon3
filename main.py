import streamlit as st
import random

# ======================
# 초기 상태 설정
# ======================
if "money" not in st.session_state:
    st.session_state.money = 100

if "level" not in st.session_state:
    st.session_state.level = 0

if "buff_rate" not in st.session_state:
    st.session_state.buff_rate = 0

if "buff_cost" not in st.session_state:
    st.session_state.buff_cost = 30


# ======================
# 계산 함수
# ======================
def get_cost():
    return int(15 + st.session_state.level * 12)

def get_success_rate():
    return max(0.1, 1 - st.session_state.level * 0.035 + st.session_state.buff_rate)

def sell_value():
    l = st.session_state.level
    return l * 30 + l * l * 10


# ======================
# 게임 기능
# ======================
def upgrade():
    cost = get_cost()

    if st.session_state.money < cost:
        st.error("💸 돈 부족")
        return

    st.session_state.money -= cost

    if random.random() < 0.03:
        st.session_state.level = 0
        st.error("💥 파괴!")
    elif random.random() < get_success_rate():
        st.session_state.level += 1
        st.success("✨ 강화 성공!")
    else:
        st.warning("❌ 실패")


def sell():
    if st.session_state.level == 0:
        st.info("🪨 판매할 검 없음")
        return

    gain = sell_value()
    st.session_state.money += gain
    st.session_state.level = 0

    st.success(f"💰 +{gain}")


def buff():
    if st.session_state.money < st.session_state.buff_cost:
        st.error("💸 돈 부족")
        return

    st.session_state.money -= st.session_state.buff_cost
    st.session_state.buff_rate += 0.08
    st.session_state.buff_cost = int(st.session_state.buff_cost * 1.7)

    st.info("📈 확률 증가")


def risk():
    if st.session_state.money < 80:
        st.error("💸 돈 부족")
        return

    st.session_state.money -= 80

    if random.random() < 0.5:
        gain = 3 + random.randint(0, 3)
        st.session_state.level += gain
        st.success(f"🔥 +{gain} 강화")
    else:
        st.session_state.level = 0
        st.error("💀 파괴!")


def trash():
    st.session_state.money += 1
    st.toast("+1 💰")


# ======================
# UI
# ======================
st.title("⚔️ Enhance RPG Streamlit")

st.metric("💰 Money", st.session_state.money)
st.metric("⚔️ Sword Level", f"+{st.session_state.level}")

st.write("---")

col1, col2 = st.columns(2)

with col1:
    if st.button(f"강화 (-{get_cost()}💰)"):
        upgrade()

    if st.button(f"확률업 (-{st.session_state.buff_cost}💰)"):
        buff()

with col2:
    if st.button(f"판매 (+{sell_value()}💰)"):
        sell()

    if st.button("위험 강화 (-80💰)"):
        risk()

st.write("---")

if st.button("🗑️ 쓰레기통 (+1💰)"):
    trash()

st.caption("Made with Streamlit ⚡")
