from main import app, db, LoginCreds
from werkzeug.security import generate_password_hash

while True:
    username = input("Enter Name : ")
    if username == "":
        break

    pswd = input('Enter Password : ')

    hashed_password = generate_password_hash(pswd)
    print(username, hashed_password)

    with app.app_context():
        new_user = LoginCreds(name=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()