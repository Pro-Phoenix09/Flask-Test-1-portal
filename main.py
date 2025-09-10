from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "qwerrrteytyutyusdfsf"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:2009@localhost/reg_users_portal"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class LoginCreds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(225), nullable=False)


@app.route("/")
def Home():

    if "user" not in session:
        return redirect(url_for("Login"))    
    
    return render_template("home.html", loggeduser=session["user"])


@app.route("/login", methods=["GET", "POST"])
def Login():
    alert_msg = None

    if "user" in session:
        return redirect(url_for("Home"))

    if request.method == "POST":
        username = request.form["enteredusername"]
        password = request.form["enteredpassword"]
        
        users = LoginCreds.query.filter(LoginCreds.name.ilike(username)).first()
        if users:
            print('user exists', users.name)
            passwordcorrect = check_password_hash(users.password, password)
            if passwordcorrect:
                print('correct password', users.password)
                session["user"] = users.name

                return redirect(url_for("Home"))

            else:
                alert_msg = "Incorrect Password"

        else:
            alert_msg = "Couldnt Find User"
            
    return render_template("login.html", alert=alert_msg)

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("Login"))  


if __name__ == "__main__":
    app.run(debug=True)