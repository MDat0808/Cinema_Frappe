import paypalrestsdk

def init_paypal():
    paypalrestsdk.configure({
        "mode": "sandbox", 
        "client_id": "ATFcfC3YxWt7vmFQrQicS4GOG8Kjjd8l86lOdwEQl5xL1JuyZwMGLOhAnQOFJi28jMMBJeaV2ttK-gJ8",
        "client_secret": "EG06qZucDibdAMbE3OSkWXUIead51KriOqqdPtxXUO-owPHoF6EAi45JdpI0CEsxYB3RzLt1oucxcDxR"
    })
