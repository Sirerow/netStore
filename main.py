from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from DBase import DB
from UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, current_user, logout_user


app = Flask(__name__, static_folder="www/files", template_folder="www")
app.config["SECRET_KEY"]="iojoijoijoijjijjkjlbhyuglftdfyugf7y"
login_manager=LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromBD(user_id, DB())


@app.route("/")
@app.route("/index.html", methods=["GET","POST"])
def index():
    if request.method=="POST":
        userInDB = DB().getUser(request.form['login'], request.form['password'])
        if userInDB!=None:
            LM = UserLogin().createUser(DB().getUserByLogin(request.form["login"]))
            login_user(LM)
            return redirect("/main_page.html")
    return render_template("index.html")

@app.route("/main_page.html")
@app.route("/main_page.html", methods=["POST"])
@login_required
def main():
    if request.method=="POST":
        if "text" in request.form:
            current_u = UserLogin.get_user(current_user)
            print(current_u)
            DB().addReview(current_u[0], request.form["text"])
        if "id" in request.form:
            DB().deleteReview(request.form["id"])
    return render_template("main_page.html", reviews=DB().getAllReviews(), lens=len(DB().getAllReviews()))

@app.route("/exit.html")
@login_required
def exit():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port="5000", debug=True)