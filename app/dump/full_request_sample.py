import requests, json

# GETTING PAYPAL ACCESS TOKEN
url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en_US'
}

username = 'AZrccVcbcXX1BpSsTTIioUdmvL2PLwznBTkwDFEcfORpz4i_BhE6FPwiQZRfa4RD0kepGAXF5oAWoY71'
password = 'EEigCPS468DFBtGYmL3WdOscFxd6O7fxOObEI8ebX3uave3flC9iXzjymdNZUli0Y3HOKRSz8WLwIejf'
auth = (username, password)

data = {'grant_type': 'client_credentials'}

r = requests.post(url, headers=headers, auth=auth, data=data)

#print(r.status_code)
#print(r.text)
print('Getting auth token status code: %s' % r.status_code)

r_dict = json.loads(r.text)

access_token = r_dict['access_token']
token_type = r_dict['token_type']

#print(access_token)
#print(token_type)

# REGISTERING USER'S CARD:
url = 'https://api.sandbox.paypal.com/v1/vault/credit-card'
headers = {
    'Content-Type': 'application/json',
    'Authorization': '{token_type} {access_token}'.format(token_type=token_type, access_token=access_token)
}

# Dumping card info to JSON:
payer_id = 'user12345'
card_type = 'visa'
card_number = '4417119669820331'
card_expire_month = '11'
card_expire_year = '2018'
card_first_name = 'Joe'
card_last_name = 'Shopper'
data = json.dumps(
    {
        "payer_id":payer_id,
         "type":card_type,
         "number":card_number,
         "expire_month":card_expire_month,
         "expire_year":card_expire_year,
         "first_name":card_first_name,
         "last_name":card_last_name
    }
)

r = requests.post(url, headers=headers, data=data)

#print(data)
print('Registering a card status code: %s' % r.status_code)
#print(r.text)

# Getting a Card ID and Payer ID:
r_dict = json.loads(r.text)

card_id = r_dict['id']
payer_id = r_dict['payer_id']

# USE A STORED CARD -- CREATING A PAYMENT:
url = 'https://api.sandbox.paypal.com/v1/payments/payment'

headers = {
    'Content-Type': 'application/json',
    'Authorization': '{token_type} {access_token}'.format(token_type=token_type, access_token=access_token)
}

payment_intent = 'sale'
payment_method = 'credit_card'
amount_total = '6.70'
amount_currency = 'USD'
payment_description = 'This is the payment description.'
data = json.dumps(
    {
        'intent':payment_intent,
        'payer':{
            'payment_method':payment_method,
            'funding_instruments':[
                {
                    'credit_card_token':{
                        'credit_card_id':card_id,
                        'payer_id':payer_id
                    }
                }
            ]
        },
        'transactions':[
            {
                'amount':{
                    'total':amount_total,
                    'currency':amount_currency
                },
                'description':payment_description
            }
        ]
    }, sort_keys=True
)

r = requests.post(url, headers=headers, data=data)


print('Creating a payment status code: %s' % r.status_code)
print(r.text)