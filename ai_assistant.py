"""
AI 어시스턴트 모듈
로컬 LLM을 사용하여 버그 리포트 내용을 자동 생성합니다.
"""
import json
import logging
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("ollama 패키지가 설치되지 않았습니다. AI 기능을 사용하려면 'pip install ollama'를 실행하세요.")


class AIAssistant:
    """로컬 LLM을 사용한 AI 어시스턴트"""
    
    DEFAULT_MODEL = "gemma2:2b"  # 가벼운 모델 (RAM 4GB, 빠름) - 추천: qwen2.5:1.5b (더 빠름)
    
    def __init__(self, model_name: Optional[str] = None, preset_dir: Optional[str] = None):
        """
        AI 어시스턴트 초기화
        
        Args:
            model_name: 사용할 모델 이름 (기본값: gemma2:2b)
            preset_dir: preset 파일들이 있는 디렉토리 경로
        """
        self.model_name = model_name or self.DEFAULT_MODEL
        self.preset_dir = preset_dir
        self.example_presets = []
        
        if not OLLAMA_AVAILABLE:
            logger.error("Ollama가 설치되지 않았습니다.")
            return
        
        # preset 디렉토리에서 예시 데이터 로드
        if self.preset_dir:
            self._load_example_presets()
    
    def _load_example_presets(self, max_examples: int = 2):
        """
        preset 파일들에서 예시 데이터를 로드
        
        Args:
            max_examples: 로드할 최대 예시 개수
        """
        if not self.preset_dir or not os.path.exists(self.preset_dir):
            logger.warning(f"preset 디렉토리를 찾을 수 없습니다: {self.preset_dir}")
            return
        
        try:
            preset_files = list(Path(self.preset_dir).glob('*.json'))[:max_examples]
            
            for preset_file in preset_files:
                try:
                    with open(preset_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # 필요한 필드만 추출
                        example = {
                            'summary': data.get('summary', ''),
                            'priority': data.get('priority', ''),
                            'severity': data.get('severity', ''),
                            'steps': data.get('steps', ''),
                            'description': data.get('description', ''),
                            'label': data.get('label', '')
                        }
                        if example['summary']:  # summary가 있는 경우만 추가
                            self.example_presets.append(example)
                except Exception as e:
                    logger.warning(f"preset 파일 로드 실패 ({preset_file.name}): {e}")
                    
            logger.info(f"{len(self.example_presets)}개의 예시 preset을 로드했습니다.")
        except Exception as e:
            logger.error(f"preset 디렉토리 읽기 실패: {e}")
    
    def _build_prompt(self, summary: str) -> str:
        """
        프롬프트를 생성
        
        Args:
            summary: 버그 요약 (제목)
            
        Returns:
            생성된 프롬프트
        """
        # 예시 데이터는 프롬프트 길이 때문에 제외 (속도 향상)
        
        prompt = f"""게임 QA 전문가로서 JIRA 버그 리포트를 작성합니다.

버그 제목: {summary}

다음 JSON 형식으로 작성:

{{
  "priority": "Critical|High|Medium|Low",
  "severity": "1 - Critical|2 - Major|3 - Minor",
  "steps": "1. 하이드아웃 접속\\n2. [행동]\\n3. [결과 확인]",
  "description": "*Observed(관찰 결과):*\\n\\n* 한글 설명\\n{{{{color:#4c9aff}}}}영문 설명{{{{color}}}}\\n\\n*Video(영상):*\\n\\n* !video.mp4|width=2560,height=1440,alt=\\"video.mp4\\"!\\n\\n\\n*Expected (기대 결과):*\\n\\n* 한글 설명\\n{{{{color:#4c9aff}}}}영문 설명{{{{color}}}}\\n\\n*Note(참고):*\\n\\n* 환경 정보 / {{{{color:#4c9aff}}}}Environment{{{{color}}}}\\n** 빌드/{{{{color:#4c9aff}}}}Build{{{{color}}}}: [빌드명]\\n** 백엔드/{{{{color:#4c9aff}}}}Backend{{{{color}}}}: [버전]\\n** Chart Version [버전]\\n** [환경링크]\\n\\n* 재현 조건\\n{{{{color:#4c9aff}}}}Reproduction conditions{{{{color}}}}"
}}

규칙:
- priority: 크래시=Critical, 주요기능불가=High, 일반=Medium, 사소=Low
- severity: 크래시/손실=1, 오작동=2, 사소=3
- steps: 1부터 시작하는 번호 목록
- description: 위 형식 정확히 따르기, 한글+영문 병기

JSON만 출력하세요:"""
        
        return prompt
    
    def generate_bug_details(self, summary: str) -> Optional[Dict[str, str]]:
        """
        버그 제목을 바탕으로 세부 정보를 생성
        
        Args:
            summary: 버그 요약 (제목)
            
        Returns:
            생성된 버그 정보 딕셔너리 또는 None (실패 시)
            {
                'priority': str,
                'severity': str,
                'steps': str,
                'description': str
            }
        """
        if not OLLAMA_AVAILABLE:
            logger.error("Ollama가 설치되지 않았습니다.")
            return None
        
        if not summary or not summary.strip():
            logger.warning("버그 제목이 비어있습니다.")
            return None
        
        try:
            # 프롬프트 생성
            prompt = self._build_prompt(summary)
            
            logger.info(f"AI 생성 시작 - 모델: {self.model_name}, 제목: {summary[:50]}...")
            
            # Ollama API 호출 (속도 최적화)
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.3,  # 낮춰서 더 빠르고 일관적으로
                    'top_p': 0.9,
                    'top_k': 40,
                    'num_predict': 1024,  # 최대 토큰 수 제한 (속도 향상)
                    'num_ctx': 2048,  # 컨텍스트 크기 제한 (메모리/속도 향상)
                }
            )
            
            # 응답에서 텍스트 추출
            generated_text = response.get('response', '').strip()
            
            if not generated_text:
                logger.error("AI가 빈 응답을 반환했습니다.")
                return None
            
            # 응답 전체를 로그에 저장 (디버깅용)
            logger.debug(f"AI 응답 (처음 500자): {generated_text[:500]}")
            logger.debug(f"AI 응답 길이: {len(generated_text)} 문자")
            
            # 응답을 파일로 저장 (디버깅용)
            try:
                with open('last_ai_response.txt', 'w', encoding='utf-8') as f:
                    f.write(generated_text)
                logger.debug("AI 응답을 'last_ai_response.txt'에 저장했습니다.")
            except:
                pass
            
            # JSON 파싱
            result = self._parse_response(generated_text)
            
            if result:
                logger.info("AI 생성 완료")
                return result
            else:
                logger.error("AI 응답 파싱 실패")
                logger.error(f"파싱 실패한 응답 (전체): {generated_text}")
                return None
                
        except Exception as e:
            logger.error(f"AI 생성 중 오류 발생: {e}", exc_info=True)
            return None
    
    def _parse_response(self, response_text: str) -> Optional[Dict[str, str]]:
        """
        AI 응답을 파싱
        
        Args:
            response_text: AI가 생성한 텍스트
            
        Returns:
            파싱된 딕셔너리 또는 None
        """
        try:
            # JSON 블록 찾기 (```json ... ``` 또는 { ... })
            json_text = response_text
            
            # 코드 블록 제거
            if '```json' in json_text:
                json_text = json_text.split('```json')[1].split('```')[0]
            elif '```' in json_text:
                json_text = json_text.split('```')[1].split('```')[0]
            
            # JSON 텍스트 정리 (제어 문자 처리)
            json_text = json_text.strip()
            
            # JSON 파싱 시도 (strict=False로 제어 문자 허용)
            try:
                data = json.loads(json_text, strict=False)
            except json.JSONDecodeError:
                # strict=False로도 실패하면 제어 문자를 이스케이프 처리
                logger.warning("JSON 파싱 실패, 제어 문자 정리 시도 중...")
                
                # 제어 문자를 이스케이프 처리
                import re
                # 줄바꿈 문자를 \\n으로 변환 (JSON 문자열 내부의 줄바꿈)
                json_text_cleaned = json_text.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                
                # 다시 원래대로 복구 (JSON 구조상 필요한 줄바꿈)
                # JSON 키-값 사이의 줄바꿈은 유지
                json_text_cleaned = re.sub(r'\\n(?=\s*["}])', '\n', json_text_cleaned)
                json_text_cleaned = re.sub(r'(?<=[{,])\s*\\n\s*', '\n', json_text_cleaned)
                
                try:
                    data = json.loads(json_text_cleaned, strict=False)
                except json.JSONDecodeError:
                    # 최후의 수단: 정규식으로 필드 추출
                    logger.warning("JSON 파싱 실패, 정규식으로 필드 추출 시도 중...")
                    return self._extract_fields_with_regex(response_text)
            
            # 필수 필드 확인
            required_fields = ['priority', 'severity', 'steps', 'description']
            if not all(field in data for field in required_fields):
                logger.error(f"필수 필드 누락: {required_fields}, 받은 필드: {list(data.keys())}")
                # 정규식으로 재시도
                return self._extract_fields_with_regex(response_text)
            
            return {
                'priority': str(data['priority']),
                'severity': str(data['severity']),
                'steps': str(data['steps']),
                'description': str(data['description'])
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류: {e}")
            logger.debug(f"파싱 실패한 텍스트 (처음 500자): {response_text[:500]}")
            # 정규식으로 재시도
            return self._extract_fields_with_regex(response_text)
        except Exception as e:
            logger.error(f"응답 파싱 중 오류: {e}", exc_info=True)
            return None
    
    def _extract_fields_with_regex(self, response_text: str) -> Optional[Dict[str, str]]:
        """
        정규식을 사용하여 응답에서 필드를 추출 (JSON 파싱 실패 시 백업)
        
        Args:
            response_text: AI 응답 텍스트
            
        Returns:
            추출된 필드 딕셔너리 또는 None
        """
        try:
            import re
            
            result = {}
            
            # Priority 추출
            priority_match = re.search(r'"priority"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
            if priority_match:
                result['priority'] = priority_match.group(1)
            
            # Severity 추출
            severity_match = re.search(r'"severity"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
            if severity_match:
                result['severity'] = severity_match.group(1)
            
            # Steps 추출 (여러 줄 가능)
            steps_match = re.search(r'"steps"\s*:\s*"((?:[^"\\]|\\.)*)"', response_text, re.IGNORECASE | re.DOTALL)
            if steps_match:
                result['steps'] = steps_match.group(1).replace('\\n', '\n').replace('\\"', '"')
            
            # Description 추출 (여러 줄 가능)
            desc_match = re.search(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"', response_text, re.IGNORECASE | re.DOTALL)
            if desc_match:
                result['description'] = desc_match.group(1).replace('\\n', '\n').replace('\\"', '"')
            
            # 필수 필드 확인
            required_fields = ['priority', 'severity', 'steps', 'description']
            if all(field in result for field in required_fields):
                logger.info("정규식을 사용한 필드 추출 성공")
                return result
            else:
                logger.error(f"정규식 추출 실패: 추출된 필드 {list(result.keys())}")
                return None
                
        except Exception as e:
            logger.error(f"정규식 추출 중 오류: {e}", exc_info=True)
            return None
    
    @staticmethod
    def is_ollama_available() -> bool:
        """Ollama가 사용 가능한지 확인"""
        return OLLAMA_AVAILABLE
    
    @staticmethod
    def check_model_exists(model_name: str) -> bool:
        """
        모델이 로컬에 설치되어 있는지 확인
        
        Args:
            model_name: 확인할 모델 이름
            
        Returns:
            설치 여부
        """
        if not OLLAMA_AVAILABLE:
            return False
        
        try:
            models = ollama.list()
            model_list = models.get('models', [])
            
            if not model_list:
                logger.warning("설치된 모델이 없습니다.")
                return False
            
            # 모델 이름 추출 (ollama 패키지 버전에 따라 다름)
            model_names = []
            for model in model_list:
                if hasattr(model, 'model'):
                    model_names.append(model.model)
                elif isinstance(model, dict) and 'model' in model:
                    model_names.append(model['model'])
                elif isinstance(model, dict) and 'name' in model:
                    model_names.append(model['name'])
            
            logger.debug(f"설치된 모델 목록: {model_names}")
            
            # 모델 이름 매칭 (정확한 이름 또는 태그 포함)
            # gemma2:2b는 "gemma2:2b"로 저장될 수도 있고 "gemma2:2b-latest" 등으로 저장될 수도 있음
            for installed_model in model_names:
                # 정확히 일치하거나, 시작 부분이 일치하는 경우
                if installed_model == model_name or installed_model.startswith(f"{model_name}:") or installed_model.startswith(model_name.split(':')[0] + ':'):
                    logger.info(f"모델 발견: {installed_model} (요청: {model_name})")
                    return True
            
            logger.warning(f"모델 '{model_name}'을(를) 찾을 수 없습니다. 설치된 모델: {model_names}")
            return False
            
        except ConnectionError as e:
            logger.error(f"Ollama 서비스에 연결할 수 없습니다: {e}")
            logger.error("Ollama 데스크톱 애플리케이션이 실행 중인지 확인해주세요.")
            return False
        except Exception as e:
            logger.error(f"모델 확인 중 오류: {e}", exc_info=True)
            return False
    
    @staticmethod
    def get_available_models() -> List[str]:
        """
        로컬에 설치된 모델 목록 가져오기
        
        Returns:
            모델 이름 리스트
        """
        if not OLLAMA_AVAILABLE:
            return []
        
        try:
            models = ollama.list()
            model_list = models.get('models', [])
            
            # 모델 이름 추출 (ollama 패키지 버전에 따라 다름)
            model_names = []
            for model in model_list:
                if hasattr(model, 'model'):
                    model_names.append(model.model)
                elif isinstance(model, dict) and 'model' in model:
                    model_names.append(model['model'])
                elif isinstance(model, dict) and 'name' in model:
                    model_names.append(model['name'])
            
            logger.info(f"설치된 모델 {len(model_names)}개: {model_names}")
            return model_names
        except ConnectionError as e:
            logger.error(f"Ollama 서비스에 연결할 수 없습니다: {e}")
            return []
        except Exception as e:
            logger.error(f"모델 목록 조회 중 오류: {e}", exc_info=True)
            return []
    
    @staticmethod
    def get_recommended_models() -> List[Dict[str, str]]:
        """
        추천 모델 목록 반환
        
        Returns:
            추천 모델 정보 리스트
        """
        return [
            {
                'name': 'qwen2.5:1.5b',
                'description': '매우 빠른 초경량 모델 (RAM ~2GB) ⚡ 추천',
                'size': '~1GB'
            },
            {
                'name': 'gemma2:2b',
                'description': '가벼운 모델 (RAM ~4GB, 빠름)',
                'size': '~1.6GB'
            },
            {
                'name': 'llama3.2:3b',
                'description': '균형잡힌 모델 (RAM ~6GB)',
                'size': '~2GB'
            },
            {
                'name': 'qwen2.5:3b',
                'description': '다국어 지원 좋은 모델 (RAM ~6GB)',
                'size': '~2GB'
            },
            {
                'name': 'llama3.1:8b',
                'description': '고성능 모델 (RAM ~10GB, 느림)',
                'size': '~4.7GB'
            }
        ]


# 전역 인스턴스 (싱글톤 패턴)
_ai_assistant_instance: Optional[AIAssistant] = None


def get_ai_assistant(preset_dir: Optional[str] = None, model_name: Optional[str] = None) -> AIAssistant:
    """
    AI 어시스턴트 싱글톤 인스턴스를 반환
    
    Args:
        preset_dir: preset 디렉토리 경로 (최초 호출 시에만 사용)
        model_name: 모델 이름 (최초 호출 시에만 사용)
        
    Returns:
        AIAssistant 인스턴스
    """
    global _ai_assistant_instance
    
    if _ai_assistant_instance is None:
        _ai_assistant_instance = AIAssistant(
            model_name=model_name,
            preset_dir=preset_dir
        )
    
    return _ai_assistant_instance

