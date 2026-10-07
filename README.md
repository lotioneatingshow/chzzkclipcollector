# 치지직 클립 수집기 (Chzzk Clip Collector)

치지직(CHZZK) 스트리머의 클립 데이터를 간편하게 수집하고 엑셀(`.xlsx`) 파일로 정리해 주는 Desktop GUI 프로그램입니다. 팬 커뮤니티의 클립 정리 및 개인 소장 목적으로 제작되었습니다.

---

## 📌 주요 기능

- **신규 채널 수집**: 채널 코드를 입력하여 해당 채널의 모든 클립 메타데이터(제목, 링크, 클립 UID, 생성 일자)를 일괄 수집합니다.
- **기존 채널 최신화**: 기존에 저장된 엑셀/CSV 파일을 기반으로, 새로 추가된 신규 클립만 빠르게 업데이트합니다.
- **깔끔한 엑셀 출력**: 
  - 클릭 가능한 하이퍼링크 및 엑셀 표(Table) 스타일 자동 적용
  - 날짜 서식 설정 및 첫 행(헤더) 고정
- **사용자 친화적 GUI (Tkinter)**:
  - **화이트 / 다크 테마** 지원 (`⚙ 설정` 메뉴에서 변경 가능)
  - 채널 검색 및 페이지네이션 기능
  - 실시간 실행 로그 및 진행 상태 표시
- **서버 보호 및 IP 차단 방지**:
  - API 연속 호출 간 딜레이 및 채널 간 대기 시간 자동 적용
  - 요청 실패 시 지연 재시도(Exponential Backoff) 로직 탑재

---

## ⚠️ 사용 전 주의사항

> 1. 본 프로그램은 **스트리머 팬분들의 클립 정리 및 소장 목적**으로 제작된 비상업적 개인 프로젝트입니다.
> 2. 치지직 서버 부하 방지 및 IP 차단을 예방하기 위해 수집 대기 시간(Delay)이 설정되어 있습니다.
> 3. 단시간에 수십 개 이상의 채널을 연속으로 최신화할 경우 치지직 측의 보안 정책에 의해 일시적인 IP 차단(`HTTP 429 Too Many Requests`)이 발생할 수 있으니 적절한 간격을 두고 사용해 주세요.

---

## 🚀 다운로드 및 실행 방법

### 방법 1. 실행 파일(.exe) 다운로드 (권장)
1. 우측의 **[Releases]** 탭에서 최신 버전의 `ChzzkClipCollector.exe` 파일을 다운로드합니다.
2. 다운로드한 `.exe` 파일을 실행합니다. (별도의 설치 과정 없이 즉시 실행됩니다.)
3. 수집된 클립 파일은 프로그램이 위치한 폴더 내 `files/` 디렉토리에 자동 저장됩니다.

### 방법 2. 파이썬 소스코드 직접 실행

#### 필수 요구 사항
- Python 3.10 이상

#### 패키지 설치
```bash
pip install requests openpyxl
```

#### 프로그램 실행
```bash
python main.py
```
---
## 🛠 실행 파일(.exe) 직접 빌드하기
PyInstaller를 이용해 독립 실행 파일로 패키징할 수 있습니다.
```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --icon=res/icon.ico --add-data "res;res" --name ChzzkClipCollector-vx.x.x main.py
```
---
## 📁 프로젝트 구조
```plaintext
ChzzkClipCollector/
├── config/             # 설정 파일 저장 폴더 (settings.json)
├── files/              # 수집된 엑셀(.xlsx) 파일 저장 폴더
├── gui/                # Tkinter 기반 GUI 모듈
│   ├── app.py          # 메인 애플리케이션 클래스
│   ├── new_channel.py  # 신규 채널 수집 패널
│   ├── update_channel.py # 기존 채널 최신화 패널
│   ├── settings.py     # 설정 창
│   ├── theme.py        # 테마(화이트/다크) 관련 색상 정의
│   ├── widgets.py      # UI 보조 위젯 및 유틸리티
│   └── worker.py       # 백그라운드 비동기 스레드 관리자
├── res/                # 아이콘 등 리소스 파일 (icon.ico)
├── chzzk_api.py        # 치지직 API 통신 및 데이터 처리
├── config.py           # API 엔드포인트 및 요청 헤더 설정
├── excel_manager.py    # openpyxl 기반 엑셀 생성 및 스타일링
├── file_manager.py     # 기존 수집 파일 탐색 및 읽기
├── utils.py            # 날짜 파싱 및 파일명 정화 함수
└── main.py             # 프로그램 엔트리포인트
```
---
## 📄 라이선스 및 안내
본 프로그램은 치지직(CHZZK)의 비공식 API를 이용하는 오픈소스 프로젝트입니다. 치지직 서비스 환경이나 API 사양 변경에 따라 일부 기능이 작동하지 않을 수 있습니다.