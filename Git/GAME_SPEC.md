# X7 AI Simulator - Technical Specification & Game Logic (v2026-03-19)

이 문서는 X7 프로젝트의 전투 로직 및 밸런스 설계를 정의하는 **최종 명세서**입니다. 본 문서는 시스템 구현을 위한 수학적 수치와 규칙만을 기술합니다.

---

## 1. 캐릭터 스탯 및 공식 (Base Stats)

### 1-1. 기초 성장 공식
- **Max HP**: $1500 + (Lv - 1) \times 100$
- **Max MP**: $360 + (Lv - 1) \times 20$
- **HP/MP 회복**: 15초당 고정 틱 회복 (RegenMpVary = 3)

### 1-2. 장비 기여도
- **최종 ATK**: $Base(Tier) + GradeBonus + EnhanceValue + IAO(AddVary)$
- **최종 DEF**: $\sum(Slot\_Base) + \sum(Grade) + \sum(Enhance) + \sum(IAO)$
- **IAO(추가 옵션)**: 티어별 1~6단계 고정 수치 (AddAttackVary / AddDefenseVary).

### 1-3. 스탯 상한 (Hard Caps)
- **치명타 확률**: 80% (`CriVaryper`)
- **치명타 피해**: 300% (`CriDamageVaryper`)
- **스킬 가속**: 100 (`SkillCooldownAccVary`)
- **공격 속도**: 300% (`AtkSpeedVaryper`)

---

## 2. 데미지 메커니즘 (Combat Formula)

### 2-1. 피해량 산출 공식
$$FinalDMG = ATK \times \frac{500}{DEF + 500} \times SkillCoeff \times TotalMult$$

- **DEF_CONST (500)**: 방어력 500당 생존력이 2배(피해 50% 감소) 증가하는 구조.

### 2-2. 스킬 가속 (Cooldown Reduction)
$$EffectiveCD = BaseCD \times \frac{100}{100 + Accel}$$
- 리니어(Linear) 방식을 채택하여 스택이 쌓여도 과도한 효율 폭주를 방지함.

---

## 3. 직업별 밸런스 및 설계 데이터 (Class Stats)

| 직업 | Q (CD/Dmg) | W (CD/Dmg) | E (CD/Dmg) | R (CD/Dmg) |
| :--- | :--- | :--- | :--- | :--- |
| **양손검** | 5s / 200% | 12s / 250% | 15s / 300% | 40s / 400% |
| **지팡이** | 5s / 200% | 15s / 400% | 40s / 600% | 20s / 300% |
| **단검** | 6s / 220% | 13s / 120% | 15s / 250% | 40s / 500% |
| **한손검** | 6s / 150% | 12s / BUFF | 20s / 250% | 45s / 500% |
| **활** | 5s / 220% | 12s / 280% | 20s / 350% | 45s / 500% |

---

## 4. 데이터 체계 및 CID (System IDs)

### 4-1. 장비 CID 규칙
- **120[Tier][Route][Index]** 형식 준수.
- Route: 기본(01), 전리품(02), 던전(03), 보스(04).

### 4-2. 스킬 GroupId 매핑
- 한손검: 100201~ / 양손검: 200401~ / 지팡이: 400201~ / 활: 300401~ / 단검: 500401~
