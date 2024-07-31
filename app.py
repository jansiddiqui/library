# app.py
import os
from flask_frozen import Freezer
from flask import Flask, render_template, request, redirect, url_for
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email settings
EMAIL_ADDRESS = 'couragelibrary07@gmail.com'
EMAIL_PASSWORD = '@COURAGE9786@'
TO_EMAIL = 'couragelibrary07@gmail.com'

def send_email(form_data):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = 'New Course Registration'
    
    body = f"New registration received:\n\nName: {form_data['name']}\nEmail: {form_data['email']}\nPhone: {form_data['phone']}\nSlot Duration: {form_data['duration']} hours\nSlot Time: {form_data['slot']}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_slot')
def select_slot():
    return render_template('slots.html')

@app.route('/take_course', methods=['GET', 'POST'])
def take_course():
    if request.method == 'POST':
        form_data = request.form.to_dict()

        # Save data to JSON file
        with open('course_data.json', 'a') as f:
            f.write(json.dumps(form_data) + "\n")

        # Send notification email
        send_email(form_data)

        return redirect(url_for('index'))
    
    duration = request.args.get('duration', '')
    slot = request.args.get('slot', '')
    return render_template('form.html', duration=duration, slot=slot)

@app.route('/admin')
def admin():
    registrations = []
    try:
        with open('course_data.json', 'r') as f:
            registrations = [json.loads(line) for line in f]
    except FileNotFoundError:
        pass
    return render_template('admin.html', registrations=registrations)

if __name__ == '__main__':
    app.run(debug=True)
