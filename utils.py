"""
공통 유틸리티 함수들을 모아둔 모듈
"""
import os
import json
from datetime import datetime
from typing import Optional, Any, Dict
import logging

from config import TEXT_REPLACEMENT_RULES

logger = logging.getLogger(__name__)


class FileManager:
    """파일 관리 관련 유틸리티 클래스"""
    
    @staticmethod
    def create_text_file(filename: str, content: str) -> None:
        """텍스트 파일을 생성"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"파일 '{filename}' 생성 완료")
        except Exception as e:
            logger.error(f"파일 '{filename}' 생성 실패: {e}")
            raise
    
    @staticmethod
    def load_text_file_all(filename: str) -> Optional[str]:
        """텍스트 파일 전체 내용을 로드"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"파일 '{filename}' 로드 완료")
            return content
        except FileNotFoundError:
            logger.warning(f"파일 '{filename}' 찾을 수 없음")
            return None
        except Exception as e:
            logger.error(f"파일 '{filename}' 로드 실패: {e}")
            return None
    
    @staticmethod
    def load_text_file_lines(filename: str) -> Optional[list]:
        """텍스트 파일을 줄별로 로드"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.readlines()
            logger.info(f"파일 '{filename}' 줄별 로드 완료")
            return content
        except FileNotFoundError:
            logger.warning(f"파일 '{filename}' 찾을 수 없음")
            return None
        except Exception as e:
            logger.error(f"파일 '{filename}' 로드 실패: {e}")
            return None
    
    @staticmethod
    def save_json(data: Dict[str, Any], filename: str) -> None:
        """JSON 데이터를 파일에 저장"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            logger.info(f"JSON 파일 '{filename}' 저장 완료")
        except Exception as e:
            logger.error(f"JSON 파일 '{filename}' 저장 실패: {e}")
            raise
    
    @staticmethod
    def load_json(filename: str) -> Optional[Dict[str, Any]]:
        """JSON 파일을 로드"""
        try:
            # 절대 경로로 변환해서 로그에 표시
            abs_path = os.path.abspath(filename)
            
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"JSON 파일 로드 완료: {abs_path}")
            return data
        except FileNotFoundError:
            abs_path = os.path.abspath(filename)
            logger.warning(f"JSON 파일 찾을 수 없음: {abs_path}")
            return None
        except json.JSONDecodeError as e:
            abs_path = os.path.abspath(filename)
            logger.error(f"JSON 파일 파싱 실패: {abs_path}, 오류: {e}")
            return None
        except Exception as e:
            abs_path = os.path.abspath(filename)
            logger.error(f"JSON 파일 로드 실패: {abs_path}, 오류: {e}")
            return None
    
    @staticmethod
    def get_most_recent_file(directory: str = '.') -> tuple:
        """가장 최근에 수정된 파일을 반환"""
        try:
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f)) and not f.endswith('.json')]
            
            if not files:
                return None, None
            
            most_recent_file = None
            most_recent_time = 0
            
            for file in files:
                file_path = os.path.join(directory, file)
                mod_time = os.path.getmtime(file_path)
                
                if mod_time > most_recent_time:
                    most_recent_time = mod_time
                    most_recent_file = file
            
            if most_recent_file:
                most_recent_time_readable = datetime.fromtimestamp(most_recent_time).strftime('%Y-%m-%d %H:%M:%S')
                return most_recent_file, most_recent_time_readable
            else:
                return None, None
                
        except Exception as e:
            logger.error(f"최근 파일 검색 실패: {e}")
            return None, None


class TextProcessor:
    """텍스트 처리 관련 유틸리티 클래스"""
    
    @staticmethod
    def apply_text_replacements(text: str) -> str:
        """텍스트에 대체 규칙을 적용"""
        result_text = text
        for old, new in TEXT_REPLACEMENT_RULES:
            result_text = result_text.replace(old, new)
        return result_text
    
    @staticmethod
    def generate_description_template(main_text: str, option: str, build_text: str = "") -> str:
        """설명 템플릿을 생성"""
        expected_text = TextProcessor.apply_text_replacements(main_text)
        
        templates = {
            "클라크래쉬": f"""**Observed:**
* {main_text}을 확인합니다.

**Sentry:**
* 링크를 첨부 중입니다.

**Expected (기대 결과):**
* {expected_text}

**Callstack:**
```

""",
            "서버크래쉬": f"""**Observed(관찰 결과):**
* {main_text}을 확인합니다.

**Video(영상):**
* 영상을 첨부 중입니다.

**Expected (기대 결과):**
* {expected_text}

**Note(참고):**
* 작성 중입니다.""",
            
            "빌드실패": f"""**Observed(관찰 결과):**
* {main_text}을 확인합니다.

**Video(영상):**
* 영상을 첨부 중입니다.

**Expected (기대 결과):**
* {expected_text}

**Note(참고):**
* 작성 중입니다."""
        }
        
        # 기본 템플릿
        default_template = f"""**Observed(관찰 결과):**
* {main_text}을 확인합니다.

**Video(영상):**
* 영상을 첨부 중입니다.

**Expected (기대 결과):**
* {expected_text}

**Note(참고):**
* 작성 중입니다."""
        
        return templates.get(option, default_template)


class OptionsManager:
    """필드 옵션 관리 클래스"""
    
    def __init__(self):
        pass
    
    def load_options(self, field_name: str, options_file: str) -> list:
        """필드 옵션들을 로드"""
        options = FileManager.load_json(options_file)
        if options and isinstance(options, list):
            return options
        return []
    
    def save_options(self, field_name: str, options_file: str, options: list) -> bool:
        """필드 옵션들을 저장"""
        try:
            FileManager.save_json(options, options_file)
            return True
        except Exception as e:
            logger.error(f"옵션 저장 실패 {field_name}: {e}")
            return False
    
    def add_option(self, field_name: str, options_file: str, new_option: str) -> bool:
        """새 옵션 추가"""
        if not new_option or new_option.strip() == "":
            return False
            
        options = self.load_options(field_name, options_file)
        new_option = new_option.strip()
        
        # 중복 확인
        if new_option not in options:
            options.insert(0, new_option)  # 최신 항목을 맨 앞에 추가
            return self.save_options(field_name, options_file, options)
        return False
    
    def remove_option(self, field_name: str, options_file: str, option: str) -> bool:
        """옵션 제거"""
        options = self.load_options(field_name, options_file)
        if option in options:
            options.remove(option)
            return self.save_options(field_name, options_file, options)
        return False


class PresetManager:
    """프리셋 관리 클래스"""
    
    def __init__(self, preset_dir: str):
        self.preset_dir = preset_dir
        if not os.path.exists(preset_dir):
            os.makedirs(preset_dir)
    
    def get_preset_files(self, sort_by_date: bool = True) -> list:
        """프리셋 파일 목록을 반환 (최신순 정렬 옵션)"""
        try:
            files = [f for f in os.listdir(self.preset_dir) if f.endswith('.json')]
            
            if sort_by_date:
                # 파일 수정 시간으로 정렬 (최신순)
                files.sort(key=lambda f: os.path.getmtime(os.path.join(self.preset_dir, f)), reverse=True)
            else:
                # 알파벳순 정렬
                files.sort()
            
            return files
        except Exception as e:
            logger.error(f"프리셋 파일 목록 조회 실패: {e}")
            return []
    
    def get_preset_prefixes(self) -> Dict[str, list]:
        """프리셋 파일들의 접두사별 그룹을 반환"""
        preset_files = self.get_preset_files()
        prefix_to_files = {}
        
        for filename in preset_files:
            parts = filename.split('_')
            if len(parts) > 1:
                prefix = parts[0]
            else:
                prefix = parts[0].replace('.json', '')
            
            if prefix not in prefix_to_files:
                prefix_to_files[prefix] = []
            prefix_to_files[prefix].append(filename)
        
        return prefix_to_files
    
    def get_preset_names_and_versions(self) -> Dict[str, Dict[str, list]]:
        """프리셋을 prefix -> name -> versions 구조로 반환"""
        preset_files = self.get_preset_files()
        structure = {}
        
        for filename in preset_files:
            file_base = filename[:-5]  # .json 제거
            parts = file_base.split('_')
            
            if len(parts) >= 2:
                prefix = parts[0]
                # 버전이 있는지 확인 (마지막이 숫자인지)
                if parts[-1].isdigit():
                    name = '_'.join(parts[1:-1])
                    version = int(parts[-1])
                else:
                    name = '_'.join(parts[1:])
                    version = 0  # 원본 버전
            else:
                # prefix만 있는 경우
                prefix = parts[0]
                name = ""
                version = 0
            
            if prefix not in structure:
                structure[prefix] = {}
            
            if name not in structure[prefix]:
                structure[prefix][name] = []
            
            structure[prefix][name].append((version, filename))
        
        # 각 name의 버전들을 내림차순으로 정렬 (최신 먼저)
        for prefix in structure:
            for name in structure[prefix]:
                structure[prefix][name].sort(reverse=True, key=lambda x: x[0])
        
        return structure
    
    def save_preset(self, filename: str, data: Dict[str, Any]) -> bool:
        """프리셋을 저장 (버전 관리 포함)"""
        try:
            if not filename.endswith('.json'):
                filename = f'{filename}.json'
            
            # 버전 관리: 동일 이름이 있으면 숫자 증가
            base_name = filename[:-5]  # .json 제거
            versioned_filename = self._get_next_version_filename(base_name)
            
            filepath = os.path.join(self.preset_dir, versioned_filename)
            FileManager.save_json(data, filepath)
            logger.info(f"프리셋 '{versioned_filename}' 저장 완료")
            return True
        except Exception as e:
            logger.error(f"프리셋 '{filename}' 저장 실패: {e}")
            return False
    
    def _get_next_version_filename(self, base_name: str) -> str:
        """다음 버전의 파일명을 생성"""
        existing_files = self.get_preset_files(sort_by_date=False)
        
        # 동일한 베이스명을 가진 파일들 찾기
        versions = []
        for file in existing_files:
            file_base = file[:-5]  # .json 제거
            
            # 정확히 같은 이름이거나 _숫자 형태인지 확인
            if file_base == base_name:
                versions.append(0)  # 원본 파일
            elif file_base.startswith(f"{base_name}_") and file_base[len(base_name)+1:].isdigit():
                version_num = int(file_base[len(base_name)+1:])
                versions.append(version_num)
        
        if not versions:
            return f"{base_name}.json"
        
        # 가장 높은 버전 + 1
        next_version = max(versions) + 1
        return f"{base_name}_{next_version}.json"
    
    def load_preset(self, filename: str) -> Optional[Dict[str, Any]]:
        """프리셋을 로드"""
        try:
            filepath = os.path.join(self.preset_dir, filename)
            return FileManager.load_json(filepath)
        except Exception as e:
            logger.error(f"프리셋 '{filename}' 로드 실패: {e}")
            return None
    
    def delete_preset(self, filename: str) -> bool:
        """프리셋을 삭제"""
        try:
            filepath = os.path.join(self.preset_dir, filename)
            os.remove(filepath)
            logger.info(f"프리셋 '{filename}' 삭제 완료")
            return True
        except Exception as e:
            logger.error(f"프리셋 '{filename}' 삭제 실패: {e}")
            return False


class ValidationHelper:
    """유효성 검사 도우미 클래스"""
    
    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """파일명이 유효한지 검사"""
        invalid_chars = '<>:"/\\|?*'
        return not any(char in filename for char in invalid_chars)
    
    @staticmethod
    def is_empty_or_whitespace(text: str) -> bool:
        """텍스트가 비어있거나 공백만 있는지 검사"""
        return not text or text.strip() == ""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """파일명을 정리"""
        invalid_chars = '<>:"/\\|?*'
        sanitized = filename
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')
        return sanitized.strip()


def setup_logging(level: int = logging.INFO) -> None:
    """로깅 설정을 초기화"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('jira_auto.log', encoding='utf-8')
        ]
    )
