"""한손검/양손검 1,2번 + 활/지팡이/단검 3번 현재 데이터 확인"""
import openpyxl

XLSX_PATH = r"C:\AI_simulator\기획서\X7_무기_스킬.xlsx"
wb = openpyxl.load_workbook(XLSX_PATH)

def dump_rows(sheet_name, start, end):
    ws = wb[sheet_name]
    print(f"\n[{sheet_name}] R{start}~R{end}:")
    for r in range(start, end + 1):
        vals = []
        for c in range(2, 13):  # B~L
            v = ws.cell(row=r, column=c).value
            vals.append(str(v)[:15] if v is not None else "_")
        if any(v != "_" for v in vals):
            print(f"  R{r:3d}: {' | '.join(vals)}")

# 한손검 2번 스킬셋
dump_rows("한손검", 42, 66)
# 양손검 1번 스킬셋
dump_rows("양손검", 10, 35)
# 양손검 2번 스킬셋
dump_rows("양손검", 42, 66)
# 활 3번 스킬셋
dump_rows("활", 80, 105)
# 지팡이 3번 스킬셋
dump_rows("지팡이", 122, 147)
# 단검 3번 스킬셋
dump_rows("단검", 74, 99)
