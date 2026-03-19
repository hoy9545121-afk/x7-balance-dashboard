"""overview 섹션 재설계 — 장비 체계(티어/등급/무기/방어구) 중심으로"""
import re, shutil

HTML_PATH = r"C:\AI_simulator\기획서\X7_대시보드.html"
HTML_SYNC = r"C:\Users\hoy5343\Documents\카카오톡 받은 파일\index.html"

with open(HTML_PATH, encoding="utf-8") as f:
    html = f.read()

# 기존 cat-tree 보존
cat_m = re.search(r'(<div class="cat-tree">.*?</div><!-- /cat-tree -->)', html, re.DOTALL)
cat_html = cat_m.group(1) if cat_m else ""

NEW_OVERVIEW = """\
<section class="section active" id="sec-overview">

  <!-- 인트로 -->
  <div class="notice-card" style="margin-bottom:20px">
    <span class="notice-char">👑</span>
    <div class="notice-text">
      <strong>X7 프로젝트 밸런스 대시보드</strong> — 성장·경제·전투 밸런스 수치를 한눈에 볼 수 있는 기획 레퍼런스입니다. 준비 중 항목은 기획서 업로드 시 자동으로 채워집니다.
    </div>
  </div>

  <!-- 장비 체계: 티어 & 등급 -->
  <div style="margin-bottom:14px">
    <div class="card">
      <div class="card-head"><span style="color:var(--gold)">⚙ 장비 체계</span></div>
      <div style="padding:16px 20px;display:grid;grid-template-columns:1fr 1fr;gap:28px">

        <div>
          <div style="font-size:.72rem;color:var(--text2);letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">
            Tier — 장비에 고유하게 부여, 성장으로 변경 불가
          </div>
          <div style="display:flex;gap:6px;flex-wrap:wrap">
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(80,200,112,.18);color:#50c870;border:1px solid #50c87050">T1</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(130,205,90,.18);color:#82cd5a;border:1px solid #82cd5a50">T2</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(200,200,70,.18);color:#c8c846;border:1px solid #c8c84650">T3</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(232,192,80,.2);color:#e8c050;border:1px solid #e8c05055">T4</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(230,140,50,.18);color:#e68c32;border:1px solid #e68c3250">T5</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(212,48,48,.18);color:#d44040;border:1px solid #d4404050">T6</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(140,60,220,.18);color:#a060e8;border:1px solid #a060e850">T7</span>
          </div>
        </div>

        <div>
          <div style="font-size:.72rem;color:var(--text2);letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">
            Grade — 동일 티어 장비 분해 재료로 강화 가능, 티어별 범위 제한
          </div>
          <div style="display:flex;gap:6px;flex-wrap:wrap">
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(160,160,160,.15);color:#aaa;border:1px solid #aaa4">일반</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(80,200,112,.15);color:#50c870;border:1px solid #50c87040">고급</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(60,140,240,.15);color:#4090f0;border:1px solid #4090f040">희귀</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(180,80,240,.15);color:#c060f0;border:1px solid #c060f040">영웅</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(240,120,30,.15);color:#f07820;border:1px solid #f0782040">전설</span>
            <span style="padding:4px 11px;border-radius:4px;font-weight:700;font-size:.85rem;background:rgba(232,192,80,.2);color:#e8c050;border:1px solid #e8c05055">유물</span>
          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- 무기 & 방어구 -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px">

    <!-- 무기 -->
    <div class="card">
      <div class="card-head">
        <span style="color:var(--gold)">⚔ 무기</span>
        <span style="font-size:.75rem;color:var(--text3)">5종 (활 추가 예정)</span>
      </div>
      <div style="padding:12px 16px;display:flex;flex-direction:column;gap:7px">
        <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(232,192,80,.07);border-radius:6px;border-left:3px solid #e8c050">
          <span style="font-size:1.2rem">🗡️</span>
          <div>
            <div style="color:var(--cream);font-weight:600;font-size:.88rem">양손검</div>
            <div style="color:var(--text3);font-size:.74rem">고화력 근거리 — 스킬 계수 최상위</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(232,192,80,.07);border-radius:6px;border-left:3px solid #e8c050">
          <span style="font-size:1.2rem">⚔️</span>
          <div>
            <div style="color:var(--cream);font-weight:600;font-size:.88rem">한손검</div>
            <div style="color:var(--text3);font-size:.74rem">밸런스형 근거리 — 안정적 DPS</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(232,192,80,.07);border-radius:6px;border-left:3px solid #e8c050">
          <span style="font-size:1.2rem">🔪</span>
          <div>
            <div style="color:var(--cream);font-weight:600;font-size:.88rem">단검</div>
            <div style="color:var(--text3);font-size:.74rem">속도형 근거리 — 쿨다운 특화</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(232,192,80,.07);border-radius:6px;border-left:3px solid #e8c050">
          <span style="font-size:1.2rem">🔮</span>
          <div>
            <div style="color:var(--cream);font-weight:600;font-size:.88rem">지팡이</div>
            <div style="color:var(--text3);font-size:.74rem">마법 원거리 — 최고 단일 피해</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(100,100,100,.07);border-radius:6px;border-left:3px solid #555;opacity:.5">
          <span style="font-size:1.2rem">🏹</span>
          <div>
            <div style="color:var(--text2);font-weight:600;font-size:.88rem">활 <span style="font-size:.7rem">(추가 예정)</span></div>
            <div style="color:var(--text3);font-size:.74rem">원거리 — 데이터 미정</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 방어구 -->
    <div class="card">
      <div class="card-head">
        <span style="color:var(--gold)">🛡 방어구</span>
        <span style="font-size:.75rem;color:var(--text3)">재질 3 × 파츠 4</span>
      </div>
      <div style="padding:12px 16px">
        <table style="width:100%;border-collapse:collapse;font-size:.82rem;text-align:center">
          <thead>
            <tr>
              <th style="padding:6px 10px;color:var(--text2);text-align:left;border-bottom:1px solid #2a2a2a"></th>
              <th style="padding:6px 8px;color:#b0b0b0;border-bottom:1px solid #2a2a2a">🪖 투구</th>
              <th style="padding:6px 8px;color:#b0b0b0;border-bottom:1px solid #2a2a2a">🥋 갑옷</th>
              <th style="padding:6px 8px;color:#b0b0b0;border-bottom:1px solid #2a2a2a">🧤 장갑</th>
              <th style="padding:6px 8px;color:#b0b0b0;border-bottom:1px solid #2a2a2a">👢 신발</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background:rgba(212,184,152,.06)">
              <td style="padding:9px 10px;color:#d4b896;font-weight:700;text-align:left;border-right:1px solid #2a2a2a">⚙ 판금</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
            </tr>
            <tr>
              <td style="padding:9px 10px;color:#a8c890;font-weight:700;text-align:left;border-right:1px solid #2a2a2a">🌿 가죽</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
            </tr>
            <tr style="background:rgba(212,184,152,.06)">
              <td style="padding:9px 10px;color:#c8a0d0;font-weight:700;text-align:left;border-right:1px solid #2a2a2a">🧵 천</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
              <td style="padding:9px;color:var(--text)">✦</td>
            </tr>
          </tbody>
        </table>
        <div style="margin-top:12px;font-size:.74rem;color:var(--text3);line-height:1.7">
          각 방어구마다 <strong style="color:var(--text2)">2~3개</strong>의 패시브 옵션 부여<br>
          재질별 옵션 풀 상이 · 파츠별로 다른 옵션 조합 제공
        </div>
      </div>
    </div>

  </div>

  <!-- 다운로드 바 -->
  <div class="download-bar" style="margin-bottom:20px">
    <span class="download-label">📂 기획서</span>
    <a class="download-btn" href="/mnt/user-data/uploads/장비_제작_및_드랍.xlsx" download>⬇ 장비_제작_및_드랍</a>
    <a class="download-btn" href="/mnt/user-data/uploads/방어구_옵션_밸런싱_최종_V2.xlsx" download>⬇ 방어구_옵션_밸런싱</a>
    <a class="download-btn" href="/mnt/user-data/uploads/X7_무기_스킬_밸런스.xlsx" download>⬇ 무기_스킬_밸런스</a>
  </div>

  <!-- 밸런스 현황 트리 -->
  """ + cat_html + """

</section>"""

html = re.sub(
    r'<section class="section active" id="sec-overview">.*?</section>(?=\s*\n\s*<!-- ══ GROWTH)',
    NEW_OVERVIEW,
    html, flags=re.DOTALL
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
shutil.copy2(HTML_PATH, HTML_SYNC)
print("✅ 완료")
print(f"   출력: {HTML_PATH}")
