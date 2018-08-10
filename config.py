import os

Config = {
    'appClientId': os.getenv('appClientId', '8e8b7ef3bcacedc0ff84ad2f54485c84'),
    'appClientSecret': os.getenv('appClientSecret', ''),
    'callback': os.getenv('callback', 'http://ali.wusisu.com:8080/login/callback'),
    'isEnterprise': os.getenv('isEnterprise', 'True') == 'True',
    'enterpriseName': os.getenv('enterpriseName', 'codingcorp'),
    'staticRoot': os.getenv('staticRoot', 'static'),
}
