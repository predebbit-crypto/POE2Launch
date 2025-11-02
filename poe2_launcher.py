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
            print("📥 Chrome WebDriver 다운로드 중... (처음 실행 시 시간이 걸릴 수 있습니다)")
            logging.info("ChromeDriverManager로 드라이버 설치 시도")
            service = Service(ChromeDriverManager().install())

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
            print("1. Chrome 브라우저가 설치되어 있는지 확인하세요")
            print("2. Chrome을 최신 버전으로 업데이트하세요")
            print("3. 인터넷 연결을 확인하세요 (WebDriver 다운로드 필요)")
            print("4. 백신 프로그램이 차단하고 있는지 확인하세요")
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
        """자동 로그인"""
        print("🔐 로그인 시도 중...")

        try:
            # 로그인 버튼 찾기 및 클릭 (다음 계정으로 로그인)
            # 실제 웹사이트 구조에 따라 선택자를 조정해야 할 수 있습니다

            # 로그인 버튼 클릭 (여러 가능한 선택자 시도)
            login_button_selectors = [
                "//a[contains(text(), '로그인')]",
                "//button[contains(text(), '로그인')]",
                "//a[contains(@class, 'login')]",
                "//button[contains(@class, 'login')]",
                "//a[@href*='login']"
            ]

            login_clicked = False
            for selector in login_button_selectors:
                try:
                    login_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    login_btn.click()
                    print("✅ 로그인 버튼 클릭")
                    login_clicked = True
                    break
                except:
                    continue

            if not login_clicked:
                print("⚠️  로그인 버튼을 찾을 수 없습니다. 이미 로그인되어 있을 수 있습니다.")
            else:
                time.sleep(2)

                # 다음 로그인 페이지로 이동했을 경우
                # ID 입력
                id_input_selectors = [
                    "//input[@name='id']",
                    "//input[@id='id']",
                    "//input[@type='text']",
                    "//input[@placeholder*='아이디']"
                ]

                for selector in id_input_selectors:
                    try:
                        id_input = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        id_input.clear()
                        id_input.send_keys(self.config['username'])
                        print("✅ 아이디 입력 완료")
                        break
                    except:
                        continue

                # 비밀번호 입력
                pw_input_selectors = [
                    "//input[@name='pw']",
                    "//input[@name='password']",
                    "//input[@type='password']",
                    "//input[@placeholder*='비밀번호']"
                ]

                for selector in pw_input_selectors:
                    try:
                        pw_input = self.driver.find_element(By.XPATH, selector)
                        pw_input.clear()
                        pw_input.send_keys(self.config['password'])
                        print("✅ 비밀번호 입력 완료")
                        break
                    except:
                        continue

                # 로그인 버튼 클릭
                submit_selectors = [
                    "//button[@type='submit']",
                    "//button[contains(text(), '로그인')]",
                    "//a[contains(text(), '로그인')]",
                    "//input[@type='submit']"
                ]

                for selector in submit_selectors:
                    try:
                        submit_btn = self.driver.find_element(By.XPATH, selector)
                        submit_btn.click()
                        print("✅ 로그인 제출")
                        break
                    except:
                        continue

                # 로그인 완료 대기
                time.sleep(5)

            print("✅ 로그인 완료")

        except Exception as e:
            print(f"❌ 로그인 실패: {e}")
            print("⚠️  수동으로 로그인해주세요. 30초 대기합니다...")
            time.sleep(30)

    def click_game_start(self):
        """게임 시작 버튼 클릭"""
        print("🎮 게임 시작 버튼 찾기...")

        try:
            # 게임 시작 버튼 찾기 (여러 가능한 선택자 시도)
            game_start_selectors = [
                "//button[contains(text(), '게임시작')]",
                "//a[contains(text(), '게임시작')]",
                "//button[contains(@class, 'game-start')]",
                "//a[contains(@class, 'game-start')]",
                "//div[contains(text(), '게임시작')]",
                "//button[contains(text(), 'PLAY')]",
                "//a[contains(text(), 'PLAY')]"
            ]

            game_started = False
            for selector in game_start_selectors:
                try:
                    game_start_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    game_start_btn.click()
                    print("✅ 게임 시작 버튼 클릭 완료")
                    game_started = True
                    break
                except:
                    continue

            if not game_started:
                print("⚠️  게임 시작 버튼을 찾을 수 없습니다.")
                print("💡 화면 왼쪽의 게임 시작 버튼을 수동으로 클릭해주세요.")

            # 게임 런처 실행 대기
            time.sleep(5)

        except Exception as e:
            print(f"❌ 게임 시작 버튼 클릭 실패: {e}")
            print("💡 화면 왼쪽의 게임 시작 버튼을 수동으로 클릭해주세요.")

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
            self.login()
            self.click_game_start()

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
