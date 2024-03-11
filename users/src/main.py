from flask import Response, session, abort
from flask_swagger_ui import get_swaggerui_blueprint
from apiflask import APIFlask
from flask_session import Session
from hashlib import md5
from datetime import timedelta
from os import environ

from db.models import User
from db.session import DBSession
from schema import UserAuthData, UserProfileData, AuthResponseHeaders

SESSION_LIFETIME = timedelta(minutes=60)

app = APIFlask(__name__, spec_path='/spec', title='Users')

app.secret_key = 'SECRET_KEY'
app.config['SPEC_FORMAT'] = 'yaml'
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = 'openapi.yaml'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PERMANENT_SESSION_LIFETIME'] =  SESSION_LIFETIME
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('USERS_DB_URL')

Session(app)

swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/spec', config={'app_name': 'Users service'})
app.register_blueprint(swaggerui_blueprint)


@app.post("/signup")
@app.input(UserAuthData)
@app.doc(responses={
    200: {'description': 'User registered successfully'},
    409: {'description': 'User is already registered'}
})
def signup(json_data):
    """
    User registration in the system
    
    Username and password should be provided in the request JSON
    """
    username = json_data.get('username')
    password = json_data.get('password')

    with DBSession.begin() as sess:
        if sess.query(User).filter_by(username=username).count():
            abort(Response('User with that username is already registered!', 409))
        
        password_hash = md5(password.encode()).hexdigest().encode()
        user = User(username=username, password_hash=password_hash)

        sess.add(user)

    return Response(status=200)


@app.route("/signin", methods=['POST'])
@app.input(UserAuthData)
@app.output({}, headers=AuthResponseHeaders)
def signin(json_data):
    """
    User authorithation in the system
    
    Username and password should be provided in the request JSON. Auth-Session is created
    """
    username = json_data.get('username')
    password = json_data.get('password')

    if not username or not password:
        abort(400)

    with DBSession() as sess:
        user = sess.query(User).filter_by(username=username).one_or_none()
        if not user:
            abort(Response('User not found!', 404))
        
        password_hash = md5(password.encode()).hexdigest().encode()
        
        if user.password_hash != password_hash:
            abort(Response('Invalid password', 401))

        session['user-id'] = user.id

        sess.add(user)

    return Response(status=200)


@app.route("/update-profile", methods=['POST'])
@app.input(UserProfileData)
@app.doc(responses={
    200: {'description': 'User registered successfully'},
    401: {'description': 'Invalid session'}
})
def update_profile(json_data):
    """
    Change User profile data
    
    JSON including some of the following fields (first_name, second_name, birth_date, email, phone) should be provided
    """
    user_id = session.get('user-id')

    if not user_id:
        abort(401)

    with DBSession.begin() as sess:
        user: User = sess.query(User).get(user_id)

        user.update(**json_data)

        sess.add(user)

    return Response(status=200)


app.run(host=environ.get('USERS_SERVER_HOST', '0.0.0.0'), port=environ.get('USERS_SERVER_PORT', 8080))
