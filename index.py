import os
import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QAction, QDialog,
                             QLineEdit, QTextEdit, QComboBox, QPushButton,QMessageBox, QMenuBar)
from PyQt5.QtCore import QSettings, Qt, QPoint,QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
import threading
from datetime import datetime, timedelta
# import jira2 모듈 (jira2 모듈을 설치하고 사용할 수 있는지 확인 필요)
import jira2

dir_preset = 'preset'
if not os.path.exists(dir_preset):
    os.makedirs(dir_preset)

class BugReportApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setWindowIcon(QIcon('jira_bug.ico'))
        layout = QVBoxLayout()
        # 커스텀 제목 표시줄
        # self.titleBar = QWidget(self)
        # self.titleBar.setStyleSheet("""
        #     QWidget {
        #         background-color: #222222;
        #         color: #ffffff;
        #         font-family: 'Malgun Gothic', sans-serif;
        #         font-size: 12pt;
        #         font-weight: bold;
        #         border-radius: 15px;  # 전체 애플리케이션 창에 둥근 모서리 적용
        #     }
        # """)

        menu_bar = QMenuBar(self)
        about_menu = menu_bar.addMenu("메뉴")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        about_action1 = QAction("Report Bugs", self)
        about_action1.triggered.connect(lambda event: QDesktopServices.openUrl(QUrl("https://github.com/SungMinseok/JiraAuto/issues")))
        about_menu.addActions([about_action,about_action1])

        # titleBarLayout = QHBoxLayout()
        # self.titleLabel = QLabel("Jira ttalkkag2")
        # self.minimizeButton = QPushButton("_")
        # self.minimizeButton.setFixedSize(30,30)
        # #self.maximizeButton = QPushButton("[]")
        # self.closeButton = QPushButton("X")
        # self.closeButton.setFixedSize(30,30)
        # 버튼 스타일 적용
        buttonStyle = """
            QPushButton {
                background-color: #333333;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
                color: #ffffff;
                font-family: 'Malgun Gothic', sans-serif;
            }
        """
        #self.minimizeButton.setStyleSheet(buttonStyle)
        #self.maximizeButton.setStyleSheet(buttonStyle)
        #self.closeButton.setStyleSheet(buttonStyle)

        # titleBarLayout.addWidget(self.titleLabel)
        # titleBarLayout.addStretch()
        # titleBarLayout.addWidget(self.minimizeButton)
        # #titleBarLayout.addWidget(self.maximizeButton)
        # titleBarLayout.addWidget(self.closeButton)
        #self.titleBar.setLayout(titleBarLayout)

        # 메인 레이아웃
        self.mainLayout = QVBoxLayout()
        #self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addStretch()
        layout.setMenuBar(menu_bar)

        layout.addLayout(self.mainLayout)
        #self.setLayout(self.mainLayout)
        
        # self.setStyleSheet("""
        #     QWidget {
        #         background-color: #1a1a1a;
        #         color: #ffffff;
        #         font-family: 'Malgun Gothic', sans-serif;
        #         font-size: 11pt;
        #         font-weight: bold;
        #     }

        #     QLineEdit {
        #         background-color: #333333;
        #         border: 1px solid #555555;
        #         padding: 5px;
        #         border-radius: 5px;
        #         font-family: 'Malgun Gothic', sans-serif;
        #     }
        # """)

        self.setMinimumSize(400, 300)

        # 버튼 기능 연결
        #self.minimizeButton.clicked.connect(self.showMinimized)
        # self.maximizeButton.clicked.connect(self.toggleMaximized)
        #self.closeButton.clicked.connect(self.closeEvent)

        self.isMaximized = False

        self.oldPos = self.pos()
        
        
        self.setStyleSheet("""
    QWidget {
        background-color: #1a1a1a;
        color: #ffffff;
        /*border-radius: 30px;*/
        /*border: 1px solid #333333;*/
        font-family: 'Malgun Gothic', sans-serif;
        font-size: 11pt;
        font-weight: bold
                           
    }

    QLineEdit {
        background-color: #333333;
        border: 1px solid #555555;
        /*padding: 5px;*/
        /*border-radius: 5px;*/
        font-family: 'Malgun Gothic', sans-serif;
    }

    QTextEdit {
        background-color: #333333;
        border: 1px solid #555555;
        /*padding: 5px;*/
        /*border-radius: 5px;*/
        font-family: 'Malgun Gothic', sans-serif;
    }
    QPushButton {
        background-color: #444444;
        border: 1px solid #666666;
        /*padding: 5px;*/
        /*border-radius: 5px;*/
        font-family: 'Malgun Gothic', sans-serif;
    }

    QPushButton:hover {
        background-color: #555555;
    }

    QPushButton:pressed {
        background-color: #666666;
    }

    QComboBox {
        background-color: #333333;
        border: 1px solid #555555;
        /*padding: 5px;*/
        /*border-radius: 5px;*/
        font-family: 'Malgun Gothic', sans-serif;
    }

    QCheckBox {
        background-color: transparent;
        border: none;
        font-family: 'Malgun Gothic', sans-serif;
    }

    QProgressDialog {
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #333333;
        font-family: 'Malgun Gothic', sans-serif;
    }

    QTimeEdit {
        background-color: #333333;
        border: 1px solid #555555;
        /*padding: 5px;*/
        /*border-radius: 5px;*/
        font-family: 'Malgun Gothic', sans-serif;
    }
""")
        



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

        self.apply_preset_btn = QPushButton('✅')
        self.apply_preset_btn.setToolTip('프리셋 적용')
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
            if field_name not in ["summary"] :
                temp_layout = QHBoxLayout()
                temp_label = QLabel(field_name)
                temp_label.setFixedWidth(80)
                temp_layout.addWidget(temp_label)
                temp_layout.addWidget(self.other_fields[field_name])
                if field_name in ["build"] :
                                
                    self.load_buildname_btn = QPushButton('🔄')
                    self.load_buildname_btn.setFixedWidth(25)
                    self.load_buildname_btn.clicked.connect(lambda: self.load_text_file_all('buildname.txt', self.other_fields["build"]))
                    temp_layout.addWidget(self.load_buildname_btn)
                    self.save_buildname_btn = QPushButton('💾')
                    self.save_buildname_btn.setFixedWidth(25)
                    self.save_buildname_btn.clicked.connect(lambda : self.create_text_file('buildname.txt', self.other_fields["build"].text()))
                    temp_layout.addWidget(self.save_buildname_btn)
                layout.addLayout(temp_layout)
            else:
                layout.addWidget(QLabel(field_name))
                layout.addWidget(self.other_fields[field_name])

        # Priority Dropdown
        self.priority = QComboBox()
        self.priority.addItems(["Blocker", "Critical", "High", "Medium","Low"])
        temp_layout = QHBoxLayout()
        temp_label = QLabel('Priority')
        temp_label.setFixedWidth(80)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.priority)
        layout.addLayout(temp_layout)

        # Severity Dropdown
        self.severity = QComboBox()
        self.severity.addItems(["1 - Critical", "2 - Major", "3 - Minor"])
        temp_layout = QHBoxLayout()
        temp_label = QLabel('severity')
        temp_label.setFixedWidth(80)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.severity)
        layout.addLayout(temp_layout)

        # Prevalence Dropdown
        self.prevalence = QComboBox()
        self.prevalence.addItems(["1 - All users", "2 - The majority of users", "3 - Half Of users", "4 - Almost no users", "5 - Encountered by single user"])
        temp_layout = QHBoxLayout()
        temp_label = QLabel('prevalence')
        temp_label.setFixedWidth(80)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.prevalence)
        layout.addLayout(temp_layout)

        # Repro Rate Dropdown
        self.repro_rate = QComboBox()
        self.repro_rate.addItems(["1 - 100% reproducible", "2 - Most times", "3 - Approximately half the time", "4 - Rare", "5 - Seen Once"])
        temp_layout = QHBoxLayout()
        temp_label = QLabel('repro_rate')
        temp_label.setFixedWidth(80)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.repro_rate)
        layout.addLayout(temp_layout)

        # Steps QTextEdit
        self.steps = QTextEdit()
        self.steps.setAcceptRichText(False)
        layout.addWidget(QLabel('Steps'))
        layout.addWidget(self.steps)

        # Description QTextEdit
        self.description = QTextEdit()
        self.description.setAcceptRichText(False)
        layout.addWidget(QLabel('Description'))
        layout.addWidget(self.description)

        # # Save Button
        # self.save_btn = QPushButton('Save')
        # self.save_btn.clicked.connect(self.saveSettings)
        # layout.addWidget(self.save_btn)

        # Generate Button
        self.generate_option = QComboBox()
        self.generate_option.addItems(["기본값","크래쉬"])
        
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
        result_text = result_text.replace('하는 현상', '하지 않아야 합니다.')
        result_text = result_text.replace('되지 않는 현상', '되어야 합니다.')
        result_text = result_text.replace('되지 않은 현상', '되어야 합니다.')
        result_text = result_text.replace('없는 현상', '있어야 합니다.')
        result_text = result_text.replace('있는 현상', '있지 않아야 합니다.')
        result_text = result_text.replace('지는 현상', '지지 않아야 합니다.')

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

    

    def create_text_file(self, filename, content):
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")

    def load_text_file_all(self, filename, target = None):
        with open(filename, 'r') as file:
            content = file.read()
        if target != None :
            target.setText(content)
    
    def load_text_file_line_by_line(self, filename, target = None):
        with open(filename, 'r') as file:
            content = file.readlines()
        return content
    
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F12:
            self.debug_function()  # Call the function to execute on F12 press

    def debug_function(self):
        #self.show_file_count()
        # Replace this with whatever you want to happen when F12 is pressed
        #QMessageBox.information(self, 'Debugging', 'F12 pressed: Debugging function executed.')
        jira2.aws_upload_custom(44)
        #self.zip_folder(self.input_box2.text(),self.combo_box.currentText(),'WindowsServer')
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragging:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False


    def get_most_recent_file(self):
        # Get a list of all files in the current directory
        #files = [f for f in os.listdir('.') if os.path.isfile(f)]
        files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.endswith('.json')]
        # Initialize variables to track the most recent file and its modification time
        most_recent_file = None
        most_recent_time = 0
        
        for file in files:
            # Get the last modification time
            mod_time = os.path.getmtime(file)
            
            # Check if this file is the most recent one we've encountered
            if mod_time > most_recent_time:
                most_recent_time = mod_time
                most_recent_file = file
        
        if most_recent_file:
            # Convert the most recent time to a readable format
            most_recent_time_readable = datetime.fromtimestamp(most_recent_time).strftime('%Y-%m-%d %H:%M:%S')
            return most_recent_file, most_recent_time_readable
        else:
            return None, None

    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About")
        layout = QVBoxLayout()
        recent_file_name, recent_moditime = self.get_most_recent_file()

        version_label = QLabel("Version: v1.0", about_dialog)
        last_update_label = QLabel(f"Last update date: {recent_moditime}", about_dialog)
        created_by_label = QLabel("Created by: mssung@pubg.com", about_dialog)
        first_production_date_label = QLabel("First production date: 2024-07-01", about_dialog)

        #github_label = QLabel("GitHub link:", about_dialog)
        #github_icon = QLabel("Issues", about_dialog)
        #pixmap = QPixmap("github_icon.png")  # Replace with the path to your GitHub icon
        #github_icon.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #github_icon.setCursor(Qt.PointingHandCursor)
        #github_icon.mousePressEvent = lambda event: QDesktopServices.openUrl(QUrl("https://github.com/SungMinseok/GetBuild/issues"))

        layout.addWidget(version_label)
        layout.addWidget(last_update_label)
        layout.addWidget(created_by_label)
        layout.addWidget(first_production_date_label)

        h_layout = QHBoxLayout()
        h_layout.addWidget(QPushButton())
        h_layout.addWidget(QPushButton())
        layout.addLayout(h_layout)

        about_dialog.setLayout(layout)
        about_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BugReportApp()
    sys.exit(app.exec_())
