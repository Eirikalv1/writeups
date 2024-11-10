#!/usr/bin/env python

from flask import Flask, request, render_template, session, flash 
from flask_session_captcha import FlaskSessionCaptcha
from flask_session import Session
from stripe import PaymentIntent, Invoice
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
print(app.config["SECRET_KEY"])
app.config['CAPTCHA_LENGTH'] = 25
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config["CAPTCHA_SESSION_KEY"] = 'captcha_image'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)
captcha = FlaskSessionCaptcha(app) 

pizzas = [
    {
        "id": "01",
        "name": "THE SIMPLE",
        "description": "Only cheese and tomatosauce",
        "price": 14.9
    },
    {
        "id": "02",
        "name": "THE DREAM",
        "description": "Cheese, tomatosauce, minced meat and paprika",
        "price": 19.5
    },
    {
  "id": "03",
        "name": "MIX",
        "description": "Cheese, tomatosauce, pepperoni, onion and paprika",
        "price": 19.5
    },
    {
        "id": "04",
        "name": "OF SPECIAL",
        "description": "Milk",
        "price": 13.37
    },
    {
        "id": "05",
        "name": "THE NULL",
        "description": "Just the bread",
        "price": 19.5
    },
    {
        "id": "06",
        "name": "THE BOY",
        "description": "Cheese, tomatosauce, ham and bacon",
        "price": 19.5
    }
] 

@app.route('/', methods=['POST', 'GET']) 
def index():
    if 'user_type' not in session:
        session['user_type'] = 'private' # Organizations get their users from the PB-Organization, which is unavailable at the moment.
    if request.method == 'POST':
        amount = next((pizza for pizza in pizzas if pizza['id'] == request.form.get('selectedPizzaId', '01')), pizzas[0]).get('price')
        session[request.form.get('cardholder')] = {'card-number':request.form.get('cardNumber'),'expiration-date':request.form.get('expirationDate'), 'cvv':request.form.get('cvv')} # Saving credit card data for users
        print(session)
        if captcha.validate() == False:
            flash('Invalid captcha. Please try again.', 'danger')
        else:
            if session['user_type'] == 'private':
                payment_intent = PaymentIntent().create(
                    amount = amount,
                    currency = 'usd',
                    payment_method = 'card'
                )
                if payment_intent.succeeded:
                    flash('Pizza ordered. Flag = ' + os.getenv('FLAG', 'S2G{...}'), 'success')
                else:
                    flash('Payment method failed. Please try another.', 'danger')
            else:
                Invoice().create(customer='id') # Invoices are paid when the pizzas are delivered.
                flash("Pizza ordered. Flag = " + os.getenv('FLAG', 'S2G{...}'), 'success')
    return render_template("index.html", pizzas=pizzas) 
  
  
if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=1337) 

