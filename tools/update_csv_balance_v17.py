"""
v17 밸런스 재설계 — skill_info.csv 업데이트
수정 후 게임 데이터 전체_수정.csv/skill_info.csv 에 저장

변경 대상:
  활 3번 Q/W/E/R: Lv.1~5 CD/MP 전면 재설계
  지팡이 3번 Q/W/E/R: Lv.1~5 CD/MP 조정
  단검 3번 Q/W/E/R: Lv.1 MP 하향
  한손검 2번 R: Lv.1 CD 50→40s
"""
import csv
import shutil
import os
from pathlib import Path

SRC = Path(r"C:\AI_simulator\게임 데이터 전체_원본.csv\skill_info.csv")
DST = Path(r"C:\AI_simulator\게임 데이터 전체_수정.csv\skill_info.csv")

# 수정 테이블: {root_id: {field: (old, new), ...}}
# cooltime 단위: 밀리초 / cost_m_p: 정수
CHANGES = {
    # ─── 활 3번 Q 충격 사격 Lv.1~5 ─────────────────────────────
    "300001": {"cooltime": (5000, 5000),  "cost_m_p": (10, 10)},   # Lv.1 변경 없음
    "300002": {"cooltime": (3000, 4500),  "cost_m_p": (30, 10)},   # Lv.2
    "300003": {"cooltime": (3000, 4000),  "cost_m_p": (30, 11)},   # Lv.3
    "300004": {"cooltime": (3000, 3500),  "cost_m_p": (30, 12)},   # Lv.4
    "300005": {"cooltime": (3000, 3000),  "cost_m_p": (30, 13)},   # Lv.5

    # ─── 활 3번 R 발묶음 Lv.1~5 ─────────────────────────────────
    "300051": {"cooltime": (45000, 45000), "cost_m_p": (180, 70)},  # Lv.1
    "300052": {"cooltime": (30000, 41000), "cost_m_p": (50,  72)},  # Lv.2
    "300053": {"cooltime": (30000, 37000), "cost_m_p": (50,  74)},  # Lv.3
    "300054": {"cooltime": (30000, 33000), "cost_m_p": (50,  76)},  # Lv.4
    "300055": {"cooltime": (30000, 30000), "cost_m_p": (50,  78)},  # Lv.5

    # ─── 활 3번 E 급습 Lv.1~5 ───────────────────────────────────
    "300151": {"cooltime": (20000, 20000), "cost_m_p": (55, 35)},   # Lv.1
    "300152": {"cooltime": (15000, 18000), "cost_m_p": (30, 35)},   # Lv.2
    "300153": {"cooltime": (15000, 16000), "cost_m_p": (30, 36)},   # Lv.3
    "300154": {"cooltime": (15000, 15000), "cost_m_p": (30, 37)},   # Lv.4
    "300155": {"cooltime": (15000, 14000), "cost_m_p": (30, 38)},   # Lv.5

    # ─── 활 3번 W 연속 쏘기 Lv.1~5 ─────────────────────────────
    "300301": {"cooltime": (12000, 12000), "cost_m_p": (35, 20)},   # Lv.1
    "300302": {"cooltime": (10000, 11000), "cost_m_p": (30, 21)},   # Lv.2
    "300303": {"cooltime": (10000, 10000), "cost_m_p": (30, 22)},   # Lv.3
    "300304": {"cooltime": (10000, 10000), "cost_m_p": (30, 24)},   # Lv.4
    "300305": {"cooltime": (10000, 9000),  "cost_m_p": (30, 26)},   # Lv.5

    # ─── 지팡이 3번 Q 얼음 화살 Lv.1~5 ─────────────────────────
    "400001": {"cooltime": (3000, 5000), "cost_m_p": (30, 18)},     # Lv.1
    "400002": {"cooltime": (2500, 4500), "cost_m_p": (34, 19)},     # Lv.2
    "400003": {"cooltime": (2500, 4000), "cost_m_p": (38, 20)},     # Lv.3
    "400004": {"cooltime": (2000, 3500), "cost_m_p": (41, 21)},     # Lv.4
    "400005": {"cooltime": (2000, 3000), "cost_m_p": (45, 22)},     # Lv.5

    # ─── 지팡이 3번 W 다후타의 손짓 Lv.1~5 ─────────────────────
    "400051": {"cost_m_p": (50, 28)},   # Lv.1 (CD 유지)
    "400052": {"cost_m_p": (55, 30)},   # Lv.2
    "400053": {"cost_m_p": (60, 32)},   # Lv.3
    "400054": {"cost_m_p": (65, 34)},   # Lv.4
    "400055": {"cost_m_p": (70, 36)},   # Lv.5

    # ─── 지팡이 3번 R 방울방울 Lv.1~5 ──────────────────────────
    "400101": {"cost_m_p": (50, 28)},   # Lv.1
    "400102": {"cost_m_p": (55, 30)},   # Lv.2
    "400103": {"cost_m_p": (60, 32)},   # Lv.3
    "400104": {"cost_m_p": (65, 34)},   # Lv.4
    "400105": {"cost_m_p": (70, 36)},   # Lv.5

    # ─── 지팡이 3번 E 심판의 낙뢰 Lv.1~5 (2-node, MP만 변경) ────
    "400151": {"cost_m_p": (50,  30)},  # Lv.1 (모든 2-node 행 동일 적용)
    "400152": {"cost_m_p": (65,  35)},  # Lv.2
    "400153": {"cost_m_p": (80,  40)},  # Lv.3
    "400154": {"cost_m_p": (95,  45)},  # Lv.4
    "400155": {"cost_m_p": (110, 50)},  # Lv.5

    # ─── 단검 3번 Q 추격자의 발톱 Lv.1 (Lv.2~5 CSV 없음) ───────
    "500601": {"cost_m_p": (50, 12)},

    # ─── 단검 3번 W 침묵의 일격 Lv.1 ───────────────────────────
    # CD는 RemovalEffect 기반 별도 파일에서 관리 → 여기서는 MP만
    "500651": {"cost_m_p": (20, 18)},

    # ─── 단검 3번 E 사방의 비수 Lv.1 ───────────────────────────
    "500701": {"cost_m_p": (40, 25)},

    # ─── 단검 3번 R 유혈의 장막 Lv.1 ───────────────────────────
    "500751": {"cost_m_p": (150, 70)},

    # ─── 한손검 2번 R 진공 폭발 Lv.1 (CD 50→40s) ───────────────
    "100551": {"cooltime": (50000, 40000)},
}

# ── 읽기 → 수정 → 쓰기 ──────────────────────────────────────────
with open(SRC, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changed_count = 0
log = []

for row in rows:
    rid = row["root_id"]
    if rid not in CHANGES:
        continue
    patch = CHANGES[rid]
    line_changes = []

    for field, (old, new) in patch.items():
        cur = int(row[field]) if row[field].strip().lstrip("-").isdigit() else row[field]
        if cur != old:
            # 현재값이 예상 old값과 다르면 스킵 (2-node CD 전용 행 보호)
            line_changes.append(f"[SKIP] {rid} {field}: 현재={cur} ≠ 예상={old} (행 스킵)")
            continue
        line_changes.append(f"  {rid} {field}: {old}→{new}")
        row[field] = str(new)
        changed_count += 1

    log.extend(line_changes)

# ── 수정 폴더에 저장 ─────────────────────────────────────────────
DST.parent.mkdir(parents=True, exist_ok=True)
with open(DST, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\n".join(log))
print(f"\n총 수정 셀: {changed_count}")
print(f"저장 완료: {DST}")
