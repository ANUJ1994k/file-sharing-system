from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Backend API endpoint
API_URL = 'http://localhost:5000/api'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        response = requests.post(f'{API_URL}/login', json=data)
        if response.status_code == 200:
            session['token'] = response.json()['token']
            return redirect('/dashboard')
        return "Login Failed"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'role': 'client'  # or 'ops'
        }
        response = requests.post(f'{API_URL}/signup', json=data)
        if response.status_code == 200:
            return redirect('/login')
        return "Signup Failed"
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        token = session.get('token')
        if token:
            files = {'file': file}
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(f'{API_URL}/upload', files=files, headers=headers)
            return "File Uploaded" if response.status_code == 200 else "Upload Failed"
    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
