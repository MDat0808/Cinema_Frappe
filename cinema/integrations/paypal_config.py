import paypalrestsdk

def init_paypal():
    paypalrestsdk.configure({
        "mode": "sandbox", 
        "client_id": "",
        "client_secret": ""
    })
