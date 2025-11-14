"""
AI Assistant 기능 테스트 스크립트

사용법:
    python test_ai_assistant.py
"""
import logging
from ai_assistant import AIAssistant, get_ai_assistant
from config import AIConfig, DIR_PRESET

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_ollama_availability():
    """Ollama 사용 가능 여부 테스트"""
    print("\n=== Ollama 사용 가능 여부 확인 ===")
    available = AIAssistant.is_ollama_available()
    print(f"Ollama 사용 가능: {available}")
    return available


def test_available_models():
    """설치된 모델 목록 확인"""
    print("\n=== 설치된 모델 목록 ===")
    models = AIAssistant.get_available_models()
    if models:
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
    else:
        print("설치된 모델이 없습니다.")
    return models


def test_model_exists():
    """기본 모델 존재 여부 확인"""
    print(f"\n=== 기본 모델({AIConfig.DEFAULT_MODEL}) 존재 여부 확인 ===")
    exists = AIAssistant.check_model_exists(AIConfig.DEFAULT_MODEL)
    print(f"모델 존재: {exists}")
    return exists


def test_ai_generation():
    """AI 생성 기능 테스트"""
    print("\n=== AI 생성 기능 테스트 ===")
    
    # 테스트용 버그 제목
    test_summaries = [
        "컨트랙트 탭 클릭 후 클라이언트 크래쉬 발생",
        "인벤토리에서 아이템명이 축약된 형태로 출력되는 현상",
        "하이드아웃 스폰 위치가 올바르지 않은 문제"
    ]
    
    # AI 어시스턴트 생성
    ai_assistant = get_ai_assistant(
        preset_dir=DIR_PRESET,
        model_name=AIConfig.DEFAULT_MODEL
    )
    
    print(f"\n로드된 예시 preset 개수: {len(ai_assistant.example_presets)}")
    
    # 각 테스트 케이스 실행
    for i, summary in enumerate(test_summaries, 1):
        print(f"\n--- 테스트 케이스 {i} ---")
        print(f"입력 (Summary): {summary}")
        
        try:
            result = ai_assistant.generate_bug_details(summary)
            
            if result:
                print("\n생성 성공!")
                print(f"Priority: {result['priority']}")
                print(f"Severity: {result['severity']}")
                print(f"Steps (일부):\n{result['steps'][:200]}...")
                print(f"Description (일부):\n{result['description'][:200]}...")
            else:
                print("생성 실패: AI가 유효한 응답을 반환하지 못했습니다.")
        except Exception as e:
            print(f"생성 실패: {e}")
        
        # 첫 번째 케이스만 테스트 (시간 절약)
        if i == 1:
            print("\n(나머지 테스트 케이스는 생략합니다)")
            break


def show_recommendations():
    """추천 모델 정보 출력"""
    print("\n=== 추천 모델 목록 ===")
    recommendations = AIAssistant.get_recommended_models()
    for model in recommendations:
        print(f"\n모델명: {model['name']}")
        print(f"  설명: {model['description']}")
        print(f"  크기: {model['size']}")


def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("AI Assistant 기능 테스트")
    print("=" * 60)
    
    # 1. Ollama 사용 가능 여부 확인
    if not test_ollama_availability():
        print("\n❌ Ollama가 설치되지 않았습니다.")
        print("\n설치 방법:")
        print("1. https://ollama.com/download 에서 Ollama 다운로드")
        print("2. pip install ollama")
        return
    
    # 2. 설치된 모델 목록 확인
    models = test_available_models()
    
    # 3. 기본 모델 존재 여부 확인
    model_exists = test_model_exists()
    
    if not model_exists:
        print(f"\n❌ 기본 모델({AIConfig.DEFAULT_MODEL})이 설치되지 않았습니다.")
        print(f"\n모델 설치 명령어:")
        print(f"ollama pull {AIConfig.DEFAULT_MODEL}")
        
        # 추천 모델 정보 출력
        show_recommendations()
        
        if not models:
            print("\n다른 모델도 설치되지 않았으므로 테스트를 종료합니다.")
            return
    
    # 4. AI 생성 기능 테스트
    try:
        test_ai_generation()
    except Exception as e:
        print(f"\n❌ AI 생성 테스트 실패: {e}")
        logger.error("AI 생성 테스트 실패", exc_info=True)
    
    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

