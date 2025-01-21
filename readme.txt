Selenium Automation Script for Sendcloud

Overview:
This project automates tasks on the Sendcloud platform using Selenium, a Python library for web browser automation. The script is designed to log in to Sendcloud, load all order records by scrolling, and process orders while handling potential errors.

Features:
- **Automated Login**: Logs in to the Sendcloud platform using predefined credentials.
- **Lazy Loading**: Scrolls through the page to load all order records dynamically.
- **Order Processing**: Processes each order, handles editing, and updates specific fields like discounts.
- **Error Handling**: Detects and logs errors encountered during order processing.
- **Error Storage**: Saves orders with errors to a JSON file for further review.

Prerequisites:
- **Python**: Ensure Python 3.6 or later is installed.
- **Selenium**: Install Selenium using `pip install selenium`.
- **ChromeDriver**: Download ChromeDriver compatible with your Chrome browser version. Update the `chrome_driver_path` variable in the script to point to the correct path.
- **Additional Libraries**: Ensure `logging` and `time` are available (built-in Python libraries).

Setup:
1. Clone this repository or download the script file.
2. Install the required libraries:
   ```bash
   pip install selenium

