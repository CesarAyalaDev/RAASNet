#!/usr/bin/env python3
"""
Installation:
pip3 install pyotp pyqrcode pypng requests
"""

import pyotp, pyqrcode, png, getpass, hashlib, requests, sys
from pyqrcode import QRCode

def otp_setup(u, pw):
    check_pwd = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    payload = {'user': u, 'pwd': check_pwd}

    r = requests.post('https://zeznzo.nl/login.py', data=payload)
    if r.status_code == 200:
        if r.text.startswith('[ERROR]'):
            print(r.text.split('[ERROR] ')[1])
            return
        elif r.text.startswith('[OK]'):
            print('Welcome!\n\nSetup will now start...')
            pass

    otp_id = pyotp.random_base32()
    print('[SECRET] %s' % otp_id)

    totp_uri = pyotp.totp.TOTP(otp_id).provisioning_uri(u, issuer_name="RAASNet")
    print(totp_uri)

    try:
        payload = {'user': u, 'pwd': hashlib.sha256(pw.encode('utf-8')).hexdigest(), 'otp_id' : otp_id}

        r = requests.post('https://zeznzo.nl/otp_setup.py', data=payload)
        if r.status_code == 200:
            if r.text.startswith('[ERROR]'):
                print(r.text.split('[ERROR] ')[1])
                sys.exit(0)
            else:
                print('[SUCCESS] OTP setup completed!')

        else:
            print('[ERROR] Failed to setup OTP!\n%i' % r.status_code)
            return

    except Exception as e:
        print('ERROR %s' % e)
        return

    s = totp_uri
    url = pyqrcode.create(s)
    url.png('./my_otp_qr.png', scale = 6)

    input('\nScan the QR-code in ./my_otp_qr.png with Google Authenticator.\n\nPRESS ANY KEY TO EXIT.')
    sys.exit(0)

print('''
NOTE:
You can only use this script ONCE to set it up.

If you need a reset, contact: raasnet@protonmail.com

''')

u = input('[Username] ')
pw = getpass.getpass('[Password] ')

otp_setup(u, pw)
