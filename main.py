from flask import Flask, render_template, request, redirect,url_for,flash
from flask_mail import Mail,Message
import random
import string

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp@gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USERNAME']='your_email@gmail.com'
app.config['MAIL_PASSWORD']='your_password'
app.config['SECRET_KEY']='your_secret_key'

mail=Mail(app)

def generate_otp():
    return ''.join(random.choices(string.digits,k=6))

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        email=request.form['email']
        otp=generate_otp()

        msg=Message('Your OTP for email verification',
                    sender='your_email@gmail.com',
                    recipients=[email])
        msg.body=f'Your OTP is {otp}. Please use it to verify your email.'
        try:
            mail.send(msg)
            flash(f'OTP sent to {email}.','success')
            return redirect(url_for('verify',otp=otp, email=email))
        except Exception as e:
            flash(f'Failed to send OTP. Error: {e}','error')

    return render_template('index.html')

@app.route('/verify',methods=['GET','POST'])
def verify():
    otp=request.args.get('otp')
    email=request.args.get('email')

    if request.method=='POST':
        entered_otp=request.form('otp')

        if entered_otp==otp:
            flash('Email verified successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid OTP, please try again ','error')

    return render_template('verify.html',email=email)

if __name__ == '__main___':
    app.run(debug=True)