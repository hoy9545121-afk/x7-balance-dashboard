# 시뮬레이터 갱신용 CSV 파일 목록

> **경로**: `C:\AI_simulator\스킬 데이터용 csv\` (또는 동일 내용의 Obsidian Vault 경로)
> **용도**: 시뮬레이터(`simulator/constants.py`, `engine.py`)를 게임 데이터에 맞게 갱신할 때 참조

---

## 1. 스킬 기본 정보

### `skill_info.csv`
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `root_id` | 스킬 식별자 (Lv1 기준) | SKILLS dict 키 |
| `root_name` | 스킬명 | `"name"` 필드 |
| `cooltime` | 쿨다운 (ms) | `"cd"` (÷1000으로 초 변환) |
| `cost_m_p` | MP 소모량 | `"mp"` 필드 |

> **업데이트 스크립트**: `tools/apply_skill_balance_v16.py`

---

### `skill_damage.csv`
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `root_id` | 스킬 식별자 | SKILLS dict |
| `skill_d_m_g_minper` | 피해 계수 최솟값 (千分率) | `"dmg"` (÷10으로 % 변환) |
| `skill_d_m_g_maxper` | 피해 계수 최댓값 | 동일 (`minper`와 같으면 고정값) |
| `status_tag_condition_cids` | 조건 발동 여부 | `[]`인 행만 적용 (무조건 피해) |

> **단위 주의**: CSV 값 1000 = 100% → 시뮬레이터에서는 ÷10 적용

---

## 2. 버프 / 상태이상 체계

### `skill_effect.csv`
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `root_id` | 스킬 식별자 | 매핑 키 |
| `status_change_cids` | 적용할 StatusChange OID 목록 | SKILLS `"buff"` 키 설계 근거 |
| `remove_status_change_cids` | 이 스킬 사용 시 제거할 버프 목록 | (현재 미구현) |

> **버프 설계 시작점**: 이 파일에서 `status_change_cids`가 비어있지 않은 스킬 탐색

---

### `StatusChangeInfo.csv`
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `OID` / `Cid` | 상태이상 식별자 | `status_change_cids` 값과 매칭 |
| `DurationMin` / `DurationMax` | 지속 시간 (ms) | SKILLS `"buff"."duration"` (÷1000) |
| `Negative` | `true`=디버프(적에게 적용), `false`=버프(자신에게 적용) | `false`인 항목만 플레이어 버프로 처리 |
| `StatusChangeEffectCids` | 실제 효과 OID | 다음 단계로 연결 |

---

### `StatusChangeEffect.csv`
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `OID` / `Cid` | 효과 식별자 | `StatusChangeEffectCids` 값과 매칭 |
| `StatModifiedCids` | 스탯 수치 OID 목록 | 다음 단계로 연결 |
| `CrowdControls` | CC 효과 (Stun, Floating 등) | 현재 미구현 |
| `ReplaceNormalSkillId` | 강화 평타 스킬 ID | `enhanced_attack` 타입 버프 설계 근거 |

---

### `StatModified.csv`
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `OID` / `Cid` | 스탯 수치 식별자 | `StatModifiedCids` 값과 매칭 |
| `Category` | 스탯 종류 | 아래 매핑표 참조 |
| `Value` | 수치 (千分率) | SKILLS `"buff"."value"` (÷10으로 % 변환) |

#### Category → 시뮬레이터 버프 타입 매핑
| CSV Category | 시뮬레이터 buff type | 설명 | 현재 구현 |
|---|---|---|---|
| `AtkSpeedVaryper` | `atk_speed` | 공격 속도 % 증가 | ✅ |
| `DefenseVaryper` | `def_pct` | 방어력 % 증가 | ✅ |
| `MoveSpeedVaryper` | (미구현) | 이동 속도 — DPS 무관 | ❌ skip |
| `AttackVary` | (미구현) | 공격력 고정값 증가 | ❌ 미구현 |
| `AttackVaryper` | (미구현) | 공격력 % 증가 | ❌ 미구현 |
| `CriDamageVaryper` | (미구현) | 치명타 피해 증가 | ❌ 미구현 |
| `CriVaryper` | (미구현) | 치명타 확률 증가 | ❌ 미구현 |
| `SkillCooldownAccVary` | (미구현) | 스킬 가속 | ❌ 미구현 |

---

### `StatusChangeRemovalEffect.csv`
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `Cooldown` | 버프 만료 시 발동되는 스킬 쿨다운 (ms) | SKILLS `"cd"` 설계 시 합산 필요 |
| `CooldownTargetSkillId` | 쿨다운이 부여될 스킬 ID | 해당 스킬 `"cd"` 값에 반영 |

> **적용 예**: 단검 W 침묵의일격 — 버프 5s + RemovalEffect CD 8s = 총 사이클 13s

---

## 3. 기본 캐릭터 스탯

### `CharacterStat.csv` (또는 추출본)
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| `Lv` | 레벨 | `LEVEL_TABLE` 인덱스 |
| `MaxHpVary` | 최대 HP | `LEVEL_TABLE[i]["max_hp"]` |
| `MaxMpVary` | 최대 MP | `LEVEL_TABLE[i]["max_mp"]` |
| `RegenHpVary` | HP 자연회복/틱 | `LEVEL_TABLE[i]["regen_hp"]` |
| `RegenMpVary` | MP 자연회복/틱 | `LEVEL_TABLE[i]["regen_mp"]` |
| `CriVaryper` | 기본 치명타 확률 (千분율) | `PlayerConfig.crit_chance` 기본값 |
| `CriDamageVaryper` | 기본 치명타 피해 (千분율) | `PlayerConfig.crit_dmg` 기본값 |

---

## 4. 장비 스탯

### 무기 / 방어구 기본값
현재 시뮬레이터 하드코딩 값 (`simulator/constants.py`의 `WPN_BASE`, `ARM_BASE` 등).
게임 DB에서 변경 시 아래 상수를 동기화:

| 시뮬레이터 상수 | 출처 컬럼 | 단위 |
|---|---|---|
| `WPN_BASE[tier]` | Weapon.AttackVary (기본 등급) | 정수 |
| `WPN_ENH[tier]` | Weapon 강화 1회당 ATK 증가 | 정수 |
| `ARM_BASE[tier]` | Armor.DefenseVary (기본 등급) | 정수 |
| `ARM_ENH[tier]` | Armor 강화 1회당 DEF 증가 | 정수 |

---

## 5. 몬스터 스탯

### `Monster.csv` (또는 DB 추출본)
| 컬럼 | 설명 | 시뮬레이터 반영 위치 |
|------|------|---------------------|
| 몬스터 종류·등급 | Normal/Strong/Commander 등 | `MonsterConfig.monster_type` |
| HP | 최대 HP | `MON_BASE[tier]["hp"]` 계산 기준 |
| ATK | 공격력 | `MON_BASE[tier]["atk"]` |
| DEF | 방어력 | `MON_BASE[tier]["def"]` |

> **현재 값**: `constants.py`의 `MON_BASE` / `MON_GRADE` (2026-03-03 DPS 기준 재계산)

---

## 빠른 참조: 밸런스 수정 흐름

```
스킬 CD / MP 변경
  → skill_info.csv (cooltime, cost_m_p 컬럼)
  → constants.py SKILLS[weapon]["levels"][lv]["cd"/"mp"]

스킬 피해 계수 변경
  → skill_damage.csv (skill_d_m_g_minper 컬럼, ×10해서 시뮬레이터 단위)
  → constants.py SKILLS[weapon]["levels"][lv]["dmg"]

RemovalEffect 쿨다운 변경
  → StatusChangeRemovalEffect.csv (Cooldown 컬럼)
  → constants.py SKILLS[weapon]["levels"][lv]["cd"] (버프 지속 + RemovalEffect CD 합산)

버프 효과 추가 / 수정
  → skill_effect.csv → StatusChangeInfo → StatusChangeEffect → StatModified 체인 탐색
  → constants.py SKILLS[weapon]["buff"]["type"/"duration"/"value"]
  → engine.py active_buffs 처리 로직에 새 타입 추가 (필요 시)

몬스터 HP / ATK / DEF 변경
  → constants.py MON_BASE / MON_GRADE

캐릭터 HP / MP / 회복 변경
  → constants.py LEVEL_TABLE
```
