#!/usr/bin/env python3
"""
GitHub 저장소 설정 자동화 스크립트
"""

import subprocess
import sys
import os
import getpass

def run_command(command, check=True):
    """명령어를 실행하고 결과를 반환합니다."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"오류 발생: {result.stderr}")
            return False
        return result
    except Exception as e:
        print(f"명령어 실행 오류: {e}")
        return False

def setup_github():
    """GitHub 저장소 설정을 자동화합니다."""
    
    print("=" * 60)
    print("GitHub 저장소 설정 자동화")
    print("=" * 60)
    print()
    
    # 1. 현재 Git 상태 확인
    print("1. Git 상태 확인...")
    result = run_command("git status")
    if not result:
        print("Git 저장소가 초기화되지 않았습니다.")
        return False
    
    print("✓ Git 저장소가 정상적으로 초기화되어 있습니다.")
    print()
    
    # 2. 사용자 정보 입력
    print("2. GitHub 정보 입력")
    print("-" * 40)
    
    username = input("GitHub 사용자명을 입력하세요: ").strip()
    if not username:
        print("사용자명이 필요합니다.")
        return False
    
    repo_name = input("저장소 이름을 입력하세요 (기본값: news-sentiment-analysis): ").strip()
    if not repo_name:
        repo_name = "news-sentiment-analysis"
    
    description = input("저장소 설명을 입력하세요 (기본값: 뉴스 수집 및 감정 분석 시스템): ").strip()
    if not description:
        description = "뉴스 수집 및 감정 분석 시스템"
    
    is_public = input("공개 저장소로 만들겠습니까? (y/n, 기본값: y): ").strip().lower()
    if is_public == "" or is_public == "y":
        visibility = "public"
    else:
        visibility = "private"
    
    print()
    
    # 3. GitHub CLI 설치 확인
    print("3. GitHub CLI 확인...")
    gh_result = run_command("gh --version", check=False)
    if gh_result and gh_result.returncode == 0:
        print("✓ GitHub CLI가 설치되어 있습니다.")
        use_gh_cli = True
    else:
        print("⚠ GitHub CLI가 설치되어 있지 않습니다.")
        print("수동으로 GitHub 저장소를 생성해야 합니다.")
        use_gh_cli = False
    
    print()
    
    if use_gh_cli:
        # 4. GitHub CLI로 저장소 생성
        print("4. GitHub 저장소 생성...")
        gh_command = f'gh repo create {repo_name} --{visibility} --description "{description}" --source=. --remote=origin --push'
        result = run_command(gh_command)
        if result:
            print("✓ GitHub 저장소가 성공적으로 생성되었습니다!")
            print(f"저장소 URL: https://github.com/{username}/{repo_name}")
        else:
            print("✗ GitHub 저장소 생성에 실패했습니다.")
            print("수동으로 생성해주세요.")
            return False
    else:
        # 5. 수동 설정 안내
        print("4. 수동 설정 안내")
        print("-" * 40)
        print("다음 단계를 따라 GitHub 저장소를 생성하세요:")
        print()
        print("1. https://github.com 에 접속")
        print("2. 로그인 후 우측 상단 '+' 버튼 클릭")
        print("3. 'New repository' 선택")
        print(f"4. Repository name: {repo_name}")
        print(f"5. Description: {description}")
        print(f"6. Visibility: {visibility}")
        print("7. 'Create repository' 클릭")
        print()
        print("저장소 생성 후 다음 명령어를 실행하세요:")
        print(f"git remote add origin https://github.com/{username}/{repo_name}.git")
        print("git branch -M main")
        print("git push -u origin main")
        print()
        
        # 사용자가 수동으로 설정할 수 있도록 대기
        input("GitHub 저장소를 생성한 후 Enter를 눌러 계속하세요...")
        
        # 원격 저장소 추가
        print("5. 원격 저장소 연결...")
        remote_command = f"git remote add origin https://github.com/{username}/{repo_name}.git"
        result = run_command(remote_command)
        if not result:
            print("✗ 원격 저장소 연결에 실패했습니다.")
            return False
        
        # 브랜치 이름 변경
        branch_command = "git branch -M main"
        result = run_command(branch_command)
        if not result:
            print("✗ 브랜치 이름 변경에 실패했습니다.")
            return False
        
        # GitHub에 푸시
        print("6. GitHub에 푸시...")
        push_command = "git push -u origin main"
        result = run_command(push_command)
        if not result:
            print("✗ GitHub 푸시에 실패했습니다.")
            return False
    
    print()
    print("=" * 60)
    print("🎉 GitHub 저장소 설정이 완료되었습니다!")
    print("=" * 60)
    print()
    print(f"📁 저장소 URL: https://github.com/{username}/{repo_name}")
    print("📖 README: 프로젝트 설명서가 자동으로 표시됩니다")
    print("🔧 Issues: 버그 리포트나 기능 요청을 할 수 있습니다")
    print("📊 Actions: CI/CD 파이프라인을 설정할 수 있습니다")
    print()
    print("다음 단계:")
    print("1. GitHub에서 저장소 확인")
    print("2. README.md 파일 확인")
    print("3. 필요한 경우 추가 설정")
    print()
    
    return True

def main():
    """메인 함수"""
    try:
        success = setup_github()
        if success:
            print("✅ 모든 설정이 완료되었습니다!")
        else:
            print("❌ 설정 중 오류가 발생했습니다.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
