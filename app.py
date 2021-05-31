'''
https://github.com/shekhargulati/flask-login-example/blob/master/flask-login-example.py
'''

from flask import Flask, Response, redirect, url_for, request, session, abort, url_for, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
import hashlib

app = Flask(__name__)


# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = '926e27eecdbc7a18858b3798ba99bddd'
    
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = '21232f297a57a5a743894a0e4a801fc3' # admin
        self.password = '6f507de48da41f024a19a92881b1494b' # Clave
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# identamos 1 usuario
users = User(1)

# some protected url
@app.route('/')
@login_required
def home():
    return Response('Acceso CONCEDIDO!!')
    # return render_template('home.html')

@app.route('/pagina1')
@login_required
def pagina1():
    return render_template('pagina1.html')

@app.route('/pagina2')
def pagina2():
    return render_template('pagina2.html')
 
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = encripta(request.form['username'])
        password = encripta(request.form['password'])
        print(username, password)
        if username == '21232f297a57a5a743894a0e4a801fc3' and password == '6f507de48da41f024a19a92881b1494b':
            # id = 1
            # print(username, password)
            session.permanet = False # Esta línea cierra la sesión una vez hayamos cerrado la pagina
            user = User(1)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return render_template('login.html')

# encriptamos en md5 lo que le pasemos
def encripta(dato):
    return hashlib.md5(dato.encode()).hexdigest()

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)
    

if __name__ == "__main__":
    app.run()