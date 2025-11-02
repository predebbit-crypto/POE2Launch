"""
POE2 Launcher 계정 설정 도구
간단하게 계정 정보를 입력하고 config.json 파일을 생성합니다.
"""

import json
import os
import sys
import getpass


def clear_screen():
    """화면 클리어"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """배너 출력"""
    print("=" * 60)
    print("  POE2 Auto Login Launcher - 계정 설정")
    print("=" * 60)
    print()


def get_config_path():
    """config.json 경로 확인"""
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        application_path = os.path.dirname(sys.executable)
    else:
        # 일반 Python 스크립트로 실행된 경우
        application_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(application_path, 'config.json')


def load_existing_config(config_path):
    """기존 설정 파일 로드"""
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None


def main():
    clear_screen()
    print_banner()

    config_path = get_config_path()
    existing_config = load_existing_config(config_path)

    if existing_config:
        print("⚠️  기존 설정 파일이 발견되었습니다.")
        print(f"   현재 아이디: {existing_config.get('username', '없음')}")
        print()
        response = input("기존 설정을 덮어쓰시겠습니까? (y/n): ").strip().lower()
        if response != 'y':
            print("\n취소되었습니다.")
            input("\n계속하려면 Enter를 누르세요...")
            return
        print()

    print("📝 다음 계정 정보를 입력해주세요.")
    print("   (Path of Exile 2에 로그인할 때 사용하는 다음 계정)")
    print()

    # 아이디 입력
    username = input("다음 아이디: ").strip()
    if not username:
        print("\n❌ 아이디를 입력하지 않았습니다.")
        input("\n계속하려면 Enter를 누르세요...")
        return

    # 비밀번호 입력
    print("\n비밀번호를 입력하세요 (입력한 내용은 화면에 표시되지 않습니다)")
    password = getpass.getpass("비밀번호: ")
    if not password:
        print("\n❌ 비밀번호를 입력하지 않았습니다.")
        input("\n계속하려면 Enter를 누르세요...")
        return

    # 비밀번호 확인
    password_confirm = getpass.getpass("비밀번호 확인: ")
    if password != password_confirm:
        print("\n❌ 비밀번호가 일치하지 않습니다.")
        input("\n계속하려면 Enter를 누르세요...")
        return

    # 설정 저장
    config = {
        "username": username,
        "password": password
    }

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 60)
        print("✅ 설정이 저장되었습니다!")
        print("=" * 60)
        print(f"\n📁 설정 파일 위치: {config_path}")
        print(f"👤 저장된 아이디: {username}")
        print()
        print("⚠️  보안 주의사항:")
        print("   - config.json 파일에는 비밀번호가 평문으로 저장됩니다")
        print("   - 이 파일을 다른 사람과 공유하지 마세요")
        print("   - 공용 컴퓨터에서는 사용을 권장하지 않습니다")
        print()
        print("🚀 이제 POE2_Launcher를 실행할 수 있습니다!")

    except Exception as e:
        print(f"\n❌ 설정 저장 실패: {e}")

    input("\n계속하려면 Enter를 누르세요...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n취소되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        input("\n계속하려면 Enter를 누르세요...")
