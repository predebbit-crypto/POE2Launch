# Python 설치 가이드

`build.bat` 실행 시 "pip은(는) 내부 또는 외부 명령이 아닙니다" 오류가 발생하나요?

Python이 설치되지 않았거나 PATH에 추가되지 않은 상태입니다.

## 🐍 Python 설치 방법

### 1단계: Python 다운로드

**공식 사이트에서 다운로드:**
- https://www.python.org/downloads/
- **"Download Python 3.x.x"** 버튼 클릭 (가장 최신 버전)

**또는 직접 링크:**
- Windows 64bit: https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
- Windows 32bit: https://www.python.org/ftp/python/3.12.0/python-3.12.0.exe

### 2단계: Python 설치

1. **다운로드한 설치 파일 실행**

2. ⚠️ **매우 중요!** 설치 시작 화면에서:
   ```
   ☑️ Add Python to PATH    <-- 반드시 체크!
   ```
   이 옵션을 체크하지 않으면 명령 프롬프트에서 Python을 사용할 수 없습니다!

3. **"Install Now"** 클릭

4. 설치 완료까지 대기 (약 1-2분)

5. **"Close"** 클릭

### 3단계: 설치 확인

1. **명령 프롬프트 새로 열기** (기존 창은 닫고 새로 열어야 합니다!)

2. 다음 명령어 실행:
   ```cmd
   python --version
   ```

3. 다음과 같이 출력되면 성공:
   ```
   Python 3.12.0
   ```

4. pip 확인:
   ```cmd
   pip --version
   ```

   출력 예:
   ```
   pip 23.x.x from C:\Users\...\Python\...
   ```

---

## 🔧 이미 Python이 설치되어 있는 경우

Python은 설치되어 있지만 PATH에 추가되지 않은 경우:

### 방법 1: Python 재설치 (권장)

1. 제어판 → 프로그램 제거 → Python 제거
2. 위의 **"Python 설치 방법"** 다시 따라하기
3. **"Add Python to PATH"** 반드시 체크!

### 방법 2: 수동으로 PATH 추가

1. **Windows 검색**에서 "환경 변수" 검색
2. **"시스템 환경 변수 편집"** 클릭
3. **"환경 변수"** 버튼 클릭
4. **시스템 변수**에서 **"Path"** 선택 → **"편집"** 클릭
5. **"새로 만들기"** 클릭하고 다음 경로 추가:
   ```
   C:\Users\[사용자명]\AppData\Local\Programs\Python\Python312
   C:\Users\[사용자명]\AppData\Local\Programs\Python\Python312\Scripts
   ```
   (Python 설치 경로에 따라 다를 수 있습니다)

6. **확인** → **확인** → **확인**
7. **명령 프롬프트 새로 열기**
8. `python --version` 으로 확인

---

## 🚀 설치 후 다음 단계

Python 설치가 완료되면:

1. **명령 프롬프트 새로 열기** (필수!)

2. POE2Launch 폴더로 이동:
   ```cmd
   cd C:\Users\sheli\Downloads\POE2Launch
   ```

3. 빌드 스크립트 실행:
   ```cmd
   build.bat
   ```

4. 성공! 🎉

---

## ❓ 자주 묻는 질문

### Q: Python을 설치했는데도 "pip을 찾을 수 없습니다" 오류가 나요

**A:** 명령 프롬프트를 새로 열었나요?
- 기존 명령 프롬프트 창을 **완전히 닫기**
- 새로운 명령 프롬프트 **다시 열기**
- Python 설치 후 환경 변수가 적용되려면 새 창이 필요합니다

### Q: "Add Python to PATH"를 체크하지 않고 설치했어요

**A:** 두 가지 방법이 있습니다:
1. **방법 1 (권장):** Python 제거 후 재설치
   - 제어판 → 프로그램 제거 → Python 제거
   - 다시 설치하면서 "Add Python to PATH" 체크

2. **방법 2:** 위의 "수동으로 PATH 추가" 참고

### Q: Python 2.x 버전이 설치되어 있어요

**A:** Python 3.8 이상이 필요합니다
- Python 3.x를 추가로 설치하세요 (2.x와 공존 가능)
- 또는 Python 2.x 제거 후 Python 3.x 설치

### Q: Microsoft Store에서 Python을 설치해도 되나요?

**A:** 네, 가능합니다!
- Microsoft Store에서 "Python 3.12" 검색
- 설치하면 자동으로 PATH에 추가됩니다
- 하지만 공식 사이트 설치를 더 권장합니다

---

## 💡 Python 없이 사용하는 방법

Python 설치가 어렵다면:

### 옵션 1: 다른 사람이 빌드한 exe 사용
- Python이 설치된 다른 컴퓨터에서 빌드
- `dist` 폴더의 exe 파일만 복사해서 사용
- exe 파일은 Python 없이도 실행 가능

### 옵션 2: 온라인 빌드 서비스 사용 (고급)
- GitHub Actions를 사용한 자동 빌드
- 이 방법은 GitHub 사용 경험이 필요합니다

---

## 📞 도움이 필요하시면

그래도 문제가 해결되지 않으면:
1. 오류 메시지 전체를 캡처
2. `python --version` 실행 결과
3. `pip --version` 실행 결과
4. GitHub Issues에 문의

---

**Python 설치 후 즐거운 게임 되세요! 🎮**
