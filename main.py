import streamlit as st
import random

# ======================
# STATE
# ======================
if "money" not in st.session_state:
    st.session_state.money = 100
if "level" not in st.session_state:
    st.session_state.level = 0
if "buff_rate" not in st.session_state:
    st.session_state.buff_rate = 0
if "buff_cost" not in st.session_state:
    st.session_state.buff_cost = 30


def get_cost():
    return int(15 + st.session_state.level * 12)

def get_success_rate():
    return max(0.1, 1 - st.session_state.level * 0.035 + st.session_state.buff_rate)

def sell_value():
    l = st.session_state.level
    return l * 30 + l * l * 10


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
        st.success("✨ 성공!")
    else:
        st.warning("❌ 실패")


def sell():
    if st.session_state.level == 0:
        st.info("검 없음")
        return

    gain = sell_value()
    st.session_state.money += gain
    st.session_state.level = 0
    st.success(f"💰 +{gain}")


def buff():
    if st.session_state.money < st.session_state.buff_cost:
        st.error("💸 부족")
        return

    st.session_state.money -= st.session_state.buff_cost
    st.session_state.buff_rate += 0.08
    st.session_state.buff_cost = int(st.session_state.buff_cost * 1.7)
    st.info("📈 확률 증가")


def risk():
    if st.session_state.money < 80:
        st.error("💸 부족")
        return

    st.session_state.money -= 80

    if random.random() < 0.5:
        gain = 3 + random.randint(0, 3)
        st.session_state.level += gain
        st.success(f"🔥 +{gain}")
    else:
        st.session_state.level = 0
        st.error("💀 파괴")


def trash():
    st.session_state.money += 1
    st.toast("+1💰")


# ======================
# 🎨 CUSTOM UI STYLE
# ======================
st.markdown("""
<style>

/* 배경 */
.stApp {
    background: radial-gradient(circle at top, #1b1f3a, #0b0c14);
    color: white;
}

/* 카드 */
.block-container {
    padding-top: 2rem;
}

/* 메트릭 카드 */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* 버튼 */
.stButton button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(135deg, #7cf7c1, #6ecbff);
    color: black;
    font-weight: bold;
    border: none;
    padding: 10px;
    transition: 0.2s;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
}

/* 텍스트 강조 */
h1 {
    text-align: center;
    color: #7cf7c1;
    text-shadow: 0 0 20px rgba(124,247,193,0.4);
}

</style>
""", unsafe_allow_html=True)


# ======================
# UI
# ======================
st.title("⚔️ ENHANCE RPG")

col1, col2 = st.columns(2)

with col1:
    st.metric("💰 MONEY", st.session_state.money)

with col2:
    st.metric("⚔️ LEVEL", f"+{st.session_state.level}")

st.write("---")

colA, colB = st.columns(2)

with colA:
    if st.button(f"강화 (-{get_cost()}💰)"):
        upgrade()

    if st.button(f"확률업 (-{st.session_state.buff_cost}💰)"):
        buff()

with colB:
    if st.button(f"판매 (+{sell_value()}💰)"):
        sell()

    if st.button("위험강화 (-80💰)"):
        risk()

st.write("---")

if st.button("🗑️ 쓰레기통 (+1💰)"):
    trash()

st.caption("⚡ RPG Enhancement System v2")
