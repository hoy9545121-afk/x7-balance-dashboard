"""전투 시뮬레이터 — Streamlit 메인 앱 (사이드바 설정 + 메인 전투 아레나)"""
import streamlit as st
from simulator.models import PlayerConfig, MonsterConfig
from simulator.engine import pve_compare, pvp_battle
from ui.player_card import render_player_config
from ui.monster_panel import render_monster_config
from ui.battle_viewer import render_pve_battle_arena, render_pvp_battle_arena
from ui.pve_results import render_pve_results
from ui.pvp_results import render_pvp_results
from ui.growth_view import render_growth_view

# 설정
st.set_page_state = {
    "layout": "wide",
    "page_title": "X7 전투 시뮬레이터",
}
st.set_page_config(layout="wide", page_title="X7 전투 시뮬레이터")

# 스타일 커스텀 (시인성 대폭 강화)
st.markdown("""
<style>
  /* 기본 배경 */
  .stApp { background-color: #060b14; color: #c8d8e8; }
  
  /* 아코디언 헤더 (몬스터, 플레이어 패널) 디자인 개선 */
  .st-emotion-cache-p5mtransition {
    background-color: rgba(11, 18, 32, 0.95) !important;
    border: 1px solid #1e3048 !important;
    border-radius: 8px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
  }
  .st-emotion-cache-p5mtransition:hover {
    border-color: #e8b84b !important;
  }
  
  /* 아코디언 글자색 강조 */
  .st-emotion-cache-p5mtransition span {
    color: #e8b84b !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.05rem;
  }

  /* 라디오 버튼 및 탭 색상 */
  .st-emotion-cache-1cvow48 { color: #e8b84b !important; }
  
  button[data-baseweb="tab"] {
    color: #7a9ab8 !important;
    font-weight: 600 !important;
  }
  button[data-baseweb="tab"][aria-selected="true"] {
    color: #e8b84b !important;
    border-bottom-color: #e8b84b !important;
  }

  /* 닫힌 selectbox 박스 자체 */
  [data-baseweb="select"] > div,
  [data-baseweb="select"] > div:hover,
  [data-baseweb="select"] > div:focus-within,
  div[data-testid="stSelectbox"] > div {
    background: #0d1a28 !important;
    background-color: #0d1a28 !important;
    border-color: #1e3048 !important;
  }

  /* 박스 안 모든 텍스트 */
  [data-baseweb="select"] span,
  [data-baseweb="select"] input,
  [data-baseweb="select"] [class*="placeholder"],
  [data-baseweb="select"] [class*="singleValue"],
  [data-baseweb="select"] [class*="ValueContainer"],
  div[data-testid="stSelectbox"] span {
    color: #dce8f5 !important;
    background-color: transparent !important;
  }
  
  /* 메트릭 폰트 크기 조정 */
  [data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    color: #e8b84b !important;
  }
</style>
""", unsafe_allow_html=True)

st.title("⚔ X7 전투 시뮬레이터")

# 1. 사이드바 - 전역 설정
with st.sidebar:
    st.header("⚙ 모드 설정")
    mode = st.radio("시뮬레이션 모드", ["PVE", "PVP", "📈 성장 밸런스"], horizontal=False)
    st.divider()
    st.info("💡 전투 및 성장 데이터를 시뮬레이션하여 밸런스를 검증하세요.")

# 세션 상태 초기화
# ... (기존 코드 유지)
if "p1" not in st.session_state:
    st.session_state["p1"] = PlayerConfig(weapon_type="양손검")
if "p2" not in st.session_state:
    st.session_state["p2"] = PlayerConfig(weapon_type="한손검")
if "monster" not in st.session_state:
    st.session_state["monster"] = MonsterConfig()

# 2. 메인 화면 레이아웃
if mode == "PVE":
    m_col, p1_col, p2_col = st.columns([1, 1, 1])
    # ... (기존 PVE 렌더링 코드)
    with m_col:
        st.session_state["monster"] = render_monster_config()
    with p1_col:
        st.session_state["p1"] = render_player_config("Player 1", st.session_state["p1"])
    with p2_col:
        st.session_state["p2"] = render_player_config("Player 2 (비교군)", st.session_state["p2"])

    p1 = st.session_state["p1"]
    p2 = st.session_state["p2"]
    monster = st.session_state["monster"]

    result = pve_compare(p1, p2, monster)
    render_pve_battle_arena(result, p1, p2, monster)
    st.markdown("<br>", unsafe_allow_html=True)
    render_pve_results(result, p1, p2, monster)

elif mode == "PVP":
    # PVP 모드
    c1, c2 = st.columns(2)
    # ... (기존 PVP 렌더링 코드)
    with c1:
        st.session_state["p1"] = render_player_config("Player 1 (Left)", st.session_state["p1"])
    with c2:
        st.session_state["p2"] = render_player_config("Player 2 (Right)", st.session_state["p2"])
    
    p1 = st.session_state["p1"]
    p2 = st.session_state["p2"]
    
    result = pvp_battle(p1, p2)
    render_pvp_battle_arena(result, p1, p2)
    st.markdown("<br>", unsafe_allow_html=True)
    render_pvp_results(result, p1, p2)

else:
    # 📈 성장 밸런스 모드
    render_growth_view()
