"""
기존 호환성을 위한 launcher
main_application.py를 실행합니다.
"""
import warnings

warnings.warn(
    "index.py는 deprecated입니다. 직접 main_application.py를 실행하세요.",
    DeprecationWarning,
    stacklevel=2
)

# 기존 호환성을 위해 main_application을 실행
if __name__ == "__main__":
    from main_application import main
    main()