# 빠른 시작 가이드 (5분 완성!)

POE2 Auto Login Launcher를 빠르게 시작하는 방법입니다.

## ⚡ 3단계로 시작하기

### 1️⃣ 다운로드 및 빌드

Windows 명령 프롬프트에서:

```cmd
git clone https://github.com/predebbit-crypto/POE2Launch.git
cd POE2Launch
build.bat
```

빌드가 완료될 때까지 1-2분 대기...

### 2️⃣ 계정 설정

```cmd
cd dist
POE2_Setup.exe
```

프로그램이 실행되면:
1. 다음 아이디 입력
2. 비밀번호 입력 (화면에 표시 안 됨)
3. 비밀번호 다시 입력
4. Enter!

### 3️⃣ 실행

```cmd
POE2_Launcher.exe
```

끝! 🎉

---

## 📋 체크리스트

빌드 전에 확인하세요:
- [ ] Chrome 브라우저 설치됨
- [ ] Python 3.8 이상 설치됨
- [ ] 인터넷 연결됨

계정 설정 전에 확인하세요:
- [ ] Path of Exile 2 다음 계정 있음
- [ ] 아이디와 비밀번호 정확히 알고 있음

실행 전에 확인하세요:
- [ ] config.json 파일이 dist 폴더에 있음
- [ ] Chrome 브라우저가 닫혀 있음 (자동으로 열림)

---

## 🎯 실행 흐름

```
POE2_Setup.exe
    ↓
계정 정보 입력
    ↓
config.json 생성 ✅
    ↓
POE2_Launcher.exe
    ↓
Chrome 자동 실행
    ↓
POE2 사이트 접속
    ↓
자동 로그인
    ↓
게임시작 버튼 클릭
    ↓
게임 런처 실행 🎮
```

---

## ❓ 문제 발생 시

### "config.json을 찾을 수 없습니다"
→ `POE2_Setup.exe`를 먼저 실행하세요

### "로그인 실패"
→ config.json의 아이디/비밀번호가 맞는지 확인하세요

### "Chrome 드라이버 오류"
→ Chrome 브라우저를 최신 버전으로 업데이트하세요

### 기타 문제
→ [SETUP_GUIDE.md](SETUP_GUIDE.md)의 문제 해결 섹션 참고

---

## 💡 팁

**빠른 재실행:**
- 한 번 설정하면 config.json은 계속 사용됩니다
- 다음부터는 `POE2_Launcher.exe`만 실행하면 됩니다

**비밀번호 변경:**
- `POE2_Setup.exe`를 다시 실행하면 됩니다
- 또는 config.json 파일을 직접 편집

**안전하게 사용:**
- 사용 후 config.json 삭제를 권장합니다
- 다음 사용 시 POE2_Setup.exe로 다시 설정

---

**더 자세한 내용은 [SETUP_GUIDE.md](SETUP_GUIDE.md)를 참고하세요!**
