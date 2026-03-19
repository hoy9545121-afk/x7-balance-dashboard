# X7 Economy Simulator - Technical Specification

This document is the **Source of Truth** for the X7 Economy & Progression Simulator. It covers character growth, equipment acquisition, crafting, drop systems, and housing.

**Source Excel files:**
- `기획서/X7_성장_경제_밸런스_통합기획서.xlsx`
- `기획서/X7_장비_제작_및_드랍.xlsx`

---

## 1. Character Growth System

### 1-1. Level XP Formula (Level 1~100)

$$req\_xp(lv) = 4300 \times 1.065^{(lv-1)}$$

$$cumXP(lv) = 4300 \times \frac{1.065^{lv} - 1}{1.065 - 1}$$

- **Growth rate**: ×1.065 per level (6.5% geometric progression)
- **Lv1 XP**: 4,300 | **Lv100 XP**: 2,193,210 | **Total to Lv100**: ~35,868,720 XP

### 1-2. Level Anchor Times (T1 Normal 기준, 500 XP/min)

| Level | Req XP (해당 레벨) | Time (hours) |
| :---: | ---: | ---: |
| 10 | 7,580 | ≈2h |
| 20 | 14,230 | ≈6h |
| 30 | 26,710 | ≈12h |
| 40 | 50,130 | ≈25h |
| 50 | 94,100 | ≈49h |
| 60 | 176,640 | ≈94h |
| 70 | 331,580 | ≈179h |
| 80 | 622,430 | ≈338h |
| 90 | 1,168,380 | ≈636h |
| 100 | 2,193,210 | ≈1196h |

> 기준: T1 Normal 필드 사냥 500 XP/min. 실제 플레이는 티어 진입 후 상위 존 이동으로 단축됨.
> "Req XP" = `req_xp(lv) = 4300 × 1.065^(lv-1)` 해당 레벨 필요 경험치 (개별). 누계 XP는 `cumXP` 공식으로 계산.

### 1-3. Monster XP (Normal 기준)

Base XP per kill is multiplied by **difficulty weight** (see below).

| Tier | Base XP/kill | XP/min (20 kills) | vs T1 |
| :---: | ---: | ---: | ---: |
| T1 | 10 | 200 | ×1.0 |
| T2 | 15 | 300 | ×1.5 |
| T3 | 22 | 440 | ×2.2 |
| T4 | 33 | 660 | ×3.3 |
| T5 | 49 | 980 | ×4.9 |
| T6 | 73 | 1,460 | ×7.3 |
| T7 | 109 | 2,180 | ×10.9 |

> T1 Normal 500 XP/min은 위 200 XP/min에 **×2.5 효율 보정**(스킬 활용, 이동 등)이 반영된 기획 기준치.

### 1-4. Difficulty XP Multipliers

| Difficulty | Multiplier |
| :--- | ---: |
| Normal | ×1.0 |
| Strong | ×1.25 |
| Commander | ×1.5 |
| Elite | ×2.5 |
| Hero | ×4.0 |
| Boss | ×8.0 |

---

## 2. Mastery System (숙련도)

### 2-1. Acquisition Rate

- **Fixed rate**: 300 XP/min (몬스터 등급·티어 무관, 전투 중 획득)
- Gated by current weapon/armor **tier**, not player level.

### 2-2. Tier Mastery Requirements

| Tier | Total Mastery XP | Time to Complete |
| :---: | ---: | ---: |
| T1 | 36,000 | 2h |
| T2 | 72,000 | 4h |
| T3 | 108,000 | 6h |
| T4 | 324,000 | 18h |
| T5 | 1,080,000 | 60h |
| T6 | 1,440,000 | 80h |
| T7 | 2,880,000 | 160h |

> T1→T2 전환: 960 XP. T7 만렙(9단계): 449,260 XP 누계.

### 2-3. Tier Transition Thresholds (Cumulative)

| Transition | Cumulative XP |
| :--- | ---: |
| T1 → T2 | 28,800 |
| T2 → T3 | 49,740 |
| T3 → T4 | 97,200 |
| T4 → T5 | 241,860 |
| T5 → T6 | 601,800 |
| T6 → T7 | 3,105,300 |

---

## 3. Equipment Acquisition Routes

There are **4 routes** to obtain equipment:

| Route | Description | Timing |
| :--- | :--- | :--- |
| **기본 제작** (Basic Craft) | 무기 기본 제작 (T1 only) | Early game |
| **전리품 제작** (Spoils Craft) | 전리품 + 가공물 + 채집물 | Field farming |
| **던전 코어 제작** (Dungeon Core) | 던전 코어 누적 | Dungeon runs |
| **보스 드랍** (Boss Drop) | 보스 처치 시 일정 확률 | Endgame |

---

## 4. Drop Rate Design

### 4-1. Equipment Material Drop Rates (분당 10마리 기준)

| Tier | Drop % / kill | Drops/min (10 kills) | Hours to 100 drops |
| :---: | ---: | ---: | ---: |
| T2 | 8.33% | 0.833 | 2.0h |
| T3 | 3.33% | 0.333 | 5.0h |
| T4 | 1.00% | 0.100 | 16.7h |
| T5 | 0.33% | 0.033 | 50h |
| T6 | 0.13% | 0.013 | 128h |
| T7 | 0.053% | 0.0053 | 315h |

### 4-2. Monster Card Drop Rate

- All monster cards: **1% (100,000 / 10,000,000)** per kill
- LootGroup DropProportion = 100,000

### 4-3. Boss & Special Drops

| Source | Drop |
| :--- | :--- |
| Boss | Equipment material (500111) + Monster Card |
| Dungeon (Ogre) | Special material (2021) + Monster Card |

---

## 5. Spoils Crafting System (전리품 제작)

### 5-1. Material Requirements per Weapon Part (무기 1파츠 기준)

| Tier | Hunt Time | Processed Material (가공물) | Spoils (전리품) | Raw Gather (채집물) |
| :---: | :---: | ---: | ---: | ---: |
| T1 | — | 2 | — | 20 |
| T2 | 12min | 20 | 10 | 200 |
| T3 | 1h | 40 | 20 | 400 |
| T4 | 5h | 60 | 30 | 600 |
| T5 | 25h | 100 | 50 | 1,000 |
| T6 | 125h | 200 | 100 | 2,000 |
| T7 | 625h | 400 | 200 | 4,000 |

> **채집 변환**: 채집물 10개 → 가공물 1개 (Craft.csv)

### 5-2. Craft.csv Material Quantities (Updated Design)

| Tier | Route | 가공물 | 특수재료 | 전리품/코어 |
| :---: | :--- | ---: | ---: | ---: |
| T2 | 전리품(특수) | 8 | 4 | 60 spoils |
| T2 | 던전코어(일반) | 8 | 4 | 3 cores |
| T3 | 전리품(특수) | 24 | 12 | 180 spoils |
| T3 | 던전코어(일반) | 24 | 12 | 15 cores |
| T4 | 던전코어 | 120 | 60 | 45 cores |
| T5 | 던전코어 | 600 | 300 | 150 cores |
| T6 | 던전코어 | 3,000 | 1,500 | 450 cores |
| T7 | 던전코어 | 15,000 | 7,500 | 1,500 cores |

---

## 6. Dungeon Core Crafting System

### 6-1. Core Accumulation Design

| Tier | Target Period | Cores Needed | Dungeon Runs | Daily Investment |
| :---: | :---: | ---: | ---: | :---: |
| T2 | 0.2 days | 3 | 1 | 45 min |
| T3 | 1 day | 15 | 3 | 45 min |
| T4 | 3 days | 45 | 9 | 45 min |
| T5 | 10 days | 150 | 30 | 45 min |
| T6 | 30 days | 450 | 90 | 45 min |
| T7 | 100 days | 1,500 | 300 | 45 min |

> 1회 던전 클리어 시 코어 획득량: T2=3 / T3=5 / T4=5 / T5=5 / T6=5 / T7=5 (설계 기준)

---

## 7. Gathering & Housing System

### 7-1. Gathering Time per Attempt (채집 시간, seconds)

| Tier | Time (s) | per hour | Notes |
| :---: | ---: | ---: | :--- |
| T1 | 3 | 1,200 | Field gather |
| T2 | 1.8 | 2,000 | Fastest tier |
| T3 | 4.5 | 800 | |
| T4 | 15 | 240 | |
| T5 | 45 | 80 | |
| T6 | 112.5 | 32 | |
| T7 | 281.25 | 13 | |

### 7-2. Housing Farm Effect

| Farm Count | Gather/day | Type |
| :---: | ---: | :--- |
| 1개 (밭) | 100 | 일반 (Basic) |
| 10개 (밭) | 1,000 | 프리미엄 (Premium) |

> Housing reduces dependence on active gathering for crafting materials.

---

## 8. Equipment Item List

### 8-1. Item Count Summary

| Tier | Basic Craft | Spoils Craft | Dungeon Core | Boss Drop | Total |
| :---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 12 | — | — | — | 12 |
| T2 | — | 12 | 9 | 3 | 24 |
| T3 | — | 12 | 12 | 15 | 39 |
| **Total** | **12** | **24** | **21** | **18** | **75** |

### 8-2. Item Slot & Material Matrix

| Tier | Route | Helmet | Armor | Gloves | Boots | Notes |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| T1 | Basic | ✅ | ✅ | ✅ | ✅ | 재질별 3종 (판금/가죽/천) |
| T2 | Spoils | ✅(v1+v2) | — | ✅ | ✅ | v1=일반재질, v2=특수재질 |
| T2 | Core | — | ✅(v1+v2) | ✅ | — | 보스드랍=신발 전용 |
| T2 | Boss | — | — | — | ✅ | |
| T3 | Spoils | ✅ | ✅ | ✅(v1+v2) | — | |
| T3 | Core | ✅ | ✅ | ✅ | ✅ | |
| T3 | Boss | ✅ | ✅ | ✅ | ✅ | 다수 변형 존재 |

### 8-3. Passive Count per Tier

| Tier | Passive Count | Notes |
| :---: | :---: | :--- |
| T1 | 1 | 단일 패시브 |
| T2 | 2 | 조합 패시브 |
| T3 | 3 | 3중 조합 패시브 |

### 8-4. Item CID Convention (방어구)

| Range | Route | Slot |
| :--- | :--- | :--- |
| 12020001~09 | T2 전리품(일반) | 투구×3 / 장갑×3 / 신발×3 |
| 12020010~12 | T2 전리품(특수) | 투구 v2×3 |
| 12020013~21 | T2 던전코어 | 갑옷v1×3 / 갑옷v2×3 / 장갑×3 |
| 12020022~24 | T2 보스드랍 | 신발×3 |
| 12030001~12 | T3 전리품 | 투구×3 / 갑옷×3 / 장갑v1×3 / 장갑v2×3 |
| 12030013~24 | T3 던전코어 | 투구×3 / 갑옷×3 / 장갑×3 / 신발×3 |

---

## 9. Crafting Material CID Convention

| CID | Name | Source |
| :--- | :--- | :--- |
| 52020001 | 2T 가공물 | 채집물 10개 → 1개 |
| 53020002 | 2T 전리품 재료 (일반) | 2T 전리품 제작 일반 루트 |
| 53020004 | 2T 전리품 재료 (특수) | 2T 전리품 제작 특수 루트 |
| 52030001 | 3T 가공물 | 채집물 10개 → 1개 |
| 53030002 | 3T 전리품 재료 (일반) | 3T 전리품 제작 일반 루트 |
| 53030006 | 3T 전리품 재료 (특수) | 3T 전리품 제작 특수 루트 |
| 500001 | T2 무기 재료 | T2 필드 드랍 (8.33%) |
| 500002 | T2 방어구 재료 | T2 필드 드랍 (8.33%) |
| 500005 | T3 무기 재료 (하위) | T3 필드 드랍 (2%) |
| 500006 | T3 방어구 재료 (하위) | T3 필드 드랍 (2%) |
| 500007 | T3 무기 재료 (상위) | T3 필드 드랍 (3.33%) |
| 500008 | T3 방어구 재료 (상위) | T3 필드 드랍 (3.33%) |
| 500111 | 보스 장비 재료 | Boss 전용 드랍 |
| 2021 | 오우거 던전 재료 | 오우거 던전 전용 |

---

## 10. Cumulative Acquisition Probability Table

### 10-1. Equipment Material (n회 시도 후 1개 이상 획득 확률)

$$P(\geq 1) = 1 - (1 - p)^n$$

| Tier (p) | 10 kills | 50 kills | 100 kills | 200 kills |
| :--- | ---: | ---: | ---: | ---: |
| T2 (8.33%) | 58.3% | 98.5% | 99.98% | ~100% |
| T3 (3.33%) | 28.7% | 82.4% | 96.5% | 99.9% |
| T4 (1.00%) | 9.6% | 39.5% | 63.4% | 86.6% |
| T5 (0.33%) | 3.3% | 14.7% | 28.0% | 49.2% |
| T6 (0.13%) | 1.3% | 6.2% | 12.1% | 22.8% |
| T7 (0.053%) | 0.5% | 2.6% | 5.1% | 10.0% |

---

*Last updated: 2026-03-18*
*Source files: X7_성장_경제_밸런스_통합기획서.xlsx / X7_장비_제작_및_드랍.xlsx*
