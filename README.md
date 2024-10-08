
# Bug Report Automation Tool

This project is a bug report automation tool that integrates with Jira to facilitate the creation of bug reports. It consists of two main files:

- `index.py`
- `jira2.py`

## Overview

- **index.py**: This is the main GUI application using PyQt5. It provides a user interface for entering bug report details and interacts with Jira to create issues automatically.
- **jira2.py**: This script handles interactions with Jira using Selenium for web automation. It includes functions to start a Chrome WebDriver and automate the creation of issues on a Jira dashboard.

## Requirements

- Python 3.x
- PyQt5
- Selenium
- chromedriver-autoinstaller
- Google Chrome browser installed

## Setup and Installation

1. **Install Python dependencies**:
   ```bash
   pip install PyQt5 selenium chromedriver-autoinstaller requests
   ```

2. **Download Google Chrome**:
   Ensure that Google Chrome is installed on your system.

3. **Set up the Chrome WebDriver**:
   The script uses `chromedriver-autoinstaller` to automatically download and set up the correct version of Chrome WebDriver.

## Usage

### Starting the Application

Run the `index.py` file to launch the GUI application:

```bash
python index.py
```

### Features

#### `index.py` - GUI Application

- **User Interface**: Provides a form to enter bug report details such as summary, reviewer, branch, build, version, component, label, priority, severity, prevalence, and reproduction rate.
- **Preset Management**: Load, save, and apply presets for different bug reporting scenarios.
- **Automated Bug Report Creation**: Automates the process of creating bug reports in Jira using the `jira2` module.
- **Description Generation**: Auto-generates the description based on the provided summary.
- **Execute Button**: When clicked, it calls the `create_issue` function in `jira2.py` to create a bug report in Jira.

#### `jira2.py` - Jira Automation Script

- **Start WebDriver**: Starts a Chrome WebDriver session. If Chrome is not running, it launches a new instance with remote debugging enabled.
- **Create Jira Issue**: Automates the creation of an issue in Jira using Selenium to fill in the necessary fields and submit the form.

### Notes

- **Chrome Setup**: The application uses a specific Chrome user data directory (`C:\ChromeTEMP`) and the Chrome executable path (`C:\Program Files\Google\Chrome\Application\chrome.exe`). Ensure these paths are correctly set up on your system.
- **Jira URL**: The default Jira URL used in the `create_issue` function is `https://jira.krafton.com/secure/Dashboard.jspa`. Update this URL to match your Jira instance if necessary.

## Troubleshooting

- **Connection Errors**: Ensure that Chrome is installed and accessible at the specified path. If you encounter a connection error, make sure that no other Chrome instance is running on the remote debugging port (9222).
- **Missing Dependencies**: Ensure all required Python packages are installed.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Selenium for web automation
- PyQt5 for GUI components
