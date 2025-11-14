"""
GUI 위젯들과 레이아웃을 관리하는 모듈
"""
import os
from typing import Dict, Any, Callable
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QPushButton, QCheckBox, QMenuBar, QAction,
    QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon

from config import DropdownOptions, FIELD_NAMES, COMBO_FIELD_NAMES, OPTIONS_FILES


class ComboFieldWithButtons:
    """+/- 버튼이 있는 콤보박스 필드"""
    
    def __init__(self, field_name: str, label_width: int = 80):
        self.field_name = field_name
        self.label_width = label_width
        self.widget = None
        self.layout = None
        self.add_button = None
        self.remove_button = None
        self.options_manager = None  # 나중에 외부에서 설정
    
    def create_combo_field(self, parent_layout, options: list = None) -> QComboBox:
        """콤보박스 필드를 생성"""
        self.widget = QComboBox()
        self.widget.setEditable(True)  # 편집 가능하도록 설정
        
        if options:
            self.widget.addItems(options)
        
        self.layout = QHBoxLayout()
        
        # 라벨
        label = QLabel(self.field_name)
        label.setFixedWidth(self.label_width)
        self.layout.addWidget(label)
        
        # 콤보박스
        self.layout.addWidget(self.widget)
        
        # + 버튼
        self.add_button = QPushButton('+')
        self.add_button.setFixedWidth(25)
        self.add_button.setToolTip(f'{self.field_name} 옵션 추가')
        self.layout.addWidget(self.add_button)
        
        # - 버튼
        self.remove_button = QPushButton('-')
        self.remove_button.setFixedWidth(25)
        self.remove_button.setToolTip(f'{self.field_name} 옵션 삭제')
        self.layout.addWidget(self.remove_button)
        
        parent_layout.addLayout(self.layout)
        return self.widget
    
    def set_options_manager(self, options_manager):
        """옵션 매니저 설정"""
        self.options_manager = options_manager
    
    def add_option(self):
        """현재 텍스트를 옵션으로 추가"""
        if not self.options_manager:
            return
            
        current_text = self.widget.currentText().strip()
        if current_text:
            options_file = OPTIONS_FILES.get(self.field_name, f'{self.field_name}_options.json')
            success = self.options_manager.add_option(self.field_name, options_file, current_text)
            if success:
                # 콤보박스 새로고침
                self.refresh_options()
                # 추가된 항목을 선택
                self.widget.setCurrentText(current_text)
    
    def remove_option(self):
        """현재 선택된 옵션 삭제"""
        if not self.options_manager:
            return
            
        current_text = self.widget.currentText().strip()
        if current_text:
            options_file = OPTIONS_FILES.get(self.field_name, f'{self.field_name}_options.json')
            success = self.options_manager.remove_option(self.field_name, options_file, current_text)
            if success:
                # 콤보박스 새로고침
                self.refresh_options()
    
    def refresh_options(self):
        """옵션 목록 새로고침"""
        if not self.options_manager:
            return
            
        options_file = OPTIONS_FILES.get(self.field_name, f'{self.field_name}_options.json')
        options = self.options_manager.load_options(self.field_name, options_file)
        
        current_text = self.widget.currentText()
        self.widget.clear()
        self.widget.addItems(options)
        self.widget.setCurrentText(current_text)


class FieldWidget:
    """필드 위젯을 관리하는 클래스"""
    
    def __init__(self, field_name: str, label_width: int = 80):
        self.field_name = field_name
        self.label_width = label_width
        self.widget = None
        self.layout = None
        self.extra_buttons = []
    
    def create_line_edit_field(self, parent_layout: QVBoxLayout) -> QLineEdit:
        """QLineEdit 필드를 생성"""
        self.widget = QLineEdit()
        
        if self.field_name == "summary":
            self._create_summary_field(parent_layout)
        else:
            self._create_standard_field(parent_layout)
        
        return self.widget
    
    def _create_summary_field(self, parent_layout: QVBoxLayout):
        """Summary 필드 특별 처리 (2줄 텍스트 입력)"""
        parent_layout.addWidget(QLabel(self.field_name))
        self.layout = QHBoxLayout()
        
        sub_label = QLineEdit()
        sub_label.setFixedWidth(self.label_width)
        self.layout.addWidget(sub_label)
        
        # QLineEdit 대신 QTextEdit 사용하여 2줄로 만들기
        from PyQt5.QtWidgets import QTextEdit
        summary_text = QTextEdit()
        summary_text.setMaximumHeight(60)  # 2줄 정도의 높이
        summary_text.setAcceptRichText(False)  # 일반 텍스트만
        summary_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 스크롤바 제거
        summary_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 기존 QLineEdit 위젯을 QTextEdit로 교체
        self.widget = summary_text
        self.layout.addWidget(self.widget)
        
        # AI 생성 버튼 추가
        ai_button = QPushButton('🤖 AI 생성')
        ai_button.setFixedWidth(100)
        ai_button.setToolTip('로컬 LLM으로 버그 세부 정보 자동 생성')
        self.layout.addWidget(ai_button)
        self.extra_buttons.append(('ai_generate', ai_button, None))
        
        parent_layout.addLayout(self.layout)
        # sub_label을 별도로 반환할 수 있도록 저장
        self.sub_label = sub_label
    
    def _create_standard_field(self, parent_layout: QVBoxLayout):
        """표준 필드 생성"""
        self.layout = QHBoxLayout()
        
        label = QLabel(self.field_name)
        label.setFixedWidth(self.label_width)
        self.layout.addWidget(label)
        self.layout.addWidget(self.widget)
        
        # 특별한 버튼들 추가
        if self.field_name in ["build", "fixversion"]:
            self._add_file_buttons()
        elif self.field_name == "label":
            self._add_checkbox()
        
        parent_layout.addLayout(self.layout)
    
    def _add_file_buttons(self):
        """파일 관련 버튼들 추가"""
        filename = f"{self.field_name}.txt" if self.field_name == "build" else "fixversion.txt"
        
        # 로드 버튼
        load_btn = QPushButton('🔄')
        load_btn.setFixedWidth(25)
        load_btn.setToolTip(f'{filename} 파일에서 로드')
        self.layout.addWidget(load_btn)
        self.extra_buttons.append(('load', load_btn, filename))
        
        # 저장 버튼
        save_btn = QPushButton('💾')
        save_btn.setFixedWidth(25)
        save_btn.setToolTip(f'{filename} 파일로 저장')
        self.layout.addWidget(save_btn)
        self.extra_buttons.append(('save', save_btn, filename))
    
    def _add_checkbox(self):
        """체크박스 추가 (label 필드용)"""
        checkbox = QCheckBox('Include')
        checkbox.setFixedWidth(75)
        checkbox.setToolTip('메인 라벨 포함 여부')
        self.layout.addWidget(checkbox)
        self.extra_buttons.append(('checkbox', checkbox, None))


class ComboFieldWidget:
    """콤보박스 필드를 관리하는 클래스"""
    
    def __init__(self, field_name: str, options: list, label_width: int = 80):
        self.field_name = field_name
        self.options = options
        self.label_width = label_width
        self.widget = None
        self.layout = None
    
    def create_combo_field(self, parent_layout: QVBoxLayout) -> QComboBox:
        """콤보박스 필드를 생성"""
        self.widget = QComboBox()
        self.widget.addItems(self.options)
        
        self.layout = QHBoxLayout()
        
        label = QLabel(self.field_name)
        label.setFixedWidth(self.label_width)
        self.layout.addWidget(label)
        self.layout.addWidget(self.widget)
        
        parent_layout.addLayout(self.layout)
        return self.widget


class PresetWidget:
    """프리셋 위젯을 관리하는 클래스"""
    
    def __init__(self):
        self.prefix_combo = None
        self.name_combo = None  # 새로 추가: 이름별 선택
        self.version_combo = None  # 새로 추가: 버전별 선택
        self.preset_line = None
        self.sort_combo = None
        self.buttons = {}
        
    def create_preset_section(self, parent_layout: QVBoxLayout) -> Dict[str, QWidget]:
        """프리셋 섹션을 생성"""
        parent_layout.addWidget(QLabel('Preset'))
        
        # 정렬 옵션
        sort_layout = QHBoxLayout()
        sort_label = QLabel('정렬:')
        sort_label.setFixedWidth(40)
        sort_layout.addWidget(sort_label)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(['최신순', '이름순'])
        self.sort_combo.setFixedWidth(80)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addStretch()
        
        parent_layout.addLayout(sort_layout)
        
        # 프리셋 콤보박스들 (3단계: prefix -> name -> version)
        preset_layout = QHBoxLayout()
        
        # Prefix 선택
        prefix_label = QLabel('카테고리:')
        prefix_label.setFixedWidth(50)
        preset_layout.addWidget(prefix_label)
        
        self.prefix_combo = QComboBox()
        self.prefix_combo.setFixedWidth(120)
        preset_layout.addWidget(self.prefix_combo)
        
        # Name 선택
        name_label = QLabel('이름:')
        name_label.setFixedWidth(35)
        preset_layout.addWidget(name_label)
        
        self.name_combo = QComboBox()
        self.name_combo.setFixedWidth(150)
        preset_layout.addWidget(self.name_combo)
        
        # Version 선택
        version_label = QLabel('버전:')
        version_label.setFixedWidth(35)
        preset_layout.addWidget(version_label)
        
        self.version_combo = QComboBox()
        self.version_combo.setFixedWidth(80)
        preset_layout.addWidget(self.version_combo)
        
        # 프리셋 관리 버튼들
        self._add_preset_buttons(preset_layout)
        
        parent_layout.addLayout(preset_layout)
        
        # 프리셋 입력 라인
        add_preset_layout = QHBoxLayout()
        self.preset_line = QLineEdit()
        add_preset_layout.addWidget(self.preset_line)
        
        save_btn = QPushButton('💾')
        save_btn.setFixedWidth(25)
        save_btn.setToolTip('프리셋 저장')
        add_preset_layout.addWidget(save_btn)
        self.buttons['save_preset'] = save_btn
        
        parent_layout.addLayout(add_preset_layout)
        
        return {
            'prefix_combo': self.prefix_combo,
            'name_combo': self.name_combo,
            'version_combo': self.version_combo,
            'preset_line': self.preset_line,
            'sort_combo': self.sort_combo,
            'buttons': self.buttons
        }
    
    def _add_preset_buttons(self, layout: QHBoxLayout):
        """프리셋 관리 버튼들을 추가"""
        # 삭제 버튼
        delete_btn = QPushButton('❌')
        delete_btn.setFixedWidth(25)
        delete_btn.setToolTip('프리셋 삭제')
        layout.addWidget(delete_btn)
        self.buttons['delete'] = delete_btn
        
        # 새로고침 버튼  
        refresh_btn = QPushButton('🔄')
        refresh_btn.setFixedWidth(25)
        refresh_btn.setToolTip('프리셋 새로고침 (F5)')
        layout.addWidget(refresh_btn)
        self.buttons['refresh'] = refresh_btn
        
        # 적용 버튼
        apply_btn = QPushButton('✅')
        apply_btn.setFixedWidth(25)
        apply_btn.setToolTip('프리셋 적용 (F6)')
        layout.addWidget(apply_btn)
        self.buttons['apply'] = apply_btn


class TextFieldWidget:
    """텍스트 필드 위젯을 관리하는 클래스"""
    
    def __init__(self, field_name: str):
        self.field_name = field_name
        self.widget = None
    
    def create_text_field(self, parent_layout: QVBoxLayout) -> QTextEdit:
        """QTextEdit 필드를 생성"""
        self.widget = QTextEdit()
        self.widget.setAcceptRichText(False)
        
        parent_layout.addWidget(QLabel(self.field_name))
        parent_layout.addWidget(self.widget)
        
        return self.widget


class ActionButtonsWidget:
    """액션 버튼들을 관리하는 클래스"""
    
    def __init__(self):
        self.buttons = {}
        self.generate_combo = None
    
    def create_action_buttons(self, parent_layout: QVBoxLayout) -> Dict[str, QWidget]:
        """액션 버튼들을 생성"""
        # Generate 섹션
        generate_layout = QHBoxLayout()
        
        self.generate_combo = QComboBox()
        self.generate_combo.addItems(DropdownOptions.GENERATE_OPTIONS)
        generate_layout.addWidget(self.generate_combo)
        
        generate_btn = QPushButton('Auto Generate')
        generate_btn.setToolTip('자동 설명 생성')
        generate_layout.addWidget(generate_btn)
        self.buttons['generate'] = generate_btn
        
        parent_layout.addLayout(generate_layout)
        
        # Execute 버튼
        execute_btn = QPushButton('Execute (F2)')
        execute_btn.setToolTip('JIRA 이슈 생성 (F2)')
        parent_layout.addWidget(execute_btn)
        self.buttons['execute'] = execute_btn
        
        return {
            'generate_combo': self.generate_combo,
            'buttons': self.buttons
        }


class SettingsDialog(QDialog):
    """설정 다이얼로그"""
    
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.settings = settings or {}
        
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout()
        
        # 엑셀 추출 옵션
        excel_layout = QHBoxLayout()
        excel_label = QLabel("엑셀로 버그 정보 추출:")
        excel_label.setFixedWidth(200)
        excel_layout.addWidget(excel_label)
        
        self.excel_export_checkbox = QCheckBox("활성화")
        self.excel_export_checkbox.setChecked(self.settings.get('excel_export_enabled', True))
        excel_layout.addWidget(self.excel_export_checkbox)
        excel_layout.addStretch()
        
        layout.addLayout(excel_layout)
        
        # 설명 라벨
        info_label = QLabel(
            "• Execute 실행 시 버그 정보를 엑셀 파일로 자동 저장합니다.\n"
            "• 파일 위치: result/bug_reports.xlsx\n"
            "• 이미 파일이 있으면 이어서 작성됩니다."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #aaaaaa; font-size: 9pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(20)
        
        # 버튼들
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_settings(self):
        """설정 값 반환"""
        return {
            'excel_export_enabled': self.excel_export_checkbox.isChecked()
        }


class MenuBarWidget:
    """메뉴바 위젯을 관리하는 클래스"""
    
    @staticmethod
    def create_menu_bar(parent: QWidget, about_callback: Callable, settings_callback: Callable = None) -> QMenuBar:
        """메뉴바를 생성"""
        menu_bar = QMenuBar(parent)
        about_menu = menu_bar.addMenu("메뉴")
        
        # Settings 액션
        if settings_callback:
            settings_action = QAction("Settings", parent)
            settings_action.triggered.connect(settings_callback)
            about_menu.addAction(settings_action)
            about_menu.addSeparator()
        
        # About 액션
        about_action = QAction("About", parent)
        about_action.triggered.connect(about_callback)
        
        # Report Bugs 액션  
        report_action = QAction("Report Bugs", parent)
        report_action.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/SungMinseok/JiraAuto/issues")
            )
        )
        
        about_menu.addActions([about_action, report_action])
        return menu_bar


class ExcelBatchWidget:
    """엑셀 일괄 실행 위젯"""
    
    @staticmethod
    def create_excel_batch_section(layout: QVBoxLayout) -> Dict[str, Any]:
        """엑셀 일괄 실행 섹션 생성"""
        # 구분선
        layout.addSpacing(20)
        separator = QLabel("─" * 80)
        separator.setStyleSheet("color: #555555;")
        layout.addWidget(separator)
        
        # 제목
        title_label = QLabel("📋 엑셀 파일 일괄 JIRA 생성")
        title_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #4a9eff;")
        layout.addWidget(title_label)
        
        # 설명
        info_label = QLabel(
            "엑셀 파일(bug_reports.xlsx)의 각 행을 읽어서 순차적으로 JIRA 이슈를 생성합니다.\n"
            "각 이슈는 최종 확인을 위해 생성 전까지만 진행되며, 수동으로 제출해야 합니다."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #aaaaaa; font-size: 9pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # 엑셀 파일 경로 입력
        path_layout = QHBoxLayout()
        path_label = QLabel("엑셀 파일 경로:")
        path_label.setFixedWidth(100)
        path_layout.addWidget(path_label)
        
        path_input = QLineEdit()
        path_input.setPlaceholderText("예: result/bug_reports.xlsx")
        # 기본값 설정
        default_path = os.path.join("result", "bug_reports.xlsx")
        path_input.setText(default_path)
        path_layout.addWidget(path_input)
        
        layout.addLayout(path_layout)
        
        layout.addSpacing(10)
        
        # 버튼들
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 파일 열기 버튼
        open_file_btn = QPushButton("📂 엑셀 파일 열기")
        open_file_btn.setFixedWidth(150)
        open_file_btn.setToolTip("엑셀 파일을 열어서 내용을 확인합니다")
        button_layout.addWidget(open_file_btn)
        
        # 실행 버튼
        execute_btn = QPushButton("▶ 일괄 실행")
        execute_btn.setFixedWidth(150)
        execute_btn.setToolTip("엑셀 파일의 각 행을 순차적으로 JIRA로 생성합니다")
        execute_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
            QPushButton:pressed {
                background-color: #1b5e20;
            }
        """)
        button_layout.addWidget(execute_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addSpacing(10)
        
        return {
            'path_input': path_input,
            'open_file_btn': open_file_btn,
            'execute_btn': execute_btn
        }


class FormBuilder:
    """폼을 구성하는 빌더 클래스"""
    
    def __init__(self):
        self.field_widgets = {}
        self.combo_widgets = {}
        self.combo_field_widgets = {}  # 새로운 콤보 필드들
        self.text_widgets = {}
        self.preset_widget = None
        self.action_widget = None
        self.excel_batch_widget = None
    
    def build_complete_form(self, parent: QWidget, about_callback: Callable, settings_callback: Callable = None) -> Dict[str, Any]:
        """완전한 폼을 구성"""
        layout = QVBoxLayout()
        
        # 메뉴바 생성
        menu_bar = MenuBarWidget.create_menu_bar(parent, about_callback, settings_callback)
        layout.setMenuBar(menu_bar)
        
        # 프리셋 섹션
        self.preset_widget = PresetWidget()
        preset_widgets = self.preset_widget.create_preset_section(layout)
        
        # 필드들 생성
        self._create_form_fields(layout)
        
        # 콤보박스 필드들 (기존 priority, severity 등)
        self._create_combo_fields(layout)
        
        # 새로운 콤보 필드들 (branch, build, fixversion, component)
        self._create_combo_field_with_buttons(layout)
        
        # 텍스트 필드들
        self._create_text_fields(layout)
        
        # 액션 버튼들
        self.action_widget = ActionButtonsWidget()
        action_widgets = self.action_widget.create_action_buttons(layout)
        
        # 엑셀 일괄 실행 섹션
        self.excel_batch_widget = ExcelBatchWidget()
        excel_batch_widgets = self.excel_batch_widget.create_excel_batch_section(layout)
        
        return {
            'layout': layout,
            'menu_bar': menu_bar,
            'preset_widgets': preset_widgets,
            'field_widgets': self.field_widgets,
            'combo_widgets': self.combo_widgets,
            'combo_field_widgets': self.combo_field_widgets,  # 새로운 콤보 필드들
            'text_widgets': self.text_widgets,
            'action_widgets': action_widgets,
            'excel_batch': excel_batch_widgets  # 엑셀 일괄 실행 위젯들
        }
    
    def _create_form_fields(self, layout: QVBoxLayout):
        """폼 필드들을 생성"""
        for field_name in FIELD_NAMES:
            field_widget = FieldWidget(field_name)
            widget = field_widget.create_line_edit_field(layout)
            self.field_widgets[field_name] = {
                'widget': widget,
                'field_widget': field_widget
            }
    
    def _create_combo_fields(self, layout: QVBoxLayout):
        """콤보박스 필드들을 생성"""
        combo_configs = [
            ('Priority', DropdownOptions.PRIORITY_OPTIONS),
            ('severity', DropdownOptions.SEVERITY_OPTIONS),
            ('prevalence', DropdownOptions.PREVALENCE_OPTIONS),
            ('repro_rate', DropdownOptions.REPRO_RATE_OPTIONS)
        ]
        
        for field_name, options in combo_configs:
            combo_widget = ComboFieldWidget(field_name, options)
            widget = combo_widget.create_combo_field(layout)
            self.combo_widgets[field_name.lower()] = {
                'widget': widget,
                'combo_widget': combo_widget
            }
    
    def _create_combo_field_with_buttons(self, layout: QVBoxLayout):
        """콤보박스 + 버튼 필드들을 생성"""
        for field_name in COMBO_FIELD_NAMES:
            combo_field_widget = ComboFieldWithButtons(field_name)
            widget = combo_field_widget.create_combo_field(layout)
            self.combo_field_widgets[field_name] = {
                'widget': widget,
                'combo_field_widget': combo_field_widget
            }
    
    def _create_text_fields(self, layout: QVBoxLayout):
        """텍스트 필드들을 생성"""
        text_fields = ['Steps', 'Description']
        
        for field_name in text_fields:
            text_widget = TextFieldWidget(field_name)
            widget = text_widget.create_text_field(layout)
            self.text_widgets[field_name.lower()] = {
                'widget': widget,
                'text_widget': text_widget
            }


def create_main_form(parent: QWidget, about_callback: Callable, settings_callback: Callable = None) -> Dict[str, Any]:
    """메인 폼을 생성하는 편의 함수"""
    builder = FormBuilder()
    return builder.build_complete_form(parent, about_callback, settings_callback)
