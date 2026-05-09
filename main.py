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


# ======================
# GAME LOGIC
# ======================
MAX_LEVEL = 25

def get_cost():
    return int(15 + st.session_state.level * 12)

def get_success_rate():
    return max(0.1, 1 - st.session_state.level * 0.035 + st.session_state.buff_rate)

def sell_value():
    l = st.session_state.level
    return l * 30 + l * l * 10

def get_sword_name():
    l = st.session_state.level

    if l == 0:
        return "🗡️ 녹슨 개복치 검"
    elif l < 5:
        return "🗡️ 운빨 강화 칼"
    elif l < 10:
        return "🗡️ 강화 중독자의 검"
    elif l < 20:
        return "🗡️ 전설 후보 검"
    elif l < MAX_LEVEL:
        return "🗡️ 신화 직전 검"
    else:
        return "👑 MAX 신의 검"


# ======================
# ACTIONS
# ======================
def upgrade():
    if st.session_state.level >= MAX_LEVEL:
        st.error("⚠️ 최대 강화 도달")
        return

    cost = get_cost()
    if st.session_state.money < cost:
        st.error("💸 돈 부족")
        return

    st.session_state.money -= cost

    # 파괴 확률
    if random.random() < 0.03:
        st.session_state.level = 0
        st.error("💥 파괴!")
        return

    if random.random() < get_success_rate():
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
        st.session_state.level = min(MAX_LEVEL, st.session_state.level + gain)
        st.success(f"🔥 +{gain}")
    else:
        st.session_state.level = 0
        st.error("💀 전부 파괴")


def trash():
    st.session_state.money += 1
    st.toast("+1 💰")


# ======================
# UI STYLE
# ======================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1b1f3a, #0b0c14);
    color: white;
}

/* 카드 */
.block-container {
    padding-top: 2rem;
}

/* metric */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.1);
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

/* 제목 */
h1 {
    text-align: center;
    color: #7cf7c1;
}
</style>
""", unsafe_allow_html=True)


# ======================
# HEADER
# ======================
st.title("⚔️ ENHANCE RPG ULTIMATE")

# ======================
# STATUS
# ======================
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="padding:15px;background:rgba(255,215,107,0.1);border-radius:12px">
    <h3>💰 MONEY</h3>
    <h2 style="color:#ffd86b">{st.session_state.money}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="padding:15px;background:rgba(124,247,193,0.1);border-radius:12px">
    <h3>⚔️ LEVEL</h3>
    <h2 style="color:#7cf7c1">+{st.session_state.level}</h2>
    </div>
    """, unsafe_allow_html=True)

# ======================
# SWORD NAME
# ======================
st.markdown(f"""
<div style="
margin:15px 0;
padding:15px;
text-align:center;
background:rgba(255,255,255,0.05);
border-radius:12px;
border:1px solid rgba(255,255,255,0.1);
">
<h2>{get_sword_name()}</h2>
</div>
""", unsafe_allow_html=True)

# ======================
# BUTTONS
# ======================
colA, colB = st.columns(2)

with colA:
    st.button(f"⚔️ 강화 (-{get_cost()}💰)", on_click=upgrade)
    st.button(f"📈 확률업 (-{st.session_state.buff_cost}💰)", on_click=buff)

with colB:
    st.button(f"💰 판매 (+{sell_value()}💰)", on_click=sell)
    st.button("💣 위험강화 (-80💰)", on_click=risk)

st.write("---")

st.button("🗑️ 쓰레기통 (+1💰)", on_click=trash)

# ======================
# FOOTER
# ======================
st.caption("⚡ Full RPG Enhancement System - Streamlit Edition")
