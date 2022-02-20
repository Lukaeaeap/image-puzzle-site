from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    print("ÿeet")
    return render_template("home.html", debug=True)
