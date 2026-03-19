# X7 AI Simulator - Technical Specification & Game Logic

This document is the absolute "Source of Truth" for the X7 Combat Simulator. It contains the exact mathematical formulas, data structures, and simulation logic used in the codebase.

---

## 1. Character & Stat Systems

### 1-1. Level Scaling (Level 1-100)
- **Max HP**: $1500 + (Level - 1) \times 100$
- **Max MP**: $360 + (Level - 1) \times 20$
- **HP Regen**: $5$ per tick (Fixed)
- **MP Regen**: $3$ per 15s tick (Fixed, `MP_REGEN_INTERVAL = 15.0`)
- **Base Attack Speed**: $0.91$ (Fixed)

### 1-2. Equipment Stat Calculation
Stats are calculated based on **Tier**, **Grade**, and **Enhancement**.
- **Grade Clamp**: A piece of equipment's grade is capped by its tier: `min(CurrentGrade, TIER_MAX_GRADE[Tier])`.
- **Stat Formula**: $Base[Tier] + GradeBonus[Grade] + (EnhanceValue[Tier] \times EnhancementLevel)$

| Slot | Base [T1/T2/T3/T4/T5/T6/T7] | Grade Bonus [일반/고급/희귀/고대/영웅/유일/유물] | Enhance [T1/T2/T3/T4/T5/T6/T7] |
| :--- | :--- | :--- | :--- |
| **Weapon** | 60 / 80 / 120 / 180 / 260 / 360 / 480 | 0 / 20 / 40 / 60 / 80 / 100 / 120 | 8 / 10 / 12 / 14 / 16 / 18 / 20 |
| **Armor** | 30 / 40 / 60 / 90 / 130 / 180 / 240 | 0 / 10 / 20 / 30 / 40 / 50 / 55 | 4 / 5 / 6 / 7 / 8 / 9 / 10 |
| **Ring** | 0 / 0 / 30 / 45 / 65 / 90 / 120 | 0 / 5 / 10 / 15 / 20 / 25 / 30 | 4 / 5 / 6 / 7 / 8 / 9 / 10 |
| **Neck/Ear**| 0 / 0 / 60 / 90 / 130 / 180 / 240 | 0 / 10 / 20 / 30 / 40 / 50 / 60 | 4 / 5 / 6 / 7 / 8 / 9 / 10 |

### 1-3. Final Stat Aggregation & Caps
Final stats apply percentage modifiers and flat additions, then are clamped by the `CAPS` table.
- **Defense System (Current Policy)**: While both `PhysicalDefenseVary` and `MagicDefenseVary` exist in the data, **only PhysicalDefenseVary is currently utilized**. 
- **Damage Types**: All skill damage is currently treated as **Physical**. This simplification is maintained as the project considers merging Physical and Magic defense into a single "Defense" stat in the future.
- **Final ATK**: $round(BaseATK \times (1 + \frac{min(AtkVary\%, 50)}{100}) + min(AddAtk, 300))$
- **Final DEF**: $round(BaseDEF \times (1 + \frac{min(DefVary\%, 50)}{100}) + min(AddDef, 600))$
- **Atk Speed**: $0.91 \times (1 + \frac{min(AtkSpdVary\%, 300)}{100})$
- **Crit Multiplier**: $1 + (\frac{min(CritChance, 80)}{100} \times \frac{min(CritDmg, 300)}{100})$ (Only for `crit: True` skills)

---

## 2. Combat Mechanics

### 2-1. Damage Formula
$$Damage = ATK \times \frac{500}{DEF + 500} \times (1 + \frac{DmgUp\%}{100}) \times (1 - \frac{DmgDown\%}{100}) \times (1 + \frac{ModeUp\%}{100}) \times (1 - \frac{ModeDown\%}{100}) \times \frac{Coeff}{100} \times CritMult$$
- **DEF_CONST**: $500$
- **ModeUp/Down**: Specifically refers to `PVE_DamageUp` or `PVP_DamageUp` depending on the simulation mode.

### 2-2. Skill Cooldown (Haste)
$$EffectiveCD = round(BaseCD \times \frac{100}{100 + min(SkillAccel, 100)} \times 10) / 10$$
- This creates a linear efficiency: $100$ Skill Accel allows using a skill twice as often.

---

## 3. Simulation Engine Logic

### 3-1. Event-Driven Loop (PVE Mode)
The simulation uses a `heapq` (priority queue) to track events over 60 seconds.
1. **MP Regen**: Every 15s, restore `regen_mp`.
2. **Monster Attack**: Every 1s, the monster hits the player (calculates player's current DEF + buffs).
3. **Player Attack**: 
   - Check **Skill Priority**: `R > W > E > Q > Auto-Attack`.
   - **Condition**: Must not be on Cooldown AND `Current_MP >= Skill_Cost`.
   - **Buff Consumption**: Some skills (like TwohandSword Q) grant an `enhanced_attack` buff. This is consumed on the very next attack (Skill or Auto) to apply a multiplier.
   - **Buff/Debuff Tracking**: Expiration times are tracked per event. Stats (DEF%, AtkSpeed%) are re-calculated dynamically if a buff is active.

### 3-2. Skill Priorities & Weapon Tiers
Currently, only **Tier 3 Skills** are implemented for the following weapon types:

| Weapon | Q (Skill) | W (Skill) | E (Skill) | R (Ultimate) |
| :--- | :--- | :--- | :--- | :--- |
| **TwohandSword** | CD 5s, 200% Dmg + EnhNextAtk | CD 12s, 250% Dmg | CD 15s, 300% Dmg (6-hit) | CD 40s, 400% Dmg |
| **OnehandSword** | CD 6s, 150% Dmg | CD 12s, 200% Dmg + DefBuff | CD 20s, 250% Dmg | CD 45s, 500% Dmg |
| **Bow** | CD 5s, 220% Dmg | CD 12s, 280% Dmg | CD 20s, 350% Dmg + SpdBuff | CD 45s, 500% Dmg |
| **Staff** | CD 4s, 200% Dmg | CD 15s, 400% Dmg (DoT) | CD 40s, 600% Dmg | CD 20s, 300% Dmg + CC |
| **Dagger** | CD 6s, 220% Dmg (Crit) | CD 13s, 120% Dmg + AtkSpdBuff | CD 15s, 250% Dmg | CD 40s, 500% Dmg |

---

## 4. Skill Exceptions & Specific Rules

### 4-1. Bow (활)
- **Explosive Arrow (폭탄화살 - 1T R-Skill)**: 
  - **Logic**: The skill data shows "Direct Damage 500%" and "Explosion Damage 500%". 
  - **Exception**: In actual simulation and gameplay, these do NOT stack. Only one of them applies at a time.
  - **Final Multiplier**: **500%** (Not 1000%).

---

## 5. Monster Data (Normal Grade)

| Tier | HP | ATK | DEF | TTK Goal (0-Enh Player) |
| :--- | :--- | :--- | :--- | :--- |
| **T1** | 418 | 30 | 12 | 5s |
| **T2** | 539 | 46 | 33 | 5s |
| **T3** | 1147 | 118 | 61 | 5s |
| **T4** | 1666 | 178 | 80 | 5s |
| **T5** | 2289 | 268 | 110 | 5s |
| **T6** | 3020 | 364 | 140 | 5s |
| **T7** | 3807 | 486 | 177 | 5s |

### Grade Multipliers

| Grade | ATK Mult | DEF Mult | HP Mult |
| :--- | :---: | :---: | :---: |
| **Normal** | ×1.0 | ×1.0 | ×1.0 |
| **Strong** | ×1.1 | ×1.1 | ×1.2 |
| **Commander** | ×1.2 | ×1.2 | ×1.5 |
| **Elite** | ×1.3 | ×1.3 | ×2.0 |
| **Hero** | ×1.5 | ×1.5 | ×5.0 |
| **Boss** | ×2.0 | ×2.0 | ×15.0 |

---

## 6. Equipment Additional Options (추가옵션 / AddVary System)

장비 획득 시 랜덤으로 부여되는 추가 능력치 시스템. 베이스 능력치 비례 수치와 확률 가중치 설계로 티어 간 가치를 보장한다.

### 6-1. 수치 산출 공식
$$OptionValue_n = \lfloor BaseStat_{tier} \times Pct_n \rfloor$$

- 옵션 번호는 1~6이며, $Pct_n = [5\%, 6\%, 7\%, 8\%, 9\%, 10\%]$ 고정.
- 낮은 수치보다 높은 수치의 등장 확률을 높게 설계하여 풀업 직전의 아쉬움 유발.

### 6-2. 확률 가중치

| 옵션 번호 | 수치 비율 | 등장 확률 | 가중치 |
| :---: | :---: | :---: | :---: |
| 1 | 5% | 10% | 100 |
| 2 | 6% | 10% | 100 |
| 3 | 7% | 10% | 100 |
| 4 | 8% | 20% | 200 |
| 5 | 9% | 20% | 200 |
| 6 | 10% | 30% | 300 |

`Probs = [100, 100, 100, 200, 200, 300]`

### 6-3. 슬롯별 적용 능력치 및 옵션값 테이블

#### 무기 (AddAttackVary)

| Tier | BaseStat | Opt1 | Opt2 | Opt3 | Opt4 | Opt5 | Opt6 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| T1 | 60 | 3 | 3 | 4 | 4 | 5 | 6 |
| T2 | 80 | 4 | 4 | 5 | 6 | 7 | 8 |
| T3 | 120 | 6 | 7 | 8 | 9 | 10 | 12 |

#### 방어구 · 목걸이 · 귀걸이 (AddPhysicalDefenseVary)

T3 방어구, T3 목걸이, T3 귀걸이는 모두 동일한 IAO 그룹(CID=1130)을 공유한다.

| Tier / 슬롯 | BaseStat | Opt1 | Opt2 | Opt3 | Opt4 | Opt5 | Opt6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| T1 방어구 | 30 | 1 | 1 | 2 | 2 | 2 | 3 |
| T2 방어구 | 40 | 2 | 2 | 2 | 3 | 3 | 4 |
| T3 방어구 / 목걸이 / 귀걸이 | 60 | 3 | 3 | 4 | 4 | 5 | 6 |

#### 반지 (AddAttackVary, T3+)

| Tier | BaseStat | Opt1 | Opt2 | Opt3 | Opt4 | Opt5 | Opt6 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| T3 | 30 | 1 | 1 | 2 | 2 | 2 | 3 |

> T1·T2 반지는 추가옵션 없음. T4~T7 무기/방어구/장신구는 향후 확장 예정.

### 6-4. 데이터 CID 참조표

#### StatModified CID

| CID 범위 | 슬롯 | 티어 | Category |
| :--- | :--- | :---: | :--- |
| 80101 ~ 80106 | 무기 | T1 | AttackVary |
| 80201 ~ 80206 | 무기 | T2 | AttackVary |
| 80301 ~ 80306 | 무기 | T3 | AttackVary |
| 81101 ~ 81106 | 방어구 | T1 | PhysicalDefenseVary |
| 81201 ~ 81206 | 방어구 | T2 | PhysicalDefenseVary |
| 81301 ~ 81306 | 방어구 / 목걸이 / 귀걸이 | T3 | PhysicalDefenseVary |
| 82301 ~ 82306 | 반지 | T3 | AttackVary |

CID 체계: `8[slot][tier]0[n]` (slot: 0=무기ATK, 1=방어구DEF, 2=반지ATK / tier: 1~3 / n: 1~6)

#### ItemAdditionalOption CID

### 4-2. 티어별 스킬 GroupId 및 성능 데이터 (v2026-03-19 추가)

기획 데이터(`[X7] 스킬 밸런스 - 스킬 리스트.csv`) 기반의 공식 스킬셋 분류입니다.

| 무기 | 티어 | Q (ID/Dmg/CD) | W (ID/Dmg/CD) | E (ID/Dmg/CD) | R (ID/Dmg/CD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **한손검** | 1T | 100201 / 130% / 6s | 100251 / 160% / 12s | 100301 / 200% / 20s | 100351 / 350% / 45s |
| | 2T | 100401 / 140% / 6s | 100451 / BUFF / 15s | 100501 / BUFF / 25s | 100551 / 400% / 50s |
| | 3T | 100601 / 150% / 6s | 100651 / BUFF / 12s | 100701 / 300% / 18s | 100751 / 500% / 45s |
| **양손검** | 1T | 200401 / 110% / 0s | 200451 / 280% / 12s | 200501 / 330% / 20s | 200551 / 450% / 45s |
| | 2T | 200601 / 100% / 8s | 200651 / 250% / 12s | 200701 / 300% / 20s | 200751 / 400% / 50s |
| | 3T | 200801 / 200% / 5s | 200851 / 250% / 12s | 200901 / 300% / 15s | 200951 / 400% / 40s |
| **활** | 1T | 300401 / 180% / 5s | 300451 / 240% / 12s | 300501 / 280% / 20s | 300551 / 420% / 50s |
| | 2T | 300601 / 200% / 5s | 300651 / 260% / 12s | 300701 / BUFF / 20s | 300751 / 480% / 45s |
| | 3T | 300801 / 220% / 5s | 300851 / 280% / 12s | 300901 / 350% / 20s | 300951 / 500% / 45s |
| **지팡이** | 1T | 400201 / 36% / 8s | 400251 / 200% / 15s | 400301 / 300% / 20s | 400351 / 420% / 50s |
| | 2T | 100001 / 20% / 8s | 100051 / 150% / 15s | 100101 / BUFF / 1s | 100150 / BUFF / 60s |
| | 3T | 400601 / 200% / 4s | 400651 / 400% / 15s | 400701 / 600% / 40s | 400751 / 300% / 20s |
| **단검** | 1T | 500401 / 100% / 5s | 500451 / 70% / 0s | 500501 / 180% / 18s | 500551 / 60% / 45s |
| | 2T | 500601 / 220% / 6s | 500651 / 120% / 10s | 500701 / 250% / 15s | 500751 / 500% / 40s |
| | 3T | 500801 / 220% / 6s | 500851 / 120% / 13s | 500901 / 250% / 15s | 500951 / 500% / 40s |

*참고: 데미지 계수가 없는 항목은 유틸리티/버프 스킬로 시뮬레이션 시 기본 계수(100%) 또는 특수 효과가 적용됩니다.*
