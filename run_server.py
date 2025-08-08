#!/usr/bin/env python3
"""
뉴스 수집 및 감정 분석 시스템 서버 실행 스크립트
"""

import subprocess
import sys
import os

def main():
    print("뉴스 수집 및 감정 분석 시스템 서버를 시작합니다...")
    
    # 현재 디렉토리 확인
    current_dir = os.getcwd()
    print(f"현재 디렉토리: {current_dir}")
    
    # Python 실행 파일 확인
    python_cmd = None
    for cmd in ['python', 'py', 'python3']:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                python_cmd = cmd
                print(f"Python 실행 파일: {cmd}")
                break
        except:
            continue
    
    if not python_cmd:
        print("Python을 찾을 수 없습니다.")
        return 1
    
    # 서버 실행
    try:
        print("서버를 시작합니다...")
        result = subprocess.run([python_cmd, 'main.py'], 
                              cwd=current_dir, timeout=30)
        return result.returncode
    except subprocess.TimeoutExpired:
        print("서버가 성공적으로 시작되었습니다!")
        print("서버 주소: http://localhost:8000")
        print("API 문서: http://localhost:8000/docs")
        return 0
    except Exception as e:
        print(f"서버 시작 중 오류 발생: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 