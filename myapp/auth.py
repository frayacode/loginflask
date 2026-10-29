from urllib.parse import urlsplit
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from .extensions import db
from .models import User
from .forms import RegisterForm, LoginForm

bp = Blueprint("auth", __name__)


def is_safe_url(target):
    """Hanya izinkan redirect ke path internal (mencegah open redirect)."""
    if not target:
        return False
    parts = urlsplit(target)
    return (
        not parts.scheme
        and not parts.netloc
        and target.startswith("/")
        and not target.startswith("//")
    )


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registrasi berhasil! Silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.email == form.email.data.lower())
        )
        if user is None or not user.check_password(form.password.data):
            flash("Email atau password salah.", "danger")
            return render_template("login.html", form=form)

        login_user(user, remember=form.remember.data)
        flash(f"Selamat datang, {user.username}!", "success")

        next_page = request.args.get("next")
        if not is_safe_url(next_page):
            next_page = url_for("main.dashboard")
        return redirect(next_page)

    return render_template("login.html", form=form)


@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("Kamu sudah logout.", "info")
    return redirect(url_for("main.index"))
