"""
POE2 Auto Login Launcher
Path of Exile 2 다음 게임 자동 로그인 런처
"""

import json
import os
import sys
import time
import traceback
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# 로그 설정
def setup_logging():
    """로그 파일 설정"""
    log_dir = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        log_dir = os.path.dirname(sys.executable)

    log_file = os.path.join(log_dir, 'poe2_launcher.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_file


LOG_FILE = setup_logging()


class POE2Launcher:
    def __init__(self, config_path='config.json'):
        """POE2 런처 초기화"""
        self.config = self.load_config(config_path)
        self.driver = None
        self.wait = None

    def load_config(self, config_path):
        """설정 파일 로드"""
        logging.info(f"설정 파일 로드 시도: {config_path}")

        if not os.path.exists(config_path):
            msg = f"❌ 설정 파일을 찾을 수 없습니다: {config_path}"
            logging.error(msg)
            print(msg)
            print(f"📝 config.json 파일을 생성하고 계정 정보를 입력해주세요.")
            print(f"\n예시:")
            print(f'{{\n  "username": "your_username",\n  "password": "your_password"\n}}')
            print(f"\n💡 POE2_Setup.exe를 실행하여 쉽게 설정할 수 있습니다.")
            input("\n계속하려면 Enter를 누르세요...")
            sys.exit(1)

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if 'username' not in config or 'password' not in config:
                msg = "❌ 설정 파일에 username 또는 password가 없습니다."
                logging.error(msg)
                print(msg)
                input("\n계속하려면 Enter를 누르세요...")
                sys.exit(1)

            logging.info("설정 파일 로드 성공")
            return config
        except json.JSONDecodeError as e:
            msg = f"❌ 설정 파일 파싱 오류: {e}"
            logging.error(msg)
            print(msg)
            input("\n계속하려면 Enter를 누르세요...")
            sys.exit(1)
        except Exception as e:
            msg = f"❌ 설정 파일 읽기 오류: {e}"
            logging.error(msg)
            print(msg)
            input("\n계속하려면 Enter를 누르세요...")
            sys.exit(1)

    def setup_driver(self):
        """Chrome 드라이버 설정"""
        print("🔧 브라우저 설정 중...")
        logging.info("Chrome 드라이버 설정 시작")

        chrome_options = Options()
        # 브라우저를 보이게 설정
        # chrome_options.add_argument('--headless')  # 숨기려면 주석 해제
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # 자동화 감지 방지
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            print("📥 Chrome WebDriver 준비 중... (처음 실행 시 시간이 걸릴 수 있습니다)")

            # Selenium 4.6+는 자체 Selenium Manager를 사용하여 드라이버 관리
            # Service()를 인자 없이 호출하면 자동으로 드라이버를 찾거나 다운로드
            try:
                logging.info("Selenium Manager로 드라이버 자동 설정 시도")
                service = Service()

                print("🌐 Chrome 브라우저 시작 중...")
                logging.info("Chrome 브라우저 시작")
                self.driver = webdriver.Chrome(service=service, options=chrome_options)

            except Exception as selenium_error:
                # Selenium Manager 실패 시 ChromeDriverManager로 폴백
                logging.warning(f"Selenium Manager 실패: {selenium_error}")
                logging.info("ChromeDriverManager로 드라이버 설치 시도 (폴백)")
                print("🔄 대체 방법으로 WebDriver 다운로드 중...")

                # 캐시 문제를 피하기 위해 최신 버전 강제 다운로드
                from webdriver_manager.chrome import ChromeDriverManager
                driver_path = ChromeDriverManager().install()
                logging.info(f"드라이버 경로: {driver_path}")

                # 경로가 올바른 chromedriver.exe를 가리키는지 확인
                if not driver_path.endswith('chromedriver.exe'):
                    # chromedriver.exe 파일 찾기
                    import glob
                    driver_dir = os.path.dirname(driver_path)
                    possible_drivers = glob.glob(os.path.join(driver_dir, '**/chromedriver.exe'), recursive=True)
                    if possible_drivers:
                        driver_path = possible_drivers[0]
                        logging.info(f"올바른 드라이버 파일 찾음: {driver_path}")
                    else:
                        # 상위 디렉토리에서 찾기
                        parent_dir = os.path.dirname(driver_dir)
                        possible_drivers = glob.glob(os.path.join(parent_dir, '**/chromedriver.exe'), recursive=True)
                        if possible_drivers:
                            driver_path = possible_drivers[0]
                            logging.info(f"상위 디렉토리에서 드라이버 찾음: {driver_path}")

                service = Service(driver_path)

                print("🌐 Chrome 브라우저 시작 중...")
                logging.info("Chrome 브라우저 시작")
                self.driver = webdriver.Chrome(service=service, options=chrome_options)

            self.wait = WebDriverWait(self.driver, 20)

            # 자동화 감지 방지 스크립트
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            print("✅ 브라우저 설정 완료")
            logging.info("Chrome 브라우저 설정 완료")

        except Exception as e:
            error_msg = f"❌ 브라우저 설정 실패: {e}"
            print(error_msg)
            logging.error(error_msg)
            logging.error(traceback.format_exc())

            print("\n💡 문제 해결 방법:")
            print("1. WebDriver 캐시 삭제:")
            print('   명령 프롬프트에서: rmdir /s /q "%USERPROFILE%\\.wdm"')
            print("2. Chrome 브라우저가 설치되어 있는지 확인하세요")
            print("3. Chrome을 최신 버전으로 업데이트하세요")
            print("4. 인터넷 연결을 확인하세요")
            print("5. 백신 프로그램이 차단하고 있는지 확인하세요")
            print(f"\n📝 자세한 로그는 다음 파일을 확인하세요: {LOG_FILE}")

            input("\n계속하려면 Enter를 누르세요...")
            sys.exit(1)

    def open_website(self):
        """POE2 다음 게임 사이트 열기"""
        url = "https://pathofexile2.game.daum.net/"
        print(f"🌐 웹사이트 열기: {url}")

        try:
            self.driver.get(url)
            print("✅ 웹사이트 로드 완료")
            time.sleep(2)
        except Exception as e:
            print(f"❌ 웹사이트 열기 실패: {e}")
            self.cleanup()
            sys.exit(1)

    def login(self):
        """자동 로그인 (게임 시작 버튼 클릭 후 나타나는 로그인 창에서)"""
        print("🔐 로그인 시도 중...")
        logging.info("로그인 프로세스 시작")

        try:
            # 로그인 창/팝업으로 전환 (iframe, 새 창, 팝업 등 확인)
            # 먼저 iframe이 있는지 확인
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                logging.info(f"iframe 발견: {len(iframes)}개")
                # 첫 번째 iframe으로 전환 시도
                try:
                    self.driver.switch_to.frame(iframes[0])
                    print("📋 로그인 프레임으로 전환")
                    logging.info("iframe으로 전환 성공")
                except Exception as e:
                    logging.warning(f"iframe 전환 실패: {e}")

            # 팝업 창이 있는지 확인
            window_handles = self.driver.window_handles
            if len(window_handles) > 1:
                logging.info(f"팝업 창 발견: {len(window_handles)}개")
                self.driver.switch_to.window(window_handles[-1])
                print("🪟 로그인 팝업 창으로 전환")
                logging.info("팝업 창으로 전환 성공")

            # 로그인 입력 필드가 나타날 때까지 대기
            time.sleep(2)

            # 아이디 입력
            id_input_selectors = [
                "//input[@name='id']",
                "//input[@id='id']",
                "//input[@name='username']",
                "//input[@id='username']",
                "//input[@type='text']",
                "//input[@placeholder*='아이디']",
                "//input[@placeholder*='ID']",
                "//input[contains(@class, 'input_id')]",
                "//input[contains(@class, 'tf_id')]"
            ]

            id_entered = False
            for selector in id_input_selectors:
                try:
                    logging.info(f"아이디 입력 시도: {selector}")
                    id_input = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    id_input.clear()
                    id_input.send_keys(self.config['username'])
                    print("✅ 아이디 입력 완료")
                    logging.info("아이디 입력 성공")
                    id_entered = True
                    break
                except Exception as e:
                    logging.debug(f"아이디 입력 실패: {selector} - {e}")
                    continue

            if not id_entered:
                print("⚠️  아이디 입력란을 찾을 수 없습니다.")
                logging.warning("아이디 입력란을 찾을 수 없음")

            time.sleep(1)

            # 비밀번호 입력
            pw_input_selectors = [
                "//input[@name='pw']",
                "//input[@name='password']",
                "//input[@id='password']",
                "//input[@id='pw']",
                "//input[@type='password']",
                "//input[@placeholder*='비밀번호']",
                "//input[@placeholder*='Password']",
                "//input[contains(@class, 'input_pw')]",
                "//input[contains(@class, 'tf_pw')]"
            ]

            pw_entered = False
            for selector in pw_input_selectors:
                try:
                    logging.info(f"비밀번호 입력 시도: {selector}")
                    pw_input = self.driver.find_element(By.XPATH, selector)
                    pw_input.clear()
                    pw_input.send_keys(self.config['password'])
                    print("✅ 비밀번호 입력 완료")
                    logging.info("비밀번호 입력 성공")
                    pw_entered = True
                    break
                except Exception as e:
                    logging.debug(f"비밀번호 입력 실패: {selector} - {e}")
                    continue

            if not pw_entered:
                print("⚠️  비밀번호 입력란을 찾을 수 없습니다.")
                logging.warning("비밀번호 입력란을 찾을 수 없음")

            time.sleep(1)

            # 로그인 버튼 클릭
            submit_selectors = [
                "//button[@type='submit']",
                "//button[contains(text(), '로그인')]",
                "//a[contains(text(), '로그인')]",
                "//input[@type='submit']",
                "//button[contains(@class, 'btn_login')]",
                "//a[contains(@class, 'btn_login')]",
                "//button[@id='loginBtn']",
                "//input[@value='로그인']"
            ]

            submit_clicked = False
            for selector in submit_selectors:
                try:
                    logging.info(f"로그인 버튼 클릭 시도: {selector}")
                    submit_btn = self.driver.find_element(By.XPATH, selector)
                    submit_btn.click()
                    print("✅ 로그인 버튼 클릭")
                    logging.info("로그인 버튼 클릭 성공")
                    submit_clicked = True
                    break
                except Exception as e:
                    logging.debug(f"로그인 버튼 클릭 실패: {selector} - {e}")
                    continue

            if not submit_clicked:
                print("⚠️  로그인 버튼을 찾을 수 없습니다. Enter 키를 시도합니다.")
                logging.warning("로그인 버튼을 찾을 수 없음, Enter 키 시도")
                try:
                    # Enter 키로 제출 시도
                    from selenium.webdriver.common.keys import Keys
                    pw_input = self.driver.find_element(By.XPATH, pw_input_selectors[0])
                    pw_input.send_keys(Keys.RETURN)
                    print("✅ Enter 키로 로그인 제출")
                    logging.info("Enter 키로 로그인 제출 성공")
                except Exception as e:
                    logging.error(f"Enter 키 제출 실패: {e}")

            # 로그인 완료 대기
            print("⏳ 로그인 처리 대기 중...")
            logging.info("로그인 처리 대기")
            time.sleep(5)

            # 메인 창으로 돌아가기 (팝업이었다면)
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[0])
                print("🏠 메인 창으로 복귀")
                logging.info("메인 창으로 복귀")

            print("✅ 로그인 완료")
            logging.info("로그인 프로세스 완료")

        except Exception as e:
            error_msg = f"❌ 로그인 실패: {e}"
            print(error_msg)
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            print("⚠️  수동으로 로그인해주세요. 30초 대기합니다...")
            time.sleep(30)

    def click_game_start(self):
        """게임 시작 버튼 클릭"""
        print("🎮 게임 시작 버튼 찾기...")
        logging.info("게임 시작 버튼 찾기 시작")

        try:
            # 페이지 로드 대기
            time.sleep(3)

            # 먼저 JavaScript로 "게임시작" 텍스트를 포함한 모든 요소 찾기
            print("🔍 페이지의 모든 요소 스캔 중...")
            logging.info("JavaScript로 게임시작 버튼 검색")

            # JavaScript로 모든 요소에서 "게임시작" 또는 "게임 시작" 텍스트 찾기
            script = """
            function findGameStartButton() {
                const keywords = ['게임시작', '게임 시작', 'PLAY', 'Play', 'play'];
                const allElements = document.querySelectorAll('*');

                for (let element of allElements) {
                    const text = element.textContent || element.innerText || '';
                    const trimmedText = text.trim();

                    // 텍스트가 키워드와 정확히 일치하거나 포함하는지 확인
                    for (let keyword of keywords) {
                        if (trimmedText === keyword ||
                            (trimmedText.length < 20 && trimmedText.includes(keyword))) {
                            // 클릭 가능한 요소인지 확인 (a, button, div with onclick 등)
                            if (element.tagName === 'A' ||
                                element.tagName === 'BUTTON' ||
                                element.onclick ||
                                element.getAttribute('onclick') ||
                                window.getComputedStyle(element).cursor === 'pointer') {
                                return element;
                            }
                        }
                    }
                }
                return null;
            }
            return findGameStartButton();
            """

            game_start_element = self.driver.execute_script(script)

            if game_start_element:
                print("✅ JavaScript로 게임 시작 버튼 발견")
                logging.info("JavaScript로 게임 시작 버튼 찾기 성공")
                # JavaScript로 직접 클릭
                self.driver.execute_script("arguments[0].click();", game_start_element)
                print("✅ 게임 시작 버튼 클릭 완료")
                logging.info("게임 시작 버튼 클릭 성공")
                game_started = True
            else:
                # JavaScript로 못 찾으면 기존 선택자들 시도
                print("🔄 XPath 선택자로 재시도...")
                logging.info("XPath 선택자로 버튼 찾기 시도")

                # 게임 시작 버튼 찾기 (여러 가능한 선택자 시도)
                game_start_selectors = [
                    # href="javascript:void(0);" 를 가진 링크
                    "//a[@href='javascript:void(0);' and contains(text(), '게임시작')]",
                    "//a[@href='javascript:void(0);' and contains(text(), '게임 시작')]",
                    "//a[@href='javascript:void(0);']//text()[contains(., '게임시작')]/..",
                    "//a[contains(@href, 'javascript:') and contains(text(), '게임시작')]",
                    "//a[contains(@href, 'void') and contains(text(), '게임시작')]",

                    # CSS 클래스나 ID로 찾기
                    "//a[contains(@class, 'game') and contains(@class, 'start')]",
                    "//a[contains(@id, 'game') and contains(@id, 'start')]",
                    "//button[contains(@class, 'game') and contains(@class, 'start')]",

                    # 텍스트로 찾기 (대소문자 구분 없이)
                    "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '게임시작')]",

                    # 기본 선택자들
                    "//button[contains(text(), '게임시작')]",
                    "//a[contains(text(), '게임시작')]",
                    "//button[contains(text(), '게임 시작')]",
                    "//a[contains(text(), '게임 시작')]",
                    "//button[contains(@class, 'game-start')]",
                    "//a[contains(@class, 'game-start')]",
                    "//div[contains(text(), '게임시작')]",
                    "//span[contains(text(), '게임시작')]",
                    "//button[contains(text(), 'PLAY')]",
                    "//a[contains(text(), 'PLAY')]",
                    "//button[contains(text(), 'Play')]",
                    "//a[contains(text(), 'Play')]"
                ]

                game_started = False
                for selector in game_start_selectors:
                    try:
                        logging.info(f"선택자 시도: {selector}")
                        game_start_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        # JavaScript로 클릭 (일반 클릭이 안 될 수 있으므로)
                        self.driver.execute_script("arguments[0].click();", game_start_btn)
                        print("✅ 게임 시작 버튼 클릭 완료")
                        logging.info(f"게임 시작 버튼 클릭 성공 - 선택자: {selector}")
                        game_started = True
                        break
                    except Exception as e:
                        logging.debug(f"선택자 실패: {selector} - {e}")
                        continue

                if not game_started:
                    print("⚠️  게임 시작 버튼을 찾을 수 없습니다.")
                    print("💡 화면 왼쪽의 게임 시작 버튼을 수동으로 클릭해주세요.")
                    logging.warning("게임 시작 버튼을 찾을 수 없음")

                    # 디버깅을 위해 페이지의 모든 링크 로그
                    try:
                        all_links = self.driver.find_elements(By.TAG_NAME, "a")
                        logging.info(f"페이지에서 찾은 총 링크 수: {len(all_links)}")
                        for i, link in enumerate(all_links[:10]):  # 처음 10개만
                            try:
                                text = link.text.strip()
                                href = link.get_attribute('href')
                                if text or 'void' in str(href):
                                    logging.info(f"링크 #{i+1}: 텍스트='{text}', href='{href}'")
                            except:
                                pass
                    except Exception as e:
                        logging.error(f"링크 디버깅 실패: {e}")

                    # 수동 클릭을 위해 더 오래 대기
                    print("⏳ 수동으로 클릭할 시간 - 30초 대기 중...")
                    time.sleep(30)
                    return

            # 로그인 창이 나타날 때까지 대기
            print("⏳ 로그인 창 로드 대기 중...")
            logging.info("로그인 창 로드 대기")
            time.sleep(3)

        except Exception as e:
            error_msg = f"❌ 게임 시작 버튼 클릭 실패: {e}"
            print(error_msg)
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            print("💡 화면 왼쪽의 게임 시작 버튼을 수동으로 클릭해주세요.")
            print("⏳ 수동으로 클릭할 시간 - 30초 대기 중...")
            time.sleep(30)

    def run(self):
        """런처 실행"""
        try:
            print("=" * 50)
            print("🎯 POE2 Auto Login Launcher 시작")
            print(f"📝 로그 파일: {LOG_FILE}")
            print("=" * 50)
            logging.info("POE2 Launcher 시작")

            self.setup_driver()
            self.open_website()
            self.click_game_start()  # 먼저 게임 시작 버튼 클릭
            self.login()  # 그 다음 로그인 창에서 로그인

            print("\n" + "=" * 50)
            print("✨ 런처 작업 완료!")
            print("게임 런처가 실행될 때까지 브라우저를 유지합니다.")
            print("종료하려면 브라우저를 닫거나 Ctrl+C를 누르세요.")
            print("=" * 50)
            logging.info("런처 작업 완료")

            # 브라우저 유지 (사용자가 수동으로 닫을 때까지)
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n⏹️  사용자가 중단했습니다.")
            logging.info("사용자가 프로그램 중단")
        except Exception as e:
            error_msg = f"\n❌ 예기치 않은 오류: {e}"
            print(error_msg)
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            print(f"\n📝 자세한 로그는 다음 파일을 확인하세요: {LOG_FILE}")
            input("\n계속하려면 Enter를 누르세요...")
        finally:
            self.cleanup()

    def cleanup(self):
        """리소스 정리"""
        if self.driver:
            print("\n🧹 브라우저 종료 중...")
            try:
                self.driver.quit()
                print("✅ 정리 완료")
            except:
                pass


def main():
    """메인 함수"""
    try:
        print("\n" + "=" * 60)
        print("  POE2 Auto Login Launcher")
        print("  Path of Exile 2 다음 게임 자동 로그인 런처")
        print("=" * 60 + "\n")

        # 실행 파일과 같은 디렉토리에서 config.json 찾기
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 경우
            application_path = os.path.dirname(sys.executable)
        else:
            # 일반 Python 스크립트로 실행된 경우
            application_path = os.path.dirname(os.path.abspath(__file__))

        config_path = os.path.join(application_path, 'config.json')
        logging.info(f"실행 경로: {application_path}")
        logging.info(f"설정 파일 경로: {config_path}")

        launcher = POE2Launcher(config_path)
        launcher.run()

    except Exception as e:
        error_msg = f"프로그램 시작 실패: {e}"
        print(f"\n❌ {error_msg}")
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        print(f"\n📝 자세한 로그는 다음 파일을 확인하세요: {LOG_FILE}")
        input("\n계속하려면 Enter를 누르세요...")
        sys.exit(1)


if __name__ == "__main__":
    main()
