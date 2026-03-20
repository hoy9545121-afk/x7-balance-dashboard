// ── GROWTH DATA ──────────────────────────────────────────────────────────
const GROWTH_LEVEL = [[1, 0, 8.6, 4300, 0, "이니스 섬"], [2, 0.14, 9.3, 4700, 4300, "이니스 섬"], [3, 0.3, 10.1, 5000, 9000, "이니스 섬"], [4, 0.47, 10.9, 5400, 14000, "이니스 섬"], [5, 0.65, 11.6, 5800, 19400, "이니스 섬"], [6, 0.84, 12.4, 6200, 25200, "이니스 섬"], [7, 1.05, 13.1, 6600, 31400, "이니스 섬"], [8, 1.27, 13.9, 7000, 38000, "이니스 섬"], [9, 1.5, 14.7, 7300, 45000, "이니스 섬"], [10, 1.74, 15.4, 7700, 52300, "이니스 섬"], [11, 2.0, 17.1, 8600, 60000, "솔즈리드 반도"], [12, 2.29, 18.7, 9300, 68600, "솔즈리드 반도"], [13, 2.6, 20.2, 10100, 77900, "솔즈리드 반도"], [14, 2.93, 21.7, 10900, 88000, "솔즈리드 반도"], [15, 3.3, 23.2, 11600, 98900, "솔즈리드 반도"], [16, 3.68, 24.8, 12400, 110500, "솔즈리드 반도"], [17, 4.1, 26.3, 13100, 122900, "솔즈리드 반도"], [18, 4.53, 27.8, 13900, 136000, "솔즈리드 반도"], [19, 5.0, 29.3, 14700, 149900, "솔즈리드 반도"], [20, 5.49, 30.9, 15400, 164600, "솔즈리드 반도"], [21, 6.0, 25.7, 12900, 180000, "릴리엇 구릉지"], [22, 6.43, 28.0, 14000, 192900, "릴리엇 구릉지"], [23, 6.9, 30.3, 15100, 206900, "릴리엇 구릉지"], [24, 7.4, 32.6, 16300, 222000, "릴리엇 구릉지"], [25, 7.94, 34.9, 17400, 238300, "릴리엇 구릉지"], [26, 8.52, 37.1, 18600, 255700, "릴리엇 구릉지"], [27, 9.14, 39.4, 19700, 274300, "릴리엇 구릉지"], [28, 9.8, 41.7, 20900, 294000, "릴리엇 구릉지"], [29, 10.5, 44.0, 22000, 314900, "릴리엇 구릉지"], [30, 11.23, 46.3, 23100, 336900, "릴리엇 구릉지"], [31, 12.0, 68.6, 34300, 360000, "가랑돌 평원"], [32, 13.14, 82.3, 41100, 394300, "가랑돌 평원"], [33, 14.51, 96.0, 48000, 435400, "가랑돌 평원"], [34, 16.11, 109.7, 54900, 483400, "가랑돌 평원"], [35, 17.94, 123.4, 61700, 538300, "가랑돌 평원"], [36, 20.0, 85.7, 42900, 600000, "하얀 숲"], [37, 21.43, 102.9, 51400, 642900, "하얀 숲"], [38, 23.14, 120.0, 60000, 694300, "하얀 숲"], [39, 25.14, 137.1, 68600, 754300, "하얀 숲"], [40, 27.43, 154.3, 77100, 822900, "하얀 숲"], [41, 30.0, 171.4, 85700, 900000, "마리아 노플"], [42, 32.86, 205.7, 102900, 985700, "마리아 노플"], [43, 36.29, 240.0, 120000, 1088600, "마리아 노플"], [44, 40.29, 274.3, 137100, 1208600, "마리아 노플"], [45, 44.86, 308.6, 154300, 1345700, "마리아 노플"], [46, 50.0, 342.9, 171400, 1500000, "황금 평원"], [47, 55.71, 411.4, 205700, 1671400, "황금 평원"], [48, 62.57, 480.0, 240000, 1877100, "황금 평원"], [49, 70.57, 548.6, 274300, 2117100, "황금 평원"], [50, 79.71, 617.1, 308600, 2391400, "황금 평원"], [51, 90.0, 685.7, 342900, 2700000, "지옥 늪지대"], [52, 101.43, 822.9, 411400, 3042900, "지옥 늪지대"], [53, 115.14, 960.0, 480000, 3454300, "지옥 늪지대"], [54, 131.14, 1097.1, 548600, 3934300, "지옥 늪지대"], [55, 149.43, 1234.3, 617100, 4482900, "지옥 늪지대"], [56, 170.0, 1371.4, 685700, 5100000, "긴 모래톱"], [57, 192.86, 1645.7, 822900, 5785700, "긴 모래톱"], [58, 220.29, 1920.0, 960000, 6608600, "긴 모래톱"], [59, 252.29, 2194.3, 1097100, 7568600, "긴 모래톱"], [60, 288.86, 2468.6, 1234300, 8665700, "긴 모래톱"], [61, 330.0, 1157.1, 578600, 9900000, "(미정)"], [62, 349.29, 1260.0, 630000, 10478600, "(미정)"], [63, 370.29, 1362.9, 681400, 11108600, "(미정)"], [64, 393.0, 1465.7, 732900, 11790000, "(미정)"], [65, 417.43, 1568.6, 784300, 12522900, "(미정)"], [66, 443.57, 1671.4, 835700, 13307200, "(미정)"], [67, 471.43, 1774.3, 887100, 14142900, "(미정)"], [68, 501.0, 1877.1, 938600, 15030000, "(미정)"], [69, 532.29, 1980.0, 990000, 15968600, "(미정)"], [70, 565.29, 2082.9, 1041400, 16958600, "(미정)"], [71, 600.0, 857.1, 428600, 18000000, "(미정)"], [72, 614.29, 933.3, 466700, 18428600, "(미정)"], [73, 629.84, 1009.5, 504800, 18895300, "(미정)"], [74, 646.67, 1085.7, 542900, 19400100, "(미정)"], [75, 664.76, 1161.9, 581000, 19943000, "(미정)"], [76, 684.13, 1238.1, 619000, 20524000, "(미정)"], [77, 704.76, 1314.3, 657100, 21143000, "(미정)"], [78, 726.67, 1390.5, 695200, 21800100, "(미정)"], [79, 749.84, 1466.7, 733300, 22495300, "(미정)"], [80, 774.29, 1542.9, 771400, 23228600, "(미정)"], [81, 800.0, 642.9, 321400, 24000000, "(미정)"], [82, 810.71, 700.0, 350000, 24321400, "(미정)"], [83, 822.38, 757.1, 378600, 24671400, "(미정)"], [84, 835.0, 814.3, 407100, 25050000, "(미정)"], [85, 848.57, 871.4, 435700, 25457100, "(미정)"], [86, 863.1, 928.6, 464300, 25892800, "(미정)"], [87, 878.57, 985.7, 492900, 26357100, "(미정)"], [88, 895.0, 1042.9, 521400, 26850000, "(미정)"], [89, 912.38, 1100.0, 550000, 27371400, "(미정)"], [90, 930.71, 1157.1, 578600, 27921400, "(미정)"], [91, 950.0, 1071.4, 535700, 28500000, "(미정)"], [92, 967.86, 1166.7, 583300, 29035700, "(미정)"], [93, 987.3, 1261.9, 631000, 29619000, "(미정)"], [94, 1008.33, 1357.1, 678600, 30250000, "(미정)"], [95, 1030.95, 1452.4, 726200, 30928600, "(미정)"], [96, 1055.16, 1547.6, 773800, 31654800, "(미정)"], [97, 1080.95, 1642.9, 821400, 32428600, "(미정)"], [98, 1108.33, 1738.1, 869000, 33250000, "(미정)"], [99, 1137.3, 1833.3, 916700, 34119000, "(미정)"], [100, 1167.86, 1928.6, 964300, 35035700, "(미정)"]];
const GROWTH_PROF  = [{"t": "1T", "target": "캐릭터 10레벨 완료", "hours": "2h", "total": 36000, "lvs": [{"lv": 1, "xp": 36000, "note": "2T 진입 가능"}]}, {"t": "2T", "target": "캐릭터 20레벨 완료", "hours": "4h", "total": 72000, "lvs": [{"lv": 1, "xp": 72000, "note": "3T 진입 가능"}]}, {"t": "3T", "target": "캐릭터 30레벨 완료", "hours": "6h", "total": 108000, "lvs": [{"lv": 1, "xp": 27700, "note": ""}, {"lv": 2, "xp": 36000, "note": ""}, {"lv": 3, "xp": 44300, "note": "4T 진입 가능"}]}, {"t": "4T", "target": "캐릭터 40레벨 완료", "hours": "18h", "total": 324000, "lvs": [{"lv": 1, "xp": 83100, "note": ""}, {"lv": 2, "xp": 108000, "note": ""}, {"lv": 3, "xp": 132900, "note": "5T 진입 가능"}]}, {"t": "5T", "target": "캐릭터 50레벨 완료", "hours": "60h", "total": 1080000, "lvs": [{"lv": 1, "xp": 166200, "note": ""}, {"lv": 2, "xp": 191100, "note": ""}, {"lv": 3, "xp": 216000, "note": ""}, {"lv": 4, "xp": 240900, "note": ""}, {"lv": 5, "xp": 265800, "note": "6T 진입 가능"}]}, {"t": "6T", "target": "캐릭터 55레벨 완료", "hours": "80h", "total": 1440000, "lvs": [{"lv": 1, "xp": 221500, "note": ""}, {"lv": 2, "xp": 254800, "note": ""}, {"lv": 3, "xp": 288000, "note": ""}, {"lv": 4, "xp": 321200, "note": ""}, {"lv": 5, "xp": 354500, "note": "7T 진입 가능"}]}, {"t": "7T", "target": "캐릭터 60레벨 완료", "hours": "160h", "total": 2880000, "lvs": [{"lv": 1, "xp": 246200, "note": ""}, {"lv": 2, "xp": 264600, "note": ""}, {"lv": 3, "xp": 283100, "note": ""}, {"lv": 4, "xp": 301500, "note": ""}, {"lv": 5, "xp": 320000, "note": ""}, {"lv": 6, "xp": 338500, "note": ""}, {"lv": 7, "xp": 356900, "note": ""}, {"lv": 8, "xp": 375400, "note": ""}, {"lv": 9, "xp": 393800, "note": ""}]}];
const TIER_COLORS_G = {"1T": "#50c870", "2T": "#5090e8", "3T": "#e8c050", "4T": "#e87830", "5T": "#c850c8", "6T": "#d43030", "7T": "#ff5555"};

const AREA_ZONE = {
  '이니스 섬':'1T','솔즈리드 반도':'2T','릴리엇 구릉지':'3T',
  '가랑돌 평원':'4T','하얀 숲':'4T','마리아 노플':'5T',
  '황금 평원':'5T','지옥 늪지대':'6T','긴 모래톱':'7T','(미정)':'—'
};

function renderGrowthLevel() {
  const body = document.getElementById('grw-lv-body');
  if (!body || body.children.length > 0) return;
  const maxXp = Math.max(...GROWTH_LEVEL.map(r=>r[3]));
  let prev = null;
  body.innerHTML = GROWTH_LEVEL.map(r => {
    const [lv, h_cum, min_req, xp_lv, xp_cum, area] = r;
    const tc = TIER_COLORS_G[AREA_ZONE[area]] || '#888';
    const isMile = lv % 10 === 0;
    const growth = prev ? ((xp_lv/prev - 1)*100).toFixed(0)+'%↑' : '—';
    prev = xp_lv;
    const bg = isMile ? 'background:rgba(232,192,80,0.07)' : '';
    return `<tr style="${bg}">
      <td style="font-weight:${isMile?700:400};color:${isMile?'var(--gold)':'inherit'}">${lv}</td>
      <td style="color:${tc};font-size:0.78rem">${area}</td>
      <td class="td-num">${xp_lv.toLocaleString()}</td>
      <td class="td-num" style="color:var(--text2)">${xp_cum.toLocaleString()}</td>
      <td class="td-num">${h_cum}h</td>
      <td style="color:var(--text3);font-size:0.75rem">${growth}</td>
    </tr>`;
  }).join('');
}
renderGrowthLevel();

// ═══════════════ DATA ═══════════════

const ARMOR_DATA = {
  '1T': [
    {slot:'아머',name:'받는 피해 감소',key:'DamageDownVaryper',mat:'판금',obt:'기본 제작',vals:['1%','1.2%','1.3%','1.5%','1.7%','2%']},
    {slot:'헬멧',name:'생명력 자연 회복',key:'RegenHpVary',mat:'판금',obt:'기본 제작',vals:[5,6,7,8,9,10]},
    {slot:'장갑',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'기본 제작',vals:[75,85,100,115,130,150]},
    {slot:'신발',name:'방어력',key:'DefenseVary',mat:'판금',obt:'기본 제작',vals:[20,24,26,30,34,40]},
    {slot:'아머',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'기본 제작',vals:[75,85,100,115,130,150]},
    {slot:'헬멧',name:'치명타 확률',key:'CriVaryper',mat:'가죽',obt:'기본 제작',vals:['1.2%','1.4%','1.6%','1.8%','2.1%','2.4%']},
    {slot:'장갑',name:'공격 속도',key:'AtkSpeedVaryper',mat:'가죽',obt:'기본 제작',vals:['2%','2.3%','2.6%','3%','3.5%','4%']},
    {slot:'신발',name:'공격력',key:'AttackVary',mat:'가죽',obt:'기본 제작',vals:[5,6,7,8,9,10]},
    {slot:'아머',name:'최대 마력',key:'MaxMpVary',mat:'천',obt:'기본 제작',vals:[20,24,26,30,34,40]},
    {slot:'헬멧',name:'마력 자연 회복',key:'RegenMpVary',mat:'천',obt:'기본 제작',vals:[3,4,5,6,7,8]},
    {slot:'장갑',name:'공격력',key:'AttackVary',mat:'천',obt:'기본 제작',vals:[5,6,7,8,9,10]},
    {slot:'신발',name:'마나 소모량 감소',key:'CostMpDownVaryper',mat:'천',obt:'기본 제작',vals:['2%','2.3%','2.6%','3%','3.5%','4%']},
  ],
  '2T': [
    {slot:'헬멧',name:'생명력 자연 회복',key:'RegenHpVary',mat:'판금',obt:'전리품 제작',vals:[8,9,10,12,14,16]},
    {slot:'헬멧',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'전리품 제작',vals:[120,140,160,185,210,240]},
    {slot:'헬멧',name:'치명타 확률',key:'CriVaryper',mat:'판금',obt:'전리품 제작',vals:['1.9%','2.2%','2.5%','2.9%','3.3%','3.8%']},
    {slot:'장갑',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'전리품 제작',vals:[120,140,160,185,210,240]},
    {slot:'장갑',name:'받는 피해 감소',key:'DamageDownVaryper',mat:'판금',obt:'전리품 제작',vals:['1.6%','1.8%','2.1%','2.4%','2.8%','3.2%']},
    {slot:'헬멧',name:'치명타 확률',key:'CriVaryper',mat:'가죽',obt:'전리품 제작',vals:['1.9%','2.2%','2.5%','2.9%','3.3%','3.8%']},
    {slot:'헬멧',name:'공격력',key:'AttackVary',mat:'가죽',obt:'전리품 제작',vals:[8,9,10,12,14,16]},
    {slot:'헬멧',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'전리품 제작',vals:[120,140,160,185,210,240]},
    {slot:'장갑',name:'공격 속도',key:'AtkSpeedVaryper',mat:'가죽',obt:'전리품 제작',vals:['3.2%','3.7%','4.2%','4.9%','5.6%','6.4%']},
    {slot:'장갑',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'가죽',obt:'전리품 제작',vals:[8,9,10,12,14,16]},
    {slot:'헬멧',name:'마력 자연 회복',key:'RegenMpVary',mat:'천',obt:'전리품 제작',vals:[5,6,7,8,9,10]},
    {slot:'헬멧',name:'최대 생명력',key:'MaxHpVary',mat:'천',obt:'전리품 제작',vals:[120,140,160,185,210,240]},
    {slot:'헬멧',name:'마나 소모량 감소',key:'CostMpDownVaryper',mat:'천',obt:'전리품 제작',vals:['3.2%','3.7%','4.2%','4.9%','5.6%','6.4%']},
    {slot:'장갑',name:'공격력',key:'AttackVary',mat:'천',obt:'전리품 제작',vals:[8,9,10,12,14,16]},
    {slot:'장갑',name:'마나 소모량 감소',key:'CostMpDownVaryper',mat:'천',obt:'전리품 제작',vals:['3.2%','3.7%','4.2%','4.9%','5.6%','6.4%']},
    {slot:'아머',name:'받는 피해 감소',key:'DamageDownVaryper',mat:'판금',obt:'던전 코어 제작',vals:['1.6%','1.8%','2.1%','2.4%','2.8%','3.2%']},
    {slot:'아머',name:'치명타 확률',key:'CriVaryper',mat:'판금',obt:'던전 코어 제작',vals:['1.9%','2.2%','2.5%','2.9%','3.3%','3.8%']},
    {slot:'아머',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'던전 코어 제작',vals:[120,140,160,185,210,240]},
    {slot:'장갑',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'던전 코어 제작',vals:[120,140,160,185,210,240]},
    {slot:'장갑',name:'공격 속도',key:'AtkSpeedVaryper',mat:'판금',obt:'던전 코어 제작',vals:['3.2%','3.7%','4.2%','4.9%','5.6%','6.4%']},
    {slot:'아머',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'던전 코어 제작',vals:[120,140,160,185,210,240]},
    {slot:'아머',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'가죽',obt:'던전 코어 제작',vals:[8,9,10,12,14,16]},
    {slot:'아머',name:'치명타 피해',key:'CriDamageVaryper',mat:'가죽',obt:'던전 코어 제작',vals:['9.5%','10.9%','12.6%','14.4%','16.6%','19.2%']},
    {slot:'장갑',name:'공격 속도',key:'AtkSpeedVaryper',mat:'가죽',obt:'던전 코어 제작',vals:['3.2%','3.7%','4.2%','4.9%','5.6%','6.4%']},
    {slot:'장갑',name:'치명타 피해',key:'CriDamageVaryper',mat:'가죽',obt:'던전 코어 제작',vals:['9.5%','10.9%','12.6%','14.4%','16.6%','19.2%']},
    {slot:'아머',name:'최대 마력',key:'MaxMpVary',mat:'천',obt:'던전 코어 제작',vals:[32,36,42,48,55,65]},
    {slot:'아머',name:'치명타 확률',key:'CriVaryper',mat:'천',obt:'던전 코어 제작',vals:['1.9%','2.2%','2.5%','2.9%','3.3%','3.8%']},
    {slot:'아머',name:'마력 자연 회복',key:'RegenMpVary',mat:'천',obt:'던전 코어 제작',vals:[5,6,7,8,9,10]},
    {slot:'장갑',name:'공격력',key:'AttackVary',mat:'천',obt:'던전 코어 제작',vals:[8,9,10,12,14,16]},
    {slot:'장갑',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'천',obt:'던전 코어 제작',vals:[8,9,10,12,14,16]},
    {slot:'신발',name:'방어력',key:'DefenseVary',mat:'판금',obt:'보스 드랍',vals:[32,36,42,48,55,65]},
    {slot:'신발',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'판금',obt:'보스 드랍',vals:[8,9,10,12,14,16]},
    {slot:'신발',name:'생명력 자연 회복',key:'RegenHpVary',mat:'판금',obt:'보스 드랍',vals:[8,9,10,12,14,16]},
    {slot:'신발',name:'공격력',key:'AttackVary',mat:'가죽',obt:'보스 드랍',vals:[8,9,10,12,14,16]},
    {slot:'신발',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'보스 드랍',vals:[120,140,160,185,210,240]},
    {slot:'신발',name:'치명타 확률',key:'CriVaryper',mat:'가죽',obt:'보스 드랍',vals:['1.9%','2.2%','2.5%','2.9%','3.3%','3.8%']},
    {slot:'신발',name:'마나 소모량 감소',key:'CostMpDownVaryper',mat:'천',obt:'보스 드랍',vals:['3.2%','3.7%','4.2%','4.9%','5.6%','6.4%']},
    {slot:'신발',name:'최대 생명력',key:'MaxHpVary',mat:'천',obt:'보스 드랍',vals:[120,140,160,185,210,240]},
    {slot:'신발',name:'공격력',key:'AttackVary',mat:'천',obt:'보스 드랍',vals:[8,9,10,12,14,16]},
  ],
  '3T': [
    {slot:'아머',name:'받는 피해 감소',key:'DamageDownVaryper',mat:'판금',obt:'전리품 제작',vals:['2.5%','2.9%','3.3%','3.8%','4.4%','5%']},
    {slot:'아머',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'전리품 제작',vals:[190,220,250,290,330,380]},
    {slot:'아머',name:'방어력',key:'DefenseVary',mat:'판금',obt:'전리품 제작',vals:[50,55,65,75,85,100]},
    {slot:'헬멧',name:'생명력 자연 회복',key:'RegenHpVary',mat:'판금',obt:'전리품 제작',vals:[12,14,16,20,22,26]},
    {slot:'헬멧',name:'치명타 확률',key:'CriVaryper',mat:'판금',obt:'전리품 제작',vals:['3%','3.4%','3.9%','4.5%','5.2%','6%']},
    {slot:'헬멧',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'판금',obt:'전리품 제작',vals:[12,14,16,18,21,25]},
    {slot:'장갑',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'전리품 제작',vals:[190,220,250,290,330,380]},
    {slot:'장갑',name:'방어력',key:'DefenseVary',mat:'판금',obt:'전리품 제작',vals:[50,55,65,75,85,100]},
    {slot:'장갑',name:'상태이상 저항력',key:'SCNegativeRecoveryVary',mat:'판금',obt:'전리품 제작',vals:[50,57,66,76,87,100]},
    {slot:'장갑',name:'받는 치유량',key:'HealAcceptVary',mat:'판금',obt:'전리품 제작',vals:[75,86,99,114,131,150]},
    {slot:'아머',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'전리품 제작',vals:[190,220,250,290,330,380]},
    {slot:'아머',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'가죽',obt:'전리품 제작',vals:[12,14,16,18,21,25]},
    {slot:'아머',name:'PVE 피해 증가',key:'PVEDamageUpVaryper',mat:'가죽',obt:'전리품 제작',vals:['4%','4.6%','5.3%','6.1%','7%','8%']},
    {slot:'헬멧',name:'치명타 확률',key:'CriVaryper',mat:'가죽',obt:'전리품 제작',vals:['3%','3.4%','3.9%','4.5%','5.2%','6%']},
    {slot:'헬멧',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'전리품 제작',vals:[190,220,250,290,330,380]},
    {slot:'헬멧',name:'받는 피해 감소',key:'DamageDownVaryper',mat:'가죽',obt:'전리품 제작',vals:['2.5%','2.9%','3.3%','3.8%','4.4%','5%']},
    {slot:'장갑',name:'공격 속도',key:'AtkSpeedVaryper',mat:'가죽',obt:'전리품 제작',vals:['5%','5.7%','6.6%','7.6%','8.7%','10%']},
    {slot:'장갑',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'가죽',obt:'전리품 제작',vals:[12,14,16,18,21,25]},
    {slot:'장갑',name:'PVE 피해 증가',key:'PVEDamageUpVaryper',mat:'가죽',obt:'전리품 제작',vals:['4%','4.6%','5.3%','6.1%','7%','8%']},
    {slot:'장갑',name:'치명타 확률',key:'CriVaryper',mat:'가죽',obt:'전리품 제작',vals:['3%','3.4%','3.9%','4.5%','5.2%','6%']},
    {slot:'아머',name:'최대 마력',key:'MaxMpVary',mat:'천',obt:'전리품 제작',vals:[50,55,65,75,85,100]},
    {slot:'아머',name:'마력 자연 회복',key:'RegenMpVary',mat:'천',obt:'전리품 제작',vals:[8,9,10,12,14,16]},
    {slot:'아머',name:'치유력',key:'HealAmpVaryper',mat:'천',obt:'전리품 제작',vals:['7.5%','8.6%','9.9%','11.4%','13.1%','15%']},
    {slot:'헬멧',name:'마력 자연 회복',key:'RegenMpVary',mat:'천',obt:'전리품 제작',vals:[8,9,10,12,14,16]},
    {slot:'헬멧',name:'최대 생명력',key:'MaxHpVary',mat:'천',obt:'전리품 제작',vals:[190,220,250,290,330,380]},
    {slot:'헬멧',name:'받는 피해 감소',key:'DamageDownVaryper',mat:'천',obt:'전리품 제작',vals:['2.5%','2.9%','3.3%','3.8%','4.4%','5%']},
    {slot:'장갑',name:'공격력',key:'AttackVary',mat:'천',obt:'전리품 제작',vals:[12,14,16,20,22,26]},
    {slot:'장갑',name:'마나 소모량 감소',key:'CostMpDownVaryper',mat:'천',obt:'전리품 제작',vals:['5%','5.7%','6.6%','7.6%','8.7%','10%']},
    {slot:'장갑',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'천',obt:'전리품 제작',vals:[12,14,16,18,21,25]},
    {slot:'장갑',name:'치유력',key:'HealAmpVaryper',mat:'천',obt:'전리품 제작',vals:['7.5%','8.6%','9.9%','11.4%','13.1%','15%']},
    {slot:'아머',name:'받는 피해 감소',key:'DamageDownVaryper',mat:'판금',obt:'드랍(Boss)',vals:['2.5%','2.9%','3.3%','3.8%','4.4%','5%']},
    {slot:'아머',name:'치명타 확률',key:'CriVaryper',mat:'판금',obt:'드랍(Boss)',vals:['3%','3.4%','3.9%','4.5%','5.2%','6%']},
    {slot:'아머',name:'치명타 피해',key:'CriDamageVaryper',mat:'판금',obt:'드랍(Boss)',vals:['14.9%','17.1%','19.7%','22.7%','26.1%','30%']},
    {slot:'헬멧',name:'생명력 자연 회복',key:'RegenHpVary',mat:'판금',obt:'드랍(Boss)',vals:[12,14,16,20,22,26]},
    {slot:'헬멧',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'드랍(Boss)',vals:[190,220,250,290,330,380]},
    {slot:'헬멧',name:'상태이상 저항력',key:'SCNegativeRecoveryVary',mat:'판금',obt:'드랍(Boss)',vals:[50,57,66,76,87,100]},
    {slot:'신발',name:'방어력',key:'DefenseVary',mat:'판금',obt:'드랍(Boss)',vals:[50,55,65,75,85,100]},
    {slot:'신발',name:'생명력 자연 회복',key:'RegenHpVary',mat:'판금',obt:'드랍(Boss)',vals:[12,14,16,20,22,26]},
    {slot:'신발',name:'최대 생명력',key:'MaxHpVary',mat:'판금',obt:'드랍(Boss)',vals:[190,220,250,290,330,380]},
    {slot:'신발',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'판금',obt:'드랍(Boss)',vals:[12,14,16,18,21,25]},
    {slot:'신발',name:'피해 증가',key:'DamageUpVaryper',mat:'판금',obt:'드랍(Boss)',vals:['4%','4.6%','5.3%','6.1%','7%','8%']},
    {slot:'신발',name:'공격 속도',key:'AtkSpeedVaryper',mat:'판금',obt:'드랍(Boss)',vals:['5%','5.7%','6.6%','7.6%','8.7%','10%']},
    {slot:'아머',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'드랍(Boss)',vals:[190,220,250,290,330,380]},
    {slot:'아머',name:'치명타 피해',key:'CriDamageVaryper',mat:'가죽',obt:'드랍(Boss)',vals:['14.9%','17.1%','19.7%','22.7%','26.1%','30%']},
    {slot:'아머',name:'공격력',key:'AttackVary',mat:'가죽',obt:'드랍(Boss)',vals:[12,14,16,20,22,26]},
    {slot:'신발',name:'공격력',key:'AttackVary',mat:'가죽',obt:'드랍(Boss)',vals:[12,14,16,20,22,26]},
    {slot:'신발',name:'최대 생명력',key:'MaxHpVary',mat:'가죽',obt:'드랍(Boss)',vals:[190,220,250,290,330,380]},
    {slot:'신발',name:'치명타 확률',key:'CriVaryper',mat:'가죽',obt:'드랍(Boss)',vals:['3%','3.4%','3.9%','4.5%','5.2%','6%']},
    {slot:'아머',name:'최대 마력',key:'MaxMpVary',mat:'천',obt:'드랍(Boss)',vals:[50,55,65,75,85,100]},
    {slot:'아머',name:'치명타 확률',key:'CriVaryper',mat:'천',obt:'드랍(Boss)',vals:['3%','3.4%','3.9%','4.5%','5.2%','6%']},
    {slot:'아머',name:'스킬 가속',key:'SkillCooldownAccVary',mat:'천',obt:'드랍(Boss)',vals:[12,14,16,18,21,25]},
    {slot:'신발',name:'마나 소모량 감소',key:'CostMpDownVaryper',mat:'천',obt:'드랍(Boss)',vals:['5%','5.7%','6.6%','7.6%','8.7%','10%']},
    {slot:'신발',name:'공격력',key:'AttackVary',mat:'천',obt:'드랍(Boss)',vals:[12,14,16,20,22,26]},
    {slot:'신발',name:'치유력',key:'HealAmpVaryper',mat:'천',obt:'드랍(Boss)',vals:['7.5%','8.6%','9.9%','11.4%','13.1%','15%']},
  ]
};

const ITEM_LIST = [
  {cid:12010001, tier:'1T',obt:'기본 제작',mat:'판금',slot:'아머',p1:'받는 피해 감소',p2:'-',p3:'-'},
  {cid:12010002, tier:'1T',obt:'기본 제작',mat:'판금',slot:'헬멧',p1:'생명력 자연 회복',p2:'-',p3:'-'},
  {cid:12010003, tier:'1T',obt:'기본 제작',mat:'판금',slot:'장갑',p1:'최대 생명력',p2:'-',p3:'-'},
  {cid:12010004, tier:'1T',obt:'기본 제작',mat:'판금',slot:'신발',p1:'방어력',p2:'-',p3:'-'},
  {cid:12010005, tier:'1T',obt:'기본 제작',mat:'가죽',slot:'아머',p1:'최대 생명력',p2:'-',p3:'-'},
  {cid:12010006, tier:'1T',obt:'기본 제작',mat:'가죽',slot:'헬멧',p1:'치명타 확률',p2:'-',p3:'-'},
  {cid:12010007, tier:'1T',obt:'기본 제작',mat:'가죽',slot:'장갑',p1:'공격 속도',p2:'-',p3:'-'},
  {cid:12010008, tier:'1T',obt:'기본 제작',mat:'가죽',slot:'신발',p1:'공격력',p2:'-',p3:'-'},
  {cid:12010009, tier:'1T',obt:'기본 제작',mat:'천',slot:'아머',p1:'최대 마력',p2:'-',p3:'-'},
  {cid:12010010, tier:'1T',obt:'기본 제작',mat:'천',slot:'헬멧',p1:'마력 자연 회복',p2:'-',p3:'-'},
  {cid:12010011, tier:'1T',obt:'기본 제작',mat:'천',slot:'장갑',p1:'공격력',p2:'-',p3:'-'},
  {cid:12010012, tier:'1T',obt:'기본 제작',mat:'천',slot:'신발',p1:'마나 소모량 감소',p2:'-',p3:'-'},
  {cid:12020001, tier:'2T',obt:'전리품 제작',mat:'판금',slot:'헬멧',p1:'생명력 자연 회복',p2:'최대 생명력',p3:'-'},
  {cid:12020002, tier:'2T',obt:'전리품 제작',mat:'판금',slot:'장갑',p1:'최대 생명력',p2:'받는 피해 감소',p3:'-'},
  {cid:12020003, tier:'2T',obt:'전리품 제작',mat:'가죽',slot:'헬멧',p1:'치명타 확률',p2:'공격력',p3:'-'},
  {cid:12020004, tier:'2T',obt:'전리품 제작',mat:'가죽',slot:'장갑',p1:'공격 속도',p2:'스킬 가속',p3:'-'},
  {cid:12020013, tier:'2T',obt:'던전 코어 제작',mat:'판금',slot:'아머',p1:'받는 피해 감소',p2:'치명타 확률',p3:'-'},
  {cid:12020014, tier:'2T',obt:'던전 코어 제작',mat:'가죽',slot:'아머',p1:'최대 생명력',p2:'스킬 가속',p3:'-'},
  {cid:12020022, tier:'2T',obt:'보스 드랍',mat:'판금',slot:'신발',p1:'방어력',p2:'스킬 가속',p3:'-'},
  {cid:12030001, tier:'3T',obt:'전리품 제작',mat:'판금',slot:'아머',p1:'받는 피해 감소',p2:'최대 생명력',p3:'방어력'},
  {cid:12030002, tier:'3T',obt:'전리품 제작',mat:'판금',slot:'헬멧',p1:'생명력 자연 회복',p2:'치명타 확률',p3:'스킬 가속'},
  {cid:12030003, tier:'3T',obt:'전리품 제작',mat:'판금',slot:'장갑',p1:'최대 생명력',p2:'방어력',p3:'상태이상 저항력'},
  {cid:12030004, tier:'3T',obt:'전리품 제작',mat:'가죽',slot:'아머',p1:'최대 생명력',p2:'스킬 가속',p3:'PVE 피해 증가'},
  {cid:12030031, tier:'3T',obt:'보스 드랍',mat:'판금',slot:'아머',p1:'받는 피해 감소',p2:'치명타 확률',p3:'치명타 피해'},
  {cid:12030032, tier:'3T',obt:'보스 드랍',mat:'판금',slot:'헬멧',p1:'생명력 자연 회복',p2:'최대 생명력',p3:'상태이상 저항력'},
  {cid:12030033, tier:'3T',obt:'보스 드랍',mat:'판금',slot:'신발',p1:'방어력',p2:'스킬 가속',p3:'피해 증가'},
];

const DPS_DATA = [
  {weapon:'한손검',Q:15,W:10,E:7.5,R:6.7},
  {weapon:'양손검',Q:24,W:12.5,E:12,R:6},
  {weapon:'지팡이',Q:30,W:16,E:9,R:9},
  {weapon:'단검',Q:22,W:5.5,E:10,R:7.5},
  {weapon:'활',Q:26,W:14,E:10.5,R:6.7},
];

// ═══════════ STATE ═══════════
let armorTier = '1T';
let armorSlot = 'all';
let armorMat = 'all';
let armorSearch = '';
let skillTier = '1';
let listTierF = 'all';
let listObtF = 'all';

// ═══════════ NAV ═══════════
function showSection(id) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
  document.getElementById('sec-' + id).classList.add('active');
  document.querySelector(`[data-s="${id}"]`).classList.add('active');
  if (id === 'armor') { renderArmorTier('1T'); renderArmorTier('2T'); renderArmorTier('3T'); }
  if (id === 'skill') { renderDPS(); renderWeaponTier('1'); renderWeaponTier('2'); renderWeaponTier('3'); }
  if (id === 'economy') { renderItemList(); }
}

// ═══════════ GENERIC TAB ═══════════
function switchTab(section, tab, btn) {
  const prefix = section + '-';
  document.querySelectorAll(`[id^="${prefix}"]`).forEach(el => el.style.display = 'none');
  document.getElementById(prefix + tab).style.display = 'block';
  btn.closest('.tab-bar').querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  if (tab === 'list') renderItemList();
  if (tab === 'compare') renderDPS();
}

// ═══════════ ARMOR ═══════════
const SLOT_ICON = {아머:'🛡',헬멧:'⛑',장갑:'🥊',신발:'👟'};
const MAT_ICON = {판금:'⚙',가죽:'🟤',천:'🟣'};
const OBT_ICON = {기본 제작:'🔨','전리품 제작':'💎','던전 코어 제작':'🔮','보스 드랍':'👺'};

function renderArmorTier(tier) {
  const gridId = 'armor-grid-' + tier;
  const grid = document.getElementById(gridId);
  if (!grid) return;

  // 1. 해당 티어의 아이템 목록 가져오기 (필터링 적용)
  let items = ITEM_LIST.filter(it => {
    if (it.tier !== tier) return false;
    if (armorSlot !== 'all' && it.slot !== armorSlot) return false;
    if (armorMat !== 'all' && it.mat !== armorMat) return false;
    if (armorSearch && !it.p1.toLowerCase().includes(armorSearch) && !it.p2.toLowerCase().includes(armorSearch)) return false;
    return true;
  });

  if (!items.length) { 
    grid.innerHTML = '<div class="empty-state">조건에 맞는 장비가 없습니다.</div>'; 
    return; 
  }

  // 2. 렌더링
  grid.innerHTML = items.map(item => {
    // 해당 아이템의 p1, p2, p3 옵션 명칭 추출
    const pNames = [item.p1, item.p2, item.p3].filter(p => p !== '-');
    
    // ARMOR_DATA에서 해당 옵션의 레벨별 수치 찾아서 HTML 생성
    const statsHtml = pNames.map(pName => {
      const d = ARMOR_DATA[tier].find(ad => ad.name === pName && ad.mat === item.mat && ad.obt === item.obt);
      if (!d) return `<div class="stat-inner-item" style="color:#666; font-size:0.8rem; padding:8px;">[DATA ERROR: ${pName}]</div>`;

      const growths = [];
      for (let i = 1; i < d.vals.length; i++) {
        const a = parseFloat(String(d.vals[i-1]).replace('%',''));
        const b = parseFloat(String(d.vals[i]).replace('%',''));
        growths.push(a > 0 ? Math.min(100, Math.round((b-a)/a*120)) : 60);
      }
      const gBars = growths.map(g => `<div class="g-seg"><div class="g-fill" style="width:${g}%"></div></div>`).join('');
      const lvCells = d.vals.map((v,i) => `<div class="lv-cell${i===5?' max':''}">${v}</div>`).join('');
      
      return `
      <div class="stat-inner-item" style="margin-bottom:16px; padding-bottom:8px;">
        <div class="armor-info" style="display:flex; align-items:center; gap:8px;">
          <div class="armor-stat-name" style="font-size:0.95rem; color:var(--cream); font-weight:600;">${d.name}</div>
          <div class="armor-key" style="font-size:0.7rem; color:var(--text3); opacity:0.7;">${d.key}</div>
        </div>
        <div class="level-grid" style="margin-top:8px;">
          <div class="level-row"><div class="lv-label">수치</div>${lvCells}</div>
        </div>
        <div class="growth-bar-wrap" style="margin-top:4px;">${gBars}</div>
      </div>`;
    }).join('');

    return `
    <div class="armor-card group-card" style="border: 1px solid var(--border-bright); background: var(--panel-dark); overflow:hidden;">
      <div class="armor-card-head" style="background: rgba(255,255,255,0.02); padding: 14px 18px; border-bottom: 1px solid var(--border); display:flex; align-items:center; gap:12px;">
        <span class="armor-slot-icon" style="font-size:1.6rem">${SLOT_ICON[item.slot]||'📦'}</span>
        <div class="armor-info" style="flex:1">
          <div class="armor-group-title" style="font-weight:700; color:var(--gold); font-size:1.05rem;">${item.tier} ${item.mat} ${item.slot}</div>
          <div class="armor-cid" style="font-size:0.75rem; color:var(--text3); letter-spacing:0.02em;">CID: ${item.cid}</div>
        </div>
        <div class="armor-badges" style="display:flex; flex-direction:column; align-items:flex-end; gap:4px;">
          <span class="badge badge-mat" style="background:rgba(255,255,255,0.05); color:var(--text2); border:1px solid var(--border);">${MAT_ICON[item.mat]||''} ${item.mat}</span>
          <span class="badge badge-obt" style="background:rgba(232,184,75,0.1); color:var(--gold); border:1px solid rgba(232,184,75,0.2);">${OBT_ICON[item.obt]||''} ${item.obt}</span>
        </div>
      </div>
      <div class="armor-card-body" style="padding:16px; border: 2px solid rgba(232, 184, 75, 0.12); margin: 12px; border-radius: 8px; background: rgba(0,0,0,0.15);">
        ${statsHtml}
      </div>
    </div>`;
  }).join('');
}

function filterArmor(type, val, btn) {
  if (type === 'slot') { armorSlot = val; }
  else { armorMat = val; }
  const bar = btn.closest('.filter-bar');
  const btns = bar.querySelectorAll('.filter-btn');
  const slotCount = 5; 
  [...btns].forEach((b,i) => {
    if (type === 'slot' && i < slotCount) b.classList.remove('active');
    if (type === 'mat' && i >= slotCount) b.classList.remove('active');
  });
  btn.classList.add('active');
  ['1T','2T','3T'].forEach(t => renderArmorTier(t));
}

function searchArmor(v) {
  armorSearch = v.toLowerCase();
  ['1T','2T','3T'].forEach(t => renderArmorTier(t));
}

// ═══════════ SKILL ═══════════
function renderWeaponTier(tier) {
  const gridId = 'weapon-grid-' + tier + 'T';
  const grid = document.getElementById(gridId);
  if (!grid) return;
  const data = WEAPON_DATA[tier];
  const typeStyle = {
    '방향 공격':'background:rgba(80,144,232,0.15);border:1px solid rgba(80,144,232,0.3);color:#80c0ff',
    '단일 공격':'background:rgba(212,48,48,0.15);border:1px solid rgba(212,48,48,0.3);color:#ff8080',
    '범위 공격':'background:rgba(232,192,80,0.1);border:1px solid rgba(232,192,80,0.25);color:#e8c050',
    '버프':'background:rgba(80,200,112,0.12);border:1px solid rgba(80,200,112,0.25);color:#70e890',
    'CC (침묵)':'background:rgba(200,80,200,0.12);border:1px solid rgba(200,80,200,0.25);color:#d080d0',
    'CC (부유)':'background:rgba(200,80,200,0.12);border:1px solid rgba(200,80,200,0.25);color:#d080d0',
    '힐':'background:rgba(80,200,112,0.12);border:1px solid rgba(80,200,112,0.25);color:#70e890',
    '힐 DoT':'background:rgba(80,200,112,0.12);border:1px solid rgba(80,200,112,0.25);color:#70e890',
    '버프→광역':'background:rgba(200,140,0,0.15);border:1px solid rgba(200,140,0,0.3);color:#ffb020',
    '공격/버프':'background:rgba(232,192,80,0.1);border:1px solid rgba(232,192,80,0.25);color:#e8c050',
    'DoT (6틱)':'background:rgba(255,120,40,0.12);border:1px solid rgba(255,120,40,0.25);color:#ff9060',
    'DoT 5틱':'background:rgba(255,120,40,0.12);border:1px solid rgba(255,120,40,0.25);color:#ff9060',
    '2타':'background:rgba(212,48,48,0.15);border:1px solid rgba(212,48,48,0.3);color:#ff8080',
    '6타 연속':'background:rgba(212,48,48,0.15);border:1px solid rgba(212,48,48,0.3);color:#ff8080',
    '방향 투사체':'background:rgba(128,216,64,0.15);border:1px solid rgba(128,216,64,0.3);color:#a0e860',
    '방향 범위':'background:rgba(128,216,64,0.12);border:1px solid rgba(128,216,64,0.25);color:#90d850',
    '위치지정 범위':'background:rgba(232,192,80,0.1);border:1px solid rgba(232,192,80,0.25);color:#e8c050',
    '방향 공격+버프':'background:rgba(128,216,64,0.12);border:1px solid rgba(128,216,64,0.25);color:#a0e860',
    '이동':'background:rgba(80,200,112,0.12);border:1px solid rgba(80,200,112,0.25);color:#70e890',
  };
  grid.innerHTML = data.map(w => {
    const skillRows = w.skills.map(s => {
      const ts = typeStyle[s.type] || 'background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:var(--text2)';
      const dmgTxt = s.dmg > 0 ? `${(s.dmg*100).toFixed(0)}%` : '—';
      const cdTxt = s.cd > 0 ? `${s.cd}s` : '기본';
      return `
        <div class="skill-row">
          <div class="skill-cmd cmd-${s.cmd}">${s.cmd}</div>
          <div></div>
          <div>
            <div class="skill-name">${s.name}</div>
            <div style="display:flex;gap:4px;margin-top:2px;flex-wrap:wrap">
              <span class="skill-type-badge" style="${ts}">${s.type}</span>
              <span style="font-size:0.65rem;color:var(--text3)">CD ${cdTxt}</span>
              ${s.mp>0?`<span style="font-size:0.65rem;color:#6080ff">MP ${s.mp}</span>`:''}
            </div>
          </div>
          <div class="skill-dmg">${dmgTxt}</div>
        </div>`;
    }).join('');
    return `
    <div class="weapon-card">
      <div class="weapon-card-head">
        <span class="weapon-icon">${w.icon}</span>
        <div>
          <div class="weapon-name" style="color:${w.color}">${w.weapon}</div>
          <div class="weapon-concept">${w.concept}</div>
        </div>
      </div>
      <div class="weapon-card-body">${skillRows}</div>
    </div>`;
  }).join('');
}

function switchSkillTier(t, btn) {
  skillTier = t;
  btn.closest('.tab-bar').querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderWeaponTier(t);
}

function renderWeapons() { ['1','2','3'].forEach(t => renderWeaponTier(t)); }

function renderDPS() {
  const cmdColors = {Q:'#f5d878',W:'#70e890',E:'#70b8ff',R:'#ff7070'};
  document.getElementById('dps-chart-inner').innerHTML = DPS_DATA.map(d => {
    const total = d.Q+d.W+d.E+d.R;
    const bars = ['Q','W','E','R'].map(cmd => `
      <div class="dps-bar-item">
        <div class="dps-bar-label" style="color:${cmdColors[cmd]}">${cmd}</div>
        <div class="dps-bar-track">
          <div class="dps-bar-fill" style="width:${d[cmd]/40*100}%;background:${cmdColors[cmd]}80"></div>
        </div>
        <div class="dps-bar-val" style="color:${cmdColors[cmd]}">${d[cmd]||'-'}</div>
      </div>`).join('');
    return `
      <div class="dps-bar-row">
        <div class="dps-weapon">${d.weapon}</div>
        <div class="dps-bars">${bars}</div>
        <div style="width:60px;text-align:right;font-family:'Cinzel Decorative',serif;font-size:0.8rem;color:var(--gold2)">합계 ${total}</div>
      </div>`;
  }).join('');
}

// ═══════════ ITEM LIST ═══════════
function filterList(type, val, btn) {
  if (type==='tier') { listTierF = val; [...btn.parentNode.querySelectorAll('.filter-btn')].slice(0,4).forEach(b=>b.classList.remove('active')); }
  else { listObtF = val; [...btn.parentNode.querySelectorAll('.filter-btn')].slice(4).forEach(b=>b.classList.remove('active')); }
  btn.classList.add('active');
  renderItemList();
}

function renderItemList() {
  const tbody = document.getElementById('item-list-body');
  if (!tbody) return;
  const obtColor = {'기본 제작':'#80e080','전리품 제작':'#e8c050','던전 코어 제작':'#b060ff','보스 드랍':'#ff7070'};
  const data = ITEM_LIST.filter(d => {
    if (listTierF !== 'all' && d.tier !== listTierF) return false;
    if (listObtF !== 'all' && d.obt !== listObtF) return false;
    return true;
  });
  tbody.innerHTML = data.map(d => `
    <tr>
      <td><span class="td-badge" style="background:rgba(232,192,80,0.1);border:1px solid rgba(232,192,80,0.25);color:var(--gold)">${d.tier}</span></td>
      <td><span class="td-badge" style="${`background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:${obtColor[d.obt]||'#ccc'}`}">${d.obt}</span></td>
      <td style="color:var(--text2)">${d.mat}</td>
      <td>${d.slot}</td>
      <td style="color:var(--cream);font-weight:500">${d.p1}</td>
      <td style="color:${d.p2!=='-'?'var(--text)':'var(--text3)'}">${d.p2}</td>
      <td style="color:${d.p3!=='-'?'var(--text)':'var(--text3)'}">${d.p3}</td>
    </tr>`).join('');
}

// ═══════════ DELEGATED EVENT HANDLERS ═══════════
document.addEventListener('DOMContentLoaded', function() {
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('[data-action]');
    if (!btn) return;
    var action = btn.dataset.action;
    if (action === 'nav') { showSection(btn.dataset.s); } 
    else if (action === 'tab') { switchTab(btn.dataset.s, btn.dataset.t, btn); } 
    else if (action === 'filter-list') { filterList(btn.dataset.type, btn.dataset.val, btn); } 
    else if (action === 'filter-armor') { filterArmor(btn.dataset.type, btn.dataset.val, btn); }
  });
  document.addEventListener('input', function(e) {
    if (e.target.dataset.action === 'search-armor') { searchArmor(e.target.value); }
  });
  renderArmorTier('1T'); renderArmorTier('2T'); renderArmorTier('3T');
  renderDPS(); renderWeaponTier('1'); renderWeaponTier('2'); renderWeaponTier('3'); renderItemList();
});
