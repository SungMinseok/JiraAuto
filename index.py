import os
import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QComboBox, QPushButton)
from PyQt5.QtCore import QSettings
import threading
# import jira2 모듈 (jira2 모듈을 설치하고 사용할 수 있는지 확인 필요)
import jira2

dir_preset = 'preset'
if not os.path.exists('dir_preset'):
    os.makedirs('dir_preset')

class BugReportApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        #self.settings = QSettings('settings.json', QSettings.NativeFormat)
        #self.settings_file = 'settings.json'

        layout = QVBoxLayout()


        # Priority Dropdown
        preset_layout = QHBoxLayout()
        self.preset = QComboBox()
        layout.addWidget(QLabel('Preset'))
        #layout.addWidget(self.preset)
        preset_layout.addWidget(self.preset)

        # Refresh and Apply Preset Buttons
        self.refresh_preset_btn = QPushButton('🔄')
        self.refresh_preset_btn.setFixedWidth(25)
        self.refresh_preset_btn.clicked.connect(self.refreshPresets)
        preset_layout.addWidget(self.refresh_preset_btn)

        self.apply_preset_btn = QPushButton('📁')
        self.apply_preset_btn.setFixedWidth(25)
        self.apply_preset_btn.clicked.connect(self.applyPreset)
        preset_layout.addWidget(self.apply_preset_btn)

        layout.addLayout(preset_layout)

        add_preset_layout = QHBoxLayout()

        self.add_preset_line = QLineEdit()
        add_preset_layout.addWidget(self.add_preset_line)
        
        self.save_preset_btn = QPushButton('💾')
        self.save_preset_btn.setFixedWidth(25)
        self.save_preset_btn.clicked.connect(self.savePreset)
        add_preset_layout.addWidget(self.save_preset_btn)

        layout.addLayout(add_preset_layout)

        # Other QLineEdits
        self.other_fields = {}
        for field_name in ["summary", "reviewer", "branch", "build", "fixversion", "component", "label"]:
            self.other_fields[field_name] = QLineEdit()
            layout.addWidget(QLabel(field_name))
            layout.addWidget(self.other_fields[field_name])

        # Priority Dropdown
        self.priority = QComboBox()
        self.priority.addItems(["Blocker", "Critical", "High", "Medium","Low"])
        layout.addWidget(QLabel('Priority'))
        layout.addWidget(self.priority)

        # Severity Dropdown
        self.severity = QComboBox()
        self.severity.addItems(["1 - Critical", "2 - Major", "3 - Minor"])
        layout.addWidget(QLabel('Severity'))
        layout.addWidget(self.severity)

        # Prevalence Dropdown
        self.prevalence = QComboBox()
        self.prevalence.addItems(["1 - All users", "2 - The majority of users", "3 - Half Of users", "4 - Almost no users", "5 - Encountered by single user"])
        layout.addWidget(QLabel('Prevalence'))
        layout.addWidget(self.prevalence)

        # Repro Rate Dropdown
        self.repro_rate = QComboBox()
        self.repro_rate.addItems(["1 - 100% reproducible", "2 - Most times", "3 - Approximately half the time", "4 - Rare", "5 - Seen Once"])
        layout.addWidget(QLabel('Repro Rate'))
        layout.addWidget(self.repro_rate)

        # Steps QTextEdit
        self.steps = QTextEdit()
        layout.addWidget(QLabel('Steps'))
        layout.addWidget(self.steps)

        # Description QTextEdit
        self.description = QTextEdit()
        layout.addWidget(QLabel('Description'))
        layout.addWidget(self.description)

        # # Save Button
        # self.save_btn = QPushButton('Save')
        # self.save_btn.clicked.connect(self.saveSettings)
        # layout.addWidget(self.save_btn)

        # Generate Button
        self.generate_btn = QPushButton('Auto Generate')
        self.generate_btn.clicked.connect(self.generate_description)
        layout.addWidget(self.generate_btn)

        # Execute Button
        self.execute_btn = QPushButton('Execute')
        self.execute_btn.clicked.connect(self.execute)
        layout.addWidget(self.execute_btn)

        self.setLayout(layout)
        self.loadSettings()
        self.setWindowTitle('Bug Report')
        self.show()

    def generate_description(self):
        main_text = self.other_fields['summary'].text()

        result_text = main_text.replace('다른 현상', '동일해야 합니다.')
        result_text = result_text.replace('하지 않는 현상', '해야 합니다.')
        result_text = result_text.replace('되는 현상', '되지 않아야 합니다.')
        result_text = result_text.replace('되지 않는 현상', '되어야 합니다.')
        result_text = result_text.replace('없는 현상', '있어야 합니다.')
        result_text = result_text.replace('있는 현상', '있지 않아야 합니다.')

        after_desc = f'*Observed(관찰 결과):*\n\n\
 * {main_text}을 확인합니다.\n\n\
*Video(영상):*\n\n\
 * 영상을 첨부 중입니다.\n\n\
*Expected(기대 결과):*\n\n\
 * {result_text}\n\n\
*Note(참고):*\n\n\
 * 참고사항을 작성 중입니다.'
        self.description.setText(after_desc)


    def saveSettings(self, filename=f'{dir_preset}/settings.json'):
        settings = {
            'priority': self.priority.currentText(),
            'severity': self.severity.currentText(),
            'prevalence': self.prevalence.currentText(),
            'repro_rate': self.repro_rate.currentText(),
            'steps': self.steps.toPlainText(),
            'description': self.description.toPlainText(),
        }
        
        for field_name in self.other_fields:
            settings[field_name] = self.other_fields[field_name].text()

        with open(f'{dir_preset}/{filename}', 'w') as file:
            json.dump(settings, file, indent=4)

    def loadSettings(self, filename=f'{dir_preset}/settings.json'):
        try:
            with open(f'{dir_preset}/{filename}', 'r') as file:
                settings = json.load(file)

            self.priority.setCurrentText(settings.get('priority', 'Blocker'))
            self.severity.setCurrentText(settings.get('severity', '1 - Critical'))
            self.prevalence.setCurrentText(settings.get('prevalence', '1 - All users'))
            self.repro_rate.setCurrentText(settings.get('repro_rate', '1 - 100% reproducible'))
            self.steps.setPlainText(settings.get('steps', ''))
            self.description.setPlainText(settings.get('description', ''))

            for field_name in self.other_fields:
                self.other_fields[field_name].setText(settings.get(field_name, ''))
        except FileNotFoundError:
            pass

    def execute(self):
        reviewer = self.other_fields['reviewer'].text()
        branch = self.other_fields['branch'].text()
        build = self.other_fields['build'].text()
        fixversion = self.other_fields['fixversion'].text()
        component = self.other_fields['component'].text()
        label = self.other_fields['label'].text()
        summary = f'[{label}] {self.other_fields['summary'].text()}'
        priority = self.priority.currentText()
        severity = self.severity.currentText()
        prevalence = self.prevalence.currentText()
        repro_rate = self.repro_rate.currentText()
        steps = self.steps.toPlainText()
        description = self.description.toPlainText()

        def thread_function():
            jira2.create_issue(summary, reviewer, branch, build, fixversion, component, label, priority, severity, prevalence, repro_rate, steps, description)

        # 스레드 생성 및 시작
        issue_thread = threading.Thread(target=thread_function)
        issue_thread.start()

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def refreshPresets(self):
        self.preset.clear()
        dir_preset = 'preset'  # 디렉토리 경로 설정
        preset_files = [f for f in os.listdir(dir_preset) if f.endswith('.json')]
        preset_files.sort(key=lambda f: os.path.getmtime(os.path.join(dir_preset, f)), reverse=True)
        self.preset.addItems(preset_files)

    def applyPreset(self):
        selected_preset = self.preset.currentText()
        if selected_preset:
            self.loadSettings(selected_preset)
    def savePreset(self):
        new_preset = self.add_preset_line.text()
        if new_preset:
            if '.json' not in new_preset :
                new_preset = f'{new_preset}.json'
            self.saveSettings(new_preset)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BugReportApp()
    sys.exit(app.exec_())
