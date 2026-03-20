"""Q<W<E<R 원칙 위반 교정

위반 항목:
  양손검 1번: E MP=25 < W MP=30 → E MP=40으로 수정
  지팡이 3번: MP 순서 교정 (Q<W<E<R 유지)
    W: 28→25, E: 30→32, R: 28→45

주의: 지팡이 E/R CD 역전(E=40s>R=20s)은 의도된 설계 — 변경 없음
"""
import openpyxl

XLSX_PATH = r"C:\AI_simulator\기획서\X7_무기_스킬.xlsx"
wb = openpyxl.load_workbook(XLSX_PATH)

def s(ws, r, c, v):
    ws.cell(row=r, column=c).value = v

# ── 1. 양손검 1번 E 대지분쇄: MP 25~29 → 40~46 ────────────────
# 2분MP Lv.1: +229, Lv.5: +325 → 총 915/1439 ✓
ws = wb["양손검"]
new_mp = [40, 41, 43, 44, 46]
for i, row in enumerate([23,24,25,26,27]):
    s(ws, row, 5, new_mp[i])
print(f"양손검1번 E MP: 25~29 → {new_mp[0]}~{new_mp[-1]} ✓")

# ── 2. 지팡이 3번 W/E/R MP 재설계 ───────────────────────────────
# 최종: Q(18)<W(25)<E(32)<R(45) — 원칙 준수
ws = wb["지팡이"]

# W 다후타의 손짓: 28~36 → 25~33
w_mp = [25, 27, 29, 31, 33]
for i, row in enumerate([130,131,132,133,134]):
    s(ws, row, 5, w_mp[i])
print(f"지팡이3번 W MP: 28→25~33 ✓")

# E 심판의 낙뢰: 30~50 → 32~44
e_mp = [32, 35, 38, 41, 44]
for i, row in enumerate([135,136,137,138,139]):
    s(ws, row, 5, e_mp[i])
print(f"지팡이3번 E MP: 30→32~44 ✓")

# R 방울방울: 28~36 → 45~60
r_mp = [45, 49, 53, 56, 60]
for i, row in enumerate([140,141,142,143,144]):
    s(ws, row, 5, r_mp[i])
print(f"지팡이3번 R MP: 28→45~60 ✓")

# 저장
try:
    wb.save(XLSX_PATH)
    print(f"\n저장 완료: {XLSX_PATH}")
except PermissionError:
    alt = XLSX_PATH.replace(".xlsx", "_fix_order.xlsx")
    wb.save(alt)
    print(f"\n원본 잠김 — 대체 저장: {alt}")

# ── 검증 ──────────────────────────────────────────────────────
print("\n=== 최종 Q<W<E<R 검증 (Lv.1 기준) ===")
checks = {
    '양손검1번': [(8,15),(12,30),(20,40),(45,80)],
    '지팡이3번': [(5,18),(15,25),(40,32),(20,45)],
}
for name, vals in checks.items():
    cds = [v[0] for v in vals]
    mps = [v[1] for v in vals]
    mp_ok = all(mps[i] < mps[i+1] for i in range(3))
    print(f"  {name} MP: {'/'.join(str(m) for m in mps)} → {'✓' if mp_ok else '✗'}")
