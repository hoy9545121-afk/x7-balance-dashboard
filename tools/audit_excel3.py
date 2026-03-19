"""
나머지 3T 데이터 및 비교 개요 확인
"""
import openpyxl

BASE = r'C:\AI_simulator\기획서'

def dump_rows(path, sheet, r_from, r_to):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    print(f"\n--- {sheet} R{r_from}~R{r_to} ---")
    for r in range(r_from, r_to+1):
        vals = [ws.cell(row=r, column=c).value for c in range(2, 15)]
        if any(v is not None for v in vals):
            print(f"  R{r}: {vals}")
    wb.close()

SKILL = fr'{BASE}\X7_무기_스킬.xlsx'

# 지팡이 3T R140~160 (방울방울 Lv2~5)
dump_rows(SKILL, '지팡이', 140, 165)

# 활 3T 데이터 (R80~115)
dump_rows(SKILL, '활', 80, 120)

# 양손검 3T 전체 (R77~120)
dump_rows(SKILL, '양손검', 77, 120)

# 한손검 3T 전체 (R77~120)
dump_rows(SKILL, '한손검', 77, 120)

# 무기 비교 개요 전체
dump_rows(SKILL, '무기 비교 개요', 1, 80)
