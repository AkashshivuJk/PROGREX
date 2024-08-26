from flask import Flask, request, redirect, url_for, render_template, session
import csv
import os

app = Flask(__name__)
app.secret_key = 'asrj'
CSV_FILE = 'users.csv'
updatepro = []
def read_progress():
    if not os.path.exists('progress.csv'):
        return {}
    progress = {}
    with open('progress.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            progress[row['subject']] = {
                'module1': int(row['module1']),
                'module2': int(row['module2']),
                'module3': int(row['module3']),
                'module4': int(row['module4']),
                'module5': int(row['module5']),
            }
    return progress

def write_progress(progress):
    with open('progress.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['subject', 'module1', 'module2', 'module3', 'module4', 'module5'])
        writer.writeheader()
        for subject, modules in progress.items():
            row = {'subject': subject}
            row.update(modules)
            writer.writerow(row)

def calculate_completion_percentage(subject_progress):
    completed_modules = sum(subject_progress.values())
    total_modules = len(subject_progress)
    return (completed_modules / total_modules) * 100


def read_users():
    if not os.path.exists(CSV_FILE):
        return []
    users = []
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users

def write_user(user):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'email', 'password'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(user)

@app.route('/')
@app.route('/')
def home():
    if 'email' in session:
        if session['email'] == 'admin@dsatm.edu.in':
            return redirect(url_for('admin'))
        progress = read_progress()

        completion_percentages = {subject: calculate_completion_percentage(progress[subject]) for subject in progress}
        return render_template('homepage.html', name=session['name'], progress=completion_percentages)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Attempting login with email: {email} and password: {password}")
        users = read_users()
        print(f"Current users: {users}")
        for user in users:
            if 'email' not in user or 'password' not in user:
                print(f"Malformed user record: {user}")
                continue
            if user['email'] == email:
                if user['password'] == password:
                    session['email'] = email
                    session['name'] = user['name']
                    if email == 'admin@dsatm.edu.in':
                        return redirect(url_for('admin'))
                    return redirect(url_for('home'))
                else:
                    return "Invalid password"
        return "Email not found"
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    print(f"Attempting signup with name: {name}, email: {email}, and password: {password}")
    users = read_users()
    print(f"Current users: {users}")
    for user in users:
        if user['email'] == email:
            return "Email already exists"
    write_user({'name': name, 'email': email, 'password': password})
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'email' in session and session['email'] == 'admin@dsatm.edu.in':
        return render_template('admin.html')
    return redirect(url_for('login'))

@app.route('/homee')
def homee():
    progress = read_progress()
    completion_percentages = {subject: calculate_completion_percentage(progress[subject]) for subject in progress}
    return render_template('homepage.html', name=session['name'], progress=completion_percentages)

@app.route('/notes')
def notes_page():
    return render_template('notes.html')

@app.route('/playlist')
def playlist_page():
    return render_template('playlist.html')

@app.route('/portfolio')
def portfolio_page():
    return render_template('portfolio.html')

@app.route('/events')
def events_page():
    return render_template('events.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/ada')
def ada_page():
    return render_template('ada.html')

@app.route('/dbms')
def dbms_page():
    return render_template('dbms.html')

@app.route('/ot')
def ot_page():
    return render_template('ot.html')

@app.route('/bio')
def bio_page():
    return render_template('bio.html')

@app.route('/cgv')
def cgv_page():
    return render_template('cgv.html')

@app.route('/uhv')
def uhv_page():
    return render_template('uhv.html')

    

@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.json
    subject = data['subject']
    module = data['module']
    checked = data['checked']

    progress = read_progress()
    if subject not in progress:
        progress[subject] = {'module1': 0, 'module2': 0, 'module3': 0, 'module4': 0, 'module5': 0}
    progress[subject][module] = checked
    write_progress(progress)
    return '', 204


if __name__ == '__main__':
    app.run(debug=True,port=8080)
