# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 실행

```bash
cd C:\AI_simulator
streamlit run app.py
```
브라우저에서 http://localhost:8501 접속.

## 프로젝트 구조

```
app.py                  # Streamlit 진입점 — 모드 토글, 레이아웃 조립, session_state 관리
simulator/
  constants.py          # 모든 정적 데이터 (장비 기본값, 몬스터, 스킬, 스탯 캡)
  models.py             # dataclass: PlayerConfig, MonsterConfig, SimResult, SoloBattleResult, PveResult, PvpResult
  calc.py               # 순수 계산 함수 (장비 스탯, 최종 스탯, 데미지 공식)
  engine.py             # 시뮬레이션 엔진 (run_sim, run_solo_pve_sim, pve_compare, pvp_battle)
ui/
  player_card.py        # 플레이어 설정 패널 (장비/능력치/스킬 탭)
  monster_panel.py      # 몬스터 선택 패널 (PVE 전용)
  pve_results.py        # PVE 결과 (DPS, TTK, 킬수, 차트)
  pvp_results.py        # PVP 결과 (승자, HP 타임라인, 레이더)
  battle_viewer.py      # 방치형 전투 아레나 비주얼 (st.rerun 기반 자동재생)
charts/
  plotly_charts.py      # 모든 Plotly 차트 빌더 함수
```

## 핵심 아키텍처

**데이터 흐름**: `app.py`가 `st.session_state["p1"]`, `["p2"]`, `["monster"]`에 `PlayerConfig` / `MonsterConfig` 객체를 저장 → UI 컴포넌트가 읽고 업데이트 → `engine.py`에서 시뮬레이션 → 결과 패널 렌더링.

### 시뮬레이션 엔진 함수 (`engine.py`)
PVE와 PVP는 **서로 다른 함수**를 사용한다:
- **`run_sim(cfg, target_def, ...)`** — PVP/비교 전용. 루프 기반, 60초, 몬스터 반격 없음.
- **`run_solo_pve_sim(cfg, monster)`** — PVE 전용. `heapq` 이벤트 큐 기반, 몬스터 반격 포함. 처치/사망 시 즉시 리스폰.

**스킬 우선순위**: 항상 `R > W > E > Q > 평타` 순으로 검사하며, 쿨다운과 MP 조건을 모두 만족해야 발동합니다.

### 데미지 공식 (`calc.py:single_hit_dmg`)
```
ATK × (500 / (DEF + 500)) × (1+dmgUp%) × (1−dmgDown%) × (1+modeUp%) × (1−modeDown%) × (coeff/100) × critMult
```
- `DEF_CONST = 500`
- `critMult = 1 + (critChance/100) × (critDmg/100)` — 스킬의 `crit: True`일 때만 적용
- `modeUp/Down`: PVE는 `pve_dmg_up/down`, PVP는 `pvp_dmg_up/down`

### 스탯 캡
모든 상한값은 `simulator/constants.py`의 `CAPS` 딕셔너리에 정의. 계산 전 `min(value, CAPS[...])` 으로 클램프.
주요 캡: ATK% +50, DEF% +50, 공격속도 +300%, 치명타확률 80, 치명타대미지 300, 스킬가속 100.
> **중요**: 스탯 캡은 절대적 상한선이 아닙니다. 밸런스 설계상 조정이 필요하다고 판단되면 **반드시 사용자에게 보고**하고 지시에 따라 조정하십시오.

### 장비 등급 클램프
티어별 최대 등급 초과 시 자동으로 `TIER_MAX_GRADE[tier]`로 클램프 (`calc.py:clamp_grade`).
`TIER_MAX_GRADE`: T1=고급, T2=희귀, T3=고대, T4=영웅, T5=유일, T6~T7=유물.

### 버프 시스템 (`engine.py`)
`active_buffs: dict[str, dict]` → `{type: {expires, value}}` 구조. `run_sim`과 `run_solo_pve_sim` 양쪽에 구현됨.

| type | 효과 | 소비 방식 | 구현 스킬 |
|------|------|-----------|-----------|
| `enhanced_attack` | 다음 평타 계수 N% | 1회 소비 (pop) | 양손검 Q |
| `atk_speed` | 공격속도 +N% → interval 단축 | 시간 만료 | 단검 W, 활 E |
| `def_pct` | DEF +N% | 시간 만료 | 한손검 W |

### MP 시스템
- `MP_REGEN_INTERVAL = 15.0`초 틱마다 `regen_mp`(=3) 회복.
- 스킬 발동 시 `ld["mp"]` 소모. MP 부족 시 해당 스킬 스킵 → 다음 우선순위로 넘어감.
- `max_mp = 360 + (level-1) × 20`

## 데이터 관리 및 워크플로우

- **데이터 소스 분리**:
  - `게임 데이터 전체_원본.csv/`: 원본 데이터가 보관되는 경로입니다.
  - `게임 데이터 전체_수정.csv/`: 수정된 데이터가 임시로 보관되는 경로입니다.
- **수정 및 반영 프로세스**:
  1. 원본 데이터를 수정할 경우, 결과물은 반드시 `게임 데이터 전체_수정.csv/` 경로에 저장합니다.
  2. 실제 게임에 적용이 완료된 후에는 해당 수정 사항을 `게임 데이터 전체_원본.csv/` 폴더에도 동기화하여 반영합니다.
- **누락 테이블 요청**: 시뮬레이터 로직 구현이나 데이터 분석 중 필요한 테이블이 `게임 데이터 전체_원본.csv/` 경로에 없을 경우, **임의로 생성하지 말고 반드시 사용자에게 해당 테이블을 요청**하십시오.

## 스킬 / 데이터 수정

- **패시브 및 장비 모디파이어 (StatModifier)**:
  - **상시 적용(Constant)**: 장비 옵션이나 패시브 스킬처럼 전투 내내 유지되는 수치는 `PlayerConfig` 모델에 필드를 추가하고, `simulator/calc.py`의 최종 스탯 계산 함수(`player_final_atk` 등)에 반영하십시오.
  - **조건부/전투 중 발동(Conditional)**: 특정 조건(예: HP 50% 이하 시 발동)에서만 활성화되는 패시브는 `engine.py` 시뮬레이션 루프 내에서 `active_buffs` 시스템을 활용하여 처리하십시오.
- **문서 동기화 (필수)**: 시뮬레이터 수치나 로직 변경 시, `기획서/` 내의 문서(.xlsx, .html)도 반드시 **동기화**해야 합니다.
- **엑셀 서식 통일성**: 엑셀 형태의 기획서(.xlsx)를 작성하거나 수정할 때, 기존 문서의 **시각적 서식(셀 스타일, 색상, 헤더 양식, 숫자 표기법 등)을 엄격히 유지**하여 일관성을 확보하십시오.
- **배포용 HTML 갱신**: 특히 `기획서/X7_기획서 배포용.html`은 대시보드이므로, 변경된 캡(CAP)이나 공식을 반영하여 즉시 갱신하십시오.
- 스킬 계수·쿨다운 변경 → `simulator/constants.py`의 `SKILLS` 딕셔너리
- 새 무기 타입 추가 → `SKILLS`에 키 추가 + `WEAPON_TYPES` 리스트에 추가
- 장비 기본값 변경 → `constants.py`의 `WPN_BASE` / `ARM_BASE` 등
- 몬스터 스탯 변경 → `MON_BASE` / `MON_GRADE`
- 데미지 공식 변경 → `simulator/calc.py`의 `single_hit_dmg` 함수
- 새 버프 타입 추가 → `engine.py`의 `active_buffs` 처리 블록 양쪽에 적용
- 차트 수정 → `charts/plotly_charts.py`
- 전투 애니메이션 수정 → `ui/battle_viewer.py`
- 새로운 게임 사양 → [GAME_SPEC.md](./GAME_SPEC.md) (Source of Truth)


## 게임 규칙 (필수)

- **스킬 레벨**: 1~5 (0레벨 없음). `SKILLS[weapon][skill]["levels"][lv-1]`로 접근.
- **Varyper 단위**: 천분률 (1000 = 100%, 100 = 10%).
- **스킬가속 공식**: `유효CD = BaseCD × 100 / (100 + n)` (n=100이면 CD 절반).
- **장비 슬롯 9종**: `weapon` / `helmet` / `chest` / `gloves` / `boots` / `ring1` / `ring2` / `neck` / `ear`
- 수식 및 수치 상세는 [GAME_SPEC.md](./GAME_SPEC.md) 참조.
