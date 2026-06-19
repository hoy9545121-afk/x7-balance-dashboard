"""에셋 복사 스크립트 — 로컬 개발용
리소스/assets/ → X7_closet_sim/assets/ 로 복사합니다.
Git 업로드 / Streamlit Cloud 배포 전 1회 실행.

사용법:
    python setup_assets.py
"""
import shutil
from pathlib import Path

SRC  = Path(__file__).parent.parent / "리소스" / "assets"
DEST = Path(__file__).parent / "assets"

if not SRC.exists():
    print(f"[ERROR] 소스 경로를 찾을 수 없습니다: {SRC}")
    raise SystemExit(1)

if DEST.exists():
    print(f"[INFO]  기존 assets/ 폴더 삭제 중…")
    shutil.rmtree(DEST)

print(f"[INFO]  {SRC} → {DEST} 복사 중…")
shutil.copytree(SRC, DEST)

# 파일 수 확인
copied = list(DEST.rglob("*.png"))
print(f"[OK]    복사 완료 — PNG {len(copied)}개")
print(f"        경로: {DEST}")
