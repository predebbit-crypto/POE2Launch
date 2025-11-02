# POE2 Auto Login Launcher

Path of Exile 2 다음 게임 사이트 자동 로그인 런처

## 기능

1. ✅ https://pathofexile2.game.daum.net/ 자동 접속
2. ✅ 저장된 다음 계정으로 자동 로그인
3. ✅ 로그인 완료 후 '게임시작' 버튼 자동 클릭

## 사용 방법

### 1단계: 준비물

- Windows 10/11 (64bit)
- Chrome 브라우저 설치 필수
- 다음 계정 (Path of Exile 2 계정)

### 2단계: 빌드 (처음 한 번만)

#### Windows:
```bash
# 명령 프롬프트(cmd) 또는 PowerShell에서 실행
build.bat
```

#### Linux/Mac:
```bash
# 터미널에서 실행
chmod +x build.sh
./build.sh
```

### 3단계: 설정

1. `dist` 폴더로 이동
2. `config.json` 파일을 텍스트 에디터로 열기
3. 다음 계정 정보 입력:

```json
{
  "username": "your_daum_id",
  "password": "your_password"
}
```

⚠️ **중요**:
- `config.json` 파일에는 실제 계정 정보가 들어가므로 절대 공유하지 마세요!
- 파일은 평문으로 저장되니 보안에 주의하세요.

### 4단계: 실행

#### Windows:
`dist` 폴더의 `POE2_Launcher.exe` 더블클릭

#### Linux/Mac:
```bash
cd dist
./POE2_Launcher
```

## 작동 방식

1. 🌐 Chrome 브라우저가 자동으로 열립니다
2. 🔐 POE2 다음 사이트에서 자동 로그인을 시도합니다
3. 🎮 로그인 성공 후 '게임시작' 버튼을 자동으로 클릭합니다
4. ⏸️  게임 런처가 실행될 때까지 브라우저를 유지합니다

## 문제 해결

### 로그인이 안 되는 경우:
- config.json 파일의 아이디/비밀번호가 정확한지 확인
- 다음 계정이 2단계 인증을 사용하는 경우, 수동으로 인증 필요
- 프로그램이 30초간 대기하므로 그 동안 수동으로 로그인 가능

### '게임시작' 버튼을 못 찾는 경우:
- 웹사이트 구조가 변경되었을 수 있습니다
- 화면에 버튼이 표시되면 수동으로 클릭하세요
- 브라우저는 계속 열려있으므로 수동 조작 가능

### Chrome 드라이버 오류:
- Chrome 브라우저가 최신 버전인지 확인
- 인터넷 연결 상태 확인 (드라이버 자동 다운로드 필요)

## 개발자 모드 (테스트용)

Python이 설치되어 있다면 빌드 없이 바로 실행 가능:

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python poe2_launcher.py
```

## 파일 구조

```
POE2Launch/
├── poe2_launcher.py      # 메인 런처 스크립트
├── requirements.txt      # Python 의존성
├── config.json.example   # 설정 파일 예시
├── build.bat            # Windows 빌드 스크립트
├── build.sh             # Linux/Mac 빌드 스크립트
├── README.md            # 이 파일
└── dist/                # 빌드된 실행 파일 (빌드 후 생성)
    ├── POE2_Launcher.exe  # Windows 실행 파일
    └── config.json        # 계정 설정 파일
```

## 주의사항

⚠️ **보안 주의사항**:
- 이 프로그램은 로컬에서만 작동하며 계정 정보를 외부로 전송하지 않습니다
- config.json 파일은 평문으로 저장되므로 다른 사람과 공유하지 마세요
- 공용 컴퓨터에서는 사용을 권장하지 않습니다

⚠️ **이용 약관**:
- 이 프로그램은 개인 편의를 위한 도구입니다
- 게임 이용약관 위반 여부는 사용자 책임입니다
- 자동화 프로그램 사용이 금지된 경우 사용하지 마세요

## 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다.

## 기술 스택

- Python 3.x
- Selenium WebDriver
- Chrome WebDriver
- PyInstaller

---

Made with ❤️ for POE2 Players
