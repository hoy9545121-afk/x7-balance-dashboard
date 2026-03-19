# X7 전투 시뮬레이터 (AI Simulator)

디자이너와 개발자를 위한 X7 게임 전투 밸런스 검증 툴입니다.

## 🚀 실행 방법

```bash
# 저장소 루트 이동 후 실행
streamlit run app.py
```
브라우저에서 `http://localhost:8501`으로 자동 접속됩니다.

## 📖 프로젝트 사양서 (Source of Truth)

프로젝트의 모든 수식과 기획 수치는 아래 두 문서를 절대적인 기준으로 합니다.

- [**GAME_SPEC.md**](./GAME_SPEC.md): **전투 시스템 사양** (데미지 공식, 스탯 캡, 스킬 계수 등)
- [**ECON_SPEC.md**](./ECON_SPEC.md): **경제 및 성장 사양** (레벨별 경험치, 숙련도, 제작/드랍 로직 등)

## 📂 주요 구조

- `app.py`: 메인 진입점 (UI 레이아웃 및 모드 관리)
- `simulator/`: 핵심 로직
  - `engine.py`: 60초 전투 시뮬레이션 엔진
  - `calc.py`: 데미지 및 스탯 계산 공식
  - `constants.py`: 게임 데이터 (계수, 몬스터 스탯 등)
- `ui/`: Streamlit 컴포넌트 (캐릭터 카드, 몬스터 패널, 결과 뷰어)
- `charts/`: Plotly 기반 데이터 시각화

## 📖 문서 가이드

- [GAME_SPEC.md](./GAME_SPEC.md): 전투 밸런스 및 시스템 사양서
- [ECON_SPEC.md](./ECON_SPEC.md): 성장·경제·드랍 설계 사양서
- [CHANGELOG.md](./CHANGELOG.md): 밸런스 수정 및 업데이트 이력
- [CLAUDE.md](./CLAUDE.md): 개발자를 위한 아키텍처 가이드
