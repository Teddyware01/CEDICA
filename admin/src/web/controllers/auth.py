from flask import Blueprint
from flask import flash,render_template, redirect, url_for, request, session
from src.core import auth
from src.web.handlers.auth import login_required, check

from flask import current_app

bp = Blueprint("auth", __name__, url_prefix="/auth")




@bp.get("/")
def home():
    return render_template("auth/home.html")

@login_required
@bp.get("/pending_user")
def pending():
    user = auth.find_user_by_email(session.get("user"))
    return render_template("auth/user_accept_pending.html", user=user)

@bp.get("/login")
def login():
    return render_template("auth/login.html")

# redirect_uri = url_for('auth.callback', _external=True)
# return current_app.oauth.google.authorize_redirect(redirect_uri)
# redirect_uri = url_for('auth.callback', _external=True)

# token = google.authorize_access_token()

@bp.get("/google_authenticate")
def google_authenticate():
    google = current_app.oauth.google
    redirect_uri = url_for('auth.callback', _external=True)
    # prompt = "select_account", es para que el usuario elija la cuenta que quiere usar
    return google.authorize_redirect(redirect_uri, prompt="select_account") 


@bp.route('/login/callback')
def callback():
    google = current_app.oauth.google
    response = google.authorize_access_token()

    if response is None or response.get('access_token') is None:
        return 'Login failed.'
    # Tener el token guardado te permite realizar llamadas a las API de Google en nombre del usuario:
    session['google_token'] = (response['access_token'], '')
    me = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
        
    if me.status_code == 200:
        # Usa 'user_info' para procesar los datos del usuario como sea necesario
        user_info = me.json()

        nombre = user_info.get("given_name")
        apellido = user_info.get("family_name")
        email = user_info.get("email")

        user = auth.find_user_by_email(email)
        if not user:
            # Crea un nuevo usuario en la base de datos
            alias = f"{nombre}_{apellido}"
            user = auth.create_user(activo=False, is_google_auth=True,is_accept_pending=True, email=email, alias=alias)
        
        authenticate(email=email)


    # Here, 'me.data' contains user information.
    # You can perform registration process using this information if needed.
    return redirect(url_for('auth.home')) 

@bp.post("/authenticate")
def authenticate(email=None):
    if request.method == "POST":
        params = request.form
        email = params["email"]
        password = params["password"]
        user = auth.find_user_by_email_and_password(email,password)
    else:
        user = auth.find_user_by_email(email)

    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect(url_for("auth.login"))

    session["user"] = user.email

    flash("Sesion iniciada correctamente!", "success")
    if user.is_accept_pending:
        return redirect(url_for("auth.home"))
        
    return redirect(url_for("auth.home"))


@bp.get("/logout")
def logout():
    if session.get("google_token"):
        del session["google_token"]

    if session.get("user"):
        del session["user"]
        session.clear()
        flash("Sesion cerrada correctamente!", "info")
    else:
        flash("No hay una sesion activa!", "error")
    
    return redirect(url_for("auth.login"))
