"""
기존 호환성을 위한 wrapper 모듈
jira_automation 모듈을 감싸서 기존 import 구조를 유지합니다.
"""
import warnings

# 기존 호환성을 위한 import
from jira_automation import create_issue

warnings.warn(
    "jira2.py는 deprecated입니다. 직접 jira_automation.py를 사용하세요.",
    DeprecationWarning,
    stacklevel=2
)

# 기존 호환성을 위해 필요한 함수들을 re-export
__all__ = ['create_issue']