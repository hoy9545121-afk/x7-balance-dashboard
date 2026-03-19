#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X7_기획서 배포용.html 에서 inline JS를 분리하고
onclick/oninput 속성을 data-* 속성으로 교체하는 스크립트.
"""

import re
import os

HTML_PATH = r"C:\AI_simulator\기획서\X7_기획서 배포용.html"
JS_PATH   = r"C:\AI_simulator\기획서\X7_dashboard.js"

# ─────────────────────────────────────────────────────────────
# STEP 1: HTML 파일 읽기
# ─────────────────────────────────────────────────────────────
with open(HTML_PATH, encoding="utf-8") as f:
    html = f.read()

print(f"[STEP 1] HTML 읽기 완료. 총 {len(html)} 바이트.")

# ─────────────────────────────────────────────────────────────
# STEP 2: <script>...</script> 블록 2개 추출 → JS 합치기
# ─────────────────────────────────────────────────────────────
# DOTALL 플래그로 멀티라인 매칭
script_pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL)
script_blocks  = script_pattern.findall(html)

print(f"[STEP 2] <script> 블록 발견: {len(script_blocks)}개")
assert len(script_blocks) == 2, f"script 블록이 2개여야 하는데 {len(script_blocks)}개 발견!"

# 두 블록 합치기
js_combined = script_blocks[0].strip() + "\n\n" + script_blocks[1].strip()

# ─────────────────────────────────────────────────────────────
# STEP 2-b: INIT 직접 호출 4줄 제거 (DOMContentLoaded 안으로 이동 예정)
# ─────────────────────────────────────────────────────────────
# 마지막 script 블록 끝의 INIT 주석 + 4줄 직접 호출 제거
init_pattern = re.compile(
    r'\n*// ═+\s*INIT\s*═+\s*\n'
    r'renderArmorTier\(\'1T\'\);\s*renderArmorTier\(\'2T\'\);\s*renderArmorTier\(\'3T\'\);\s*\n'
    r'renderDPS\(\);\s*\n'
    r'renderWeaponTier\(\'1\'\);\s*renderWeaponTier\(\'2\'\);\s*renderWeaponTier\(\'3\'\);\s*\n'
    r'renderItemList\(\);\s*'
)
js_combined_clean, n_init = init_pattern.subn('', js_combined)
if n_init == 0:
    # 줄 단위로 4줄을 직접 찾아서 제거 (패턴이 조금 다를 경우 대비)
    lines = js_combined.split('\n')
    init_lines = {
        "renderArmorTier('1T'); renderArmorTier('2T'); renderArmorTier('3T');",
        "renderDPS();",
        "renderWeaponTier('1'); renderWeaponTier('2'); renderWeaponTier('3');",
        "renderItemList();",
    }
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped in init_lines or stripped == "// ═══════════ INIT ═══════════":
            continue
        new_lines.append(line)
    js_combined_clean = '\n'.join(new_lines)
    print("[STEP 2] INIT 4줄을 줄 단위로 제거했습니다.")
else:
    print(f"[STEP 2] INIT 블록 정규식으로 {n_init}개 제거.")

# 또한 첫 번째 script 블록 끝의 renderGrowthLevel(); 단독 호출도 제거
# (DOMContentLoaded 안에는 넣지 않음 — 이 함수는 탭 전환 시 lazy 렌더이므로 그대로 둬도 되지만
#  원 코드에 직접 호출이 있으면 DOMContentLoaded 이전에도 실행됨. 여기서는 제거하지 않는다.
#  — renderGrowthLevel()은 INIT 4줄과 별개이므로 유지.)

print(f"[STEP 2] JS 코드 추출 완료. 총 {len(js_combined_clean)} 바이트.")

# ─────────────────────────────────────────────────────────────
# STEP 3: HTML에서 onclick / oninput 교체
# ─────────────────────────────────────────────────────────────

def replace_attrs(html_text):

    # 3-1 + 3-2: showSection('XXX') → data-action="nav" data-s="XXX"
    # nav 버튼은 이미 data-s 있음 → onclick만 제거하고 data-action 추가
    # cat-item div는 data-s 없음 → 둘 다 추가
    # 통합: 모든 onclick="showSection('XXX')" → data-action="nav" data-s="XXX"
    html_text = re.sub(
        r'''onclick="showSection\('([^']+)'\)"''',
        lambda m: f'data-action="nav" data-s="{m.group(1)}"',
        html_text
    )

    # 3-3: switchTab('SECTION','TAB',this) → data-action="tab" data-s="SECTION" data-t="TAB"
    html_text = re.sub(
        r'''onclick="switchTab\('([^']+)','([^']+)',this\)"''',
        lambda m: f'data-action="tab" data-s="{m.group(1)}" data-t="{m.group(2)}"',
        html_text
    )

    # 3-4: filterList('TYPE','VAL',this) → data-action="filter-list" data-type="TYPE" data-val="VAL"
    html_text = re.sub(
        r'''onclick="filterList\('([^']+)','([^']+)',this\)"''',
        lambda m: f'data-action="filter-list" data-type="{m.group(1)}" data-val="{m.group(2)}"',
        html_text
    )

    # 3-5: filterArmor('TYPE','VAL',this) → data-action="filter-armor" data-type="TYPE" data-val="VAL"
    html_text = re.sub(
        r'''onclick="filterArmor\('([^']+)','([^']+)',this\)"''',
        lambda m: f'data-action="filter-armor" data-type="{m.group(1)}" data-val="{m.group(2)}"',
        html_text
    )

    # 3-6: oninput="searchArmor(this.value)" → data-action="search-armor"
    html_text = re.sub(
        r'''oninput="searchArmor\(this\.value\)"''',
        'data-action="search-armor"',
        html_text
    )

    return html_text

html_modified = replace_attrs(html)

# ─────────────────────────────────────────────────────────────
# STEP 4: <script>...</script> 블록 2개 제거 + 외부 스크립트 링크 삽입
# ─────────────────────────────────────────────────────────────

# script 블록 제거 (공백 줄도 정리)
html_modified = re.sub(r'\n*<script>.*?</script>', '', html_modified, flags=re.DOTALL)

# </body> 바로 앞에 외부 JS 삽입
html_modified = html_modified.replace(
    '</body>',
    '<script src="./X7_dashboard.js"></script>\n</body>'
)

print("[STEP 4] <script> 블록 제거 및 외부 스크립트 링크 삽입 완료.")

# ─────────────────────────────────────────────────────────────
# STEP 5: X7_dashboard.js 생성 + delegated handler 추가
# ─────────────────────────────────────────────────────────────

delegated_handler = '''

// ═══════════ DELEGATED EVENT HANDLERS ═══════════
document.addEventListener('DOMContentLoaded', function() {
  // Click delegation
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('[data-action]');
    if (!btn) return;
    var action = btn.dataset.action;
    if (action === 'nav') {
      showSection(btn.dataset.s);
    } else if (action === 'tab') {
      switchTab(btn.dataset.s, btn.dataset.t, btn);
    } else if (action === 'filter-list') {
      filterList(btn.dataset.type, btn.dataset.val, btn);
    } else if (action === 'filter-armor') {
      filterArmor(btn.dataset.type, btn.dataset.val, btn);
    }
  });

  // Input delegation for armor search
  document.addEventListener('input', function(e) {
    if (e.target.dataset.action === 'search-armor') {
      searchArmor(e.target.value);
    }
  });

  // Init
  renderArmorTier('1T'); renderArmorTier('2T'); renderArmorTier('3T');
  renderDPS();
  renderWeaponTier('1'); renderWeaponTier('2'); renderWeaponTier('3');
  renderItemList();
});
'''

js_final = js_combined_clean.rstrip() + delegated_handler

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_final)

print(f"[STEP 5] X7_dashboard.js 저장 완료. {len(js_final)} 바이트.")

# ─────────────────────────────────────────────────────────────
# HTML 파일 저장
# ─────────────────────────────────────────────────────────────
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_modified)

print(f"[SAVE] HTML 파일 저장 완료. {len(html_modified)} 바이트.")

# ─────────────────────────────────────────────────────────────
# STEP 6: 검증
# ─────────────────────────────────────────────────────────────
print("\n" + "="*50)
print("[STEP 6] 검증 결과")
print("="*50)

# 다시 읽어서 검증
with open(HTML_PATH, encoding="utf-8") as f:
    html_check = f.read()

onclick_count  = len(re.findall(r'onclick=', html_check))
oninput_count  = len(re.findall(r'oninput=', html_check))
script_inline  = len(re.findall(r'<script>', html_check))
script_ext     = len(re.findall(r'<script src="./X7_dashboard\.js">', html_check))

print(f"  onclick= 개수      : {onclick_count}  (목표: 0)")
print(f"  oninput= 개수      : {oninput_count}  (목표: 0)")
print(f"  inline <script> 개수: {script_inline}  (목표: 0)")
print(f"  외부 script 링크   : {script_ext}  (목표: 1)")

# JS 파일 검증
js_size = os.path.getsize(JS_PATH)
print(f"  X7_dashboard.js 크기: {js_size} 바이트  (목표: >0)")

all_ok = (onclick_count == 0 and oninput_count == 0
          and script_inline == 0 and script_ext == 1
          and js_size > 0)

print()
if all_ok:
    print("[결과] 모든 검증 통과!")
else:
    print("[결과] 일부 검증 실패. 위 항목을 확인하세요.")

# data-action 분포 확인 (보너스 정보)
nav_count         = len(re.findall(r'data-action="nav"', html_check))
tab_count         = len(re.findall(r'data-action="tab"', html_check))
filter_list_count = len(re.findall(r'data-action="filter-list"', html_check))
filter_arm_count  = len(re.findall(r'data-action="filter-armor"', html_check))
search_arm_count  = len(re.findall(r'data-action="search-armor"', html_check))

print()
print("[BONUS] data-action 분포:")
print(f"  nav          : {nav_count}")
print(f"  tab          : {tab_count}")
print(f"  filter-list  : {filter_list_count}")
print(f"  filter-armor : {filter_arm_count}")
print(f"  search-armor : {search_arm_count}")
