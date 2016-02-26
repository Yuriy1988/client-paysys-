import requests

url = 'https://api.sandbox.paypal.com/v1/payments/payment'
headers = {'Content-Type': 'application/json', 'Accept-Language': 'en_US', 'Authorization':'Bearer A101.WTIsjlE61K0DkovEOE1XwwN5qkX-VAMbW4xo0bDDYMUKj4nrOGSaQ7nhWxXBTDb-.ZmKcYOFKD0YcTD9GaE3c_9KjnH4'}
#header2 = 'Authorization: Bearer A101.WTIsjlE61K0DkovEOE1XwwN5qkX-VAMbW4xo0bDDYMUKj4nrOGSaQ7nhWxXBTDb-.ZmKcYOFKD0YcTD9GaE3c_9KjnH4'
post_data = '{ \
  "intent":"sale", \
  "payer":{ \
    "payment_method":"credit_card", \
    "funding_instruments":[ \
      { \
        "credit_card_token":{ \
          "credit_card_id":"CARD-3EV70752CK1507708K3HSAYA", \
          "payer_id":"user12345" \
        } \
      } \
    ] \
  }, \
  "transactions":[ \
    { \
      "amount":{ \
        "total":"6.70", \
        "currency":"USD" \
      }, \
      "description":"This is the payment transaction description." \
    } \
  ] \
}'



r = requests.get(url, headers=headers)

print(r)
