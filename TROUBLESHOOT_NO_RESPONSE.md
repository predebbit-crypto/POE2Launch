# 실행이 안 될 때 문제 해결 가이드

POE2_Launcher.exe를 실행했는데 아무 반응이 없나요? 이 가이드를 따라해보세요.

## 🔍 문제 진단

### 1단계: 다시 빌드하기

업데이트된 코드로 다시 빌드해야 합니다. 이제 **콘솔 창이 표시**되어 오류 메시지를 확인할 수 있습니다.

```cmd
cd C:\Users\sheli\Downloads\POE2Launch
build.bat
```

새로 빌드된 파일로 다시 시도하세요.

---

## 🐛 가능한 원인과 해결 방법

### 원인 1: config.json 파일이 없음

**증상:**
- 프로그램이 바로 종료됨
- 콘솔 창에 "설정 파일을 찾을 수 없습니다" 메시지

**해결 방법:**
```cmd
cd dist
POE2_Setup.exe
```

또는 수동으로 config.json 생성

---

### 원인 2: Chrome 브라우저 문제

**증상:**
- "브라우저 설정 실패" 메시지
- Chrome이 열리지 않음

**해결 방법:**

#### A. Chrome 브라우저 확인
1. Chrome이 설치되어 있나요?
   - 설치: https://www.google.com/chrome/
2. Chrome 버전 확인 (chrome://version/)
   - 주소창에 `chrome://version/` 입력
   - 버전 확인 (현재 141.x 사용 중이면 OK)

#### B. Chrome 업데이트
```
Chrome 실행 → 우측 상단 ⋮ → 도움말 → Chrome 정보
→ 자동 업데이트 진행
```

#### C. WebDriver 캐시 삭제
```cmd
# WebDriver 캐시 폴더 삭제
rmdir /s /q "%USERPROFILE%\.wdm"
```

그 다음 POE2_Launcher.exe 다시 실행

---

### 원인 3: 백신 프로그램 차단

**증상:**
- 프로그램이 시작하자마자 종료
- 백신 경고 메시지

**해결 방법:**

#### Windows Defender 예외 추가:
1. Windows 설정 열기 (Win + I)
2. "업데이트 및 보안" → "Windows 보안"
3. "바이러스 및 위협 방지" 클릭
4. "설정 관리" 클릭
5. "제외 추가" → "폴더"
6. `C:\Users\sheli\Downloads\POE2Launch\dist` 폴더 선택

#### 기타 백신 프로그램:
- 해당 백신의 설정에서 POE2Launch 폴더를 예외로 추가

---

### 원인 4: 인터넷 연결 문제

**증상:**
- "WebDriver 다운로드 실패" 메시지
- Chrome은 있지만 드라이버 다운로드 안 됨

**해결 방법:**
1. 인터넷 연결 확인
2. 방화벽 설정 확인
3. 프록시 설정 확인

---

### 원인 5: 관리자 권한 필요

**해결 방법:**
1. `POE2_Launcher.exe` 우클릭
2. "관리자 권한으로 실행" 클릭

---

## 📝 로그 파일 확인하기

이제 프로그램이 실행되면 **poe2_launcher.log** 파일이 생성됩니다.

**로그 파일 위치:**
```
C:\Users\sheli\Downloads\POE2Launch\dist\poe2_launcher.log
```

**로그 파일 열기:**
```cmd
cd C:\Users\sheli\Downloads\POE2Launch\dist
notepad poe2_launcher.log
```

로그 파일에서 오류 메시지를 확인할 수 있습니다.

---

## 🧪 디버그 모드로 실행하기

Python이 설치되어 있다면 직접 스크립트를 실행하여 더 자세한 오류 확인:

```cmd
cd C:\Users\sheli\Downloads\POE2Launch
python poe2_launcher.py
```

이렇게 하면 콘솔에 모든 메시지가 출력됩니다.

---

## ✅ 체크리스트

빌드 후 다시 시도하기 전에 확인:

- [ ] 최신 코드로 다시 빌드했다 (`build.bat`)
- [ ] `dist` 폴더에 `config.json` 파일이 있다
- [ ] Chrome 브라우저가 설치되어 있다 (버전 141.x OK)
- [ ] 백신 프로그램 예외 설정 완료
- [ ] 인터넷 연결 정상
- [ ] 콘솔 창이 표시되는 새 버전을 실행했다

---

## 🆘 그래도 안 되면?

다음 정보를 수집하여 문의하세요:

1. **콘솔 창 메시지** (스크린샷)
2. **poe2_launcher.log 파일 내용**
3. **Chrome 버전** (chrome://version/)
4. **Windows 버전**
5. **백신 프로그램 이름**

---

## 💡 임시 해결 방법

exe 파일이 계속 작동하지 않으면 Python으로 직접 실행:

```cmd
# 1. Python 의존성 설치
pip install -r requirements.txt

# 2. 설정 도구 실행
python setup_config.py

# 3. 런처 실행
python poe2_launcher.py
```

이 방법은 Python이 설치되어 있어야 합니다.

---

**새 버전으로 다시 빌드 후 시도해보시고, 여전히 문제가 있으면 로그 파일을 확인해주세요!** 📋
