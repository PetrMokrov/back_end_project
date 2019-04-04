from itsdangerous import URLSafeTimedSerializer

from web_app import app

expiration_time = 3600 #TODO: it should be config parameter


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_SIGN_MSG_KEY'])
    return serializer.dumps(email)


def confirm_token(token, expiration=expiration_time):
    serializer = URLSafeTimedSerializer(app.config['SECRET_SIGN_MSG_KEY'])
    try:
        email = serializer.loads(
            token,
            max_age=expiration
        )
    except:
        return False
    return email