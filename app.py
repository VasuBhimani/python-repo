from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key_here'

# Predefined password for authentication
PASSWORD = 'test222'

# Path to the data folder
data_folder = os.path.join(os.getcwd(), 'data')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Incorrect password", 403
    return render_template('login.html')

@app.before_request
def require_login():
    if not session.get('logged_in') and request.endpoint not in ['login', 'static']:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    # List all text files in the data folder
    files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
    return render_template('index.html', files=files)

@app.route('/view/<filename>')
def view_file(filename):
    # Read the content of the selected file
    file_path = os.path.join(data_folder, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return render_template('view.html', filename=filename, content=content)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
