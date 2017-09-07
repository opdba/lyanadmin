from .salt_https_api import salt_api_token

SALT_OPS_CONFIG = {
    'connect_type': '',  # http,
    'simple_service_url': '',
    'package_path': './static/scripts/',
    'salt_api_url': 'https://192.168.1.240:8888/',
    'salt_api_user': 'saltapi',
    'salt_api_password': 'saltapi'
}

def token_id():
    s = salt_api_token(
        {
            "username": SALT_OPS_CONFIG['salt_api_user'],
            "password": SALT_OPS_CONFIG['salt_api_password'],
            "eauth": "pam"
        },
        SALT_OPS_CONFIG['salt_api_url'] + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    print salt_token
    return salt_token
