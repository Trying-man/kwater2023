#!/usr/bin/env python3
"""
서버 테스트 스크립트
"""

import requests
import time
import sys

def test_server():
    """서버가 정상적으로 작동하는지 테스트합니다."""
    
    base_url = "http://localhost:8000"
    
    print("서버 테스트를 시작합니다...")
    print(f"서버 주소: {base_url}")
    print()
    
    # 1. 기본 엔드포인트 테스트
    print("1. 기본 엔드포인트 테스트...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✓ 기본 엔드포인트 정상 작동")
            print(f"  응답: {response.json()}")
        else:
            print(f"✗ 기본 엔드포인트 오류: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return False
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        return False
    
    print()
    
    # 2. 감정분석 상태 확인
    print("2. 감정분석 모델 상태 확인...")
    try:
        response = requests.get(f"{base_url}/sentiment/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("✓ 감정분석 상태 확인 완료")
            print(f"  모델 사용 가능: {status.get('available', False)}")
            print(f"  모델 이름: {status.get('model_name', 'N/A')}")
        else:
            print(f"✗ 감정분석 상태 확인 실패: {response.status_code}")
    except Exception as e:
        print(f"✗ 감정분석 상태 확인 오류: {e}")
    
    print()
    
    # 3. 뉴스 조회 테스트
    print("3. 뉴스 조회 테스트...")
    try:
        response = requests.get(f"{base_url}/news/kwater", params={"max_results": 5}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✓ 뉴스 조회 정상 작동")
            print(f"  조회된 기사 수: {data.get('count', 0)}")
        else:
            print(f"✗ 뉴스 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"✗ 뉴스 조회 오류: {e}")
    
    print()
    
    # 4. 감정분석 포함 뉴스 조회 테스트
    print("4. 감정분석 포함 뉴스 조회 테스트...")
    try:
        response = requests.get(f"{base_url}/news/kwater/with-sentiment", params={"max_results": 3}, timeout=60)
        if response.status_code == 200:
            data = response.json()
            print("✓ 감정분석 포함 뉴스 조회 정상 작동")
            print(f"  조회된 기사 수: {data.get('count', 0)}")
            
            # 감정분석 결과 확인
            articles = data.get('articles', [])
            if articles:
                print("  감정분석 결과:")
                for i, article in enumerate(articles[:3], 1):
                    sentiment = article.get('sentiment', 'Unknown')
                    title = article.get('title', 'No title')[:50] + "..."
                    print(f"    {i}. {sentiment}: {title}")
        else:
            print(f"✗ 감정분석 포함 뉴스 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"✗ 감정분석 포함 뉴스 조회 오류: {e}")
    
    print()
    print("테스트 완료!")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("뉴스 수집 및 감정 분석 시스템 서버 테스트")
    print("=" * 50)
    print()
    
    success = test_server()
    
    if success:
        print()
        print("✓ 모든 테스트가 성공적으로 완료되었습니다!")
        print("서버가 정상적으로 작동하고 있습니다.")
    else:
        print()
        print("✗ 일부 테스트가 실패했습니다.")
        print("서버 상태를 확인해주세요.")
    
    print()
    print("API 문서: http://localhost:8000/docs")
    print("서버 주소: http://localhost:8000") 