#!/usr/bin/env python3
"""
스킬 밸런스 v16 설계안 (v1.1 상향/너프 반영) → 게임 CSV 적용 스크립트
수정 대상:
  - skill_info.csv       : cooltime, cost_m_p 업데이트
  - skill_damage.csv     : skill_d_m_g_minper/maxper 업데이트
  - StatusChangeRemovalEffect.csv : RemovalEffect-based CD 업데이트
"""

import csv
import shutil
import os
from pathlib import Path
from collections import defaultdict

CSV_DIR = Path(r"C:\AI_simulator\스킬 데이터용 csv")
BACKUP_DIR = CSV_DIR / "_backup_v16"

# ─── 스킬_info 업데이트 (v1.1 반영) ───────────────────────────────────────────
# cd: ms단위, mp: 절대값
SKILL_INFO_UPDATES = {
    # 한손검 3T
    100601: {"cd": 6000,  "mp": 15},   # 성스러운 일격
    100651: {"cd": 12000, "mp": 35},   # 가호의 빛
    100701: {"cd": 20000, "mp": 55},   # 폭주하는 광휘
    100751: {"cd": 45000, "mp": 180},  # 광휘의 심판
    
    # 지팡이 3T: 얼음 화살 (전 레벨 쿨타임 +1s 너프)
    400000: {"cd": 4000,  "mp": 30},
    400001: {"cd": 4000,  "mp": 30},
    400002: {"cd": 3500,  "mp": 34},
    400003: {"cd": 3500,  "mp": 38},
    400004: {"cd": 3000,  "mp": 41},
    400005: {"cd": 3000,  "mp": 45},
    
    # 단검 3T (상향 반영)
    500601: {"cd": 6000,  "mp": 35},   # 추격자의 발톱 (MP 50->35 상향)
    500651: {"cd": None,  "mp": 20},   # 침묵의 일격
    500701: {"cd": 15000, "mp": 40},   # 사방의 비수
    500751: {"cd": 40000, "mp": 150},  # 유혈의 장막 (CD 45s->40s 상향)
}

# ─── 스킬_damage 업데이트 (v1.1 반영) ─────────────────────────────────────────
# 수치: 1000 = 100%
SKILL_DAMAGE_UPDATES = {
    # 한손검 3T
    100751: [5000],   # 상향 (4500 -> 5000)
    
    # 단검 3T (상향 반영)
    500601: [2200],   # 상향 (2000 -> 2200)
    500651: [1200],   # 피해 추가 (0 -> 1200)
    500751: [5000],   # 상향 (4500 -> 5000)
    
    # 지팡이 3T (유지)
    400000: [2000],
    400001: [2000],
}

# ─── StatusChangeRemovalEffect CD 업데이트 ───────────────────────────────────
REMOVAL_EFFECT_UPDATES = {
    # 침묵의 일격 (단검 3T W) - 필요시 쿨타임 조정
    500651: 12000,
}

# ─── 헬퍼 함수 및 로직 ───────────────────────────────────────────────────────

def backup_files():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for fname in ["skill_info.csv", "skill_damage.csv", "StatusChangeRemovalEffect.csv"]:
        src = CSV_DIR / fname
        dst = BACKUP_DIR / fname
        if src.exists():
            shutil.copy2(src, dst)

def read_csv_rows(path: Path):
    if not path.exists(): return [], []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    return rows, fieldnames

def write_csv_rows(path: Path, rows, fieldnames):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def update_skill_info(rows):
    changed = 0
    for row in rows:
        rid = int(row.get("root_id", 0))
        if rid in SKILL_INFO_UPDATES:
            upd = SKILL_INFO_UPDATES[rid]
            if upd["cd"] is not None and row["cooltime"] != str(upd["cd"]):
                row["cooltime"] = str(upd["cd"]); changed += 1
            if upd["mp"] is not None and row["cost_m_p"] != str(upd["mp"]):
                row["cost_m_p"] = str(upd["mp"]); changed += 1
    return changed

def update_skill_damage(rows):
    changed = 0
    for row in rows:
        rid = int(row.get("root_id", 0))
        if rid in SKILL_DAMAGE_UPDATES:
            dmg_list = SKILL_DAMAGE_UPDATES[rid]
            # 단순 1-hit 대응 로직 (v1.1 타겟용)
            new_val = str(dmg_list[0])
            if row["skill_d_m_g_minper"] != new_val:
                row["skill_d_m_g_minper"] = new_val
                row["skill_d_m_g_maxper"] = new_val
                changed += 1
    return changed

def main():
    print("X7 스킬 밸런스 v1.1 최신화 중...")
    backup_files()
    
    # Info 업데이트
    si_path = CSV_DIR / "skill_info.csv"
    si_rows, si_fields = read_csv_rows(si_path)
    if si_rows:
        cnt = update_skill_info(si_rows)
        write_csv_rows(si_path, si_rows, si_fields)
        print(f"  skill_info.csv 업데이트 완료 ({cnt}개 항목 변경)")

    # Damage 업데이트
    sd_path = CSV_DIR / "skill_damage.csv"
    sd_rows, sd_fields = read_csv_rows(sd_path)
    if sd_rows:
        cnt = update_skill_damage(sd_rows)
        write_csv_rows(sd_path, sd_rows, sd_fields)
        print(f"  skill_damage.csv 업데이트 완료 ({cnt}개 항목 변경)")

    print("모든 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()
