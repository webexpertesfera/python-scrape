from flask import Flask, render_template, request, jsonify
import subprocess
import logging
import os
import json
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to execute the Selenium script
@app.route('/start-script', methods=['POST'])
def start_script():
    try:
        file_path = 'orders_with_errors.json'
        
        # Clear the old data from the JSON file
        if os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write('{}')  # Write an empty JSON object to clear the file
            logging.info("Cleared old data from orders_with_errors.json.")
        else:
            logging.warning("File not found: orders_with_errors.json. A new file will be created.")
        
        # Execute the Selenium script
        result = subprocess.run(['python3', 'selenium_script.py'], capture_output=True, text=True)
        logging.info("Selenium script executed.")
        
        # Check and read the file content after script execution
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                file_content = json.load(file)  # Read file content
        else:
            logging.error("File not found: orders_with_errors.json")
            return jsonify({"status": "error", "message": "orders_with_errors.json not found."}), 404

        return jsonify({"status": "success", "output": result.stdout, "fileContent": file_content}), 200

    except Exception as e:
        logging.error(f"Error executing script: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True)