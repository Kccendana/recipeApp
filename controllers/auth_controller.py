from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)
# Added imports for file handling and security
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Import models
from models.user_model import UserModel
from models.category_model import CategoryModel
from models.recipe_model import RecipeModel
auth_bp = Blueprint(
    "auth",
    __name__
)

# Registration route
@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)

def register():
    # Prevent logged-in users from registering again
    if "user_id" in session:
        return redirect("/dashboard")

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = UserModel.get_user_by_email(
            email
        )

        if existing_user:

            flash(
                 "This email is already registered. Please log in instead.",
        "error"
            )

            return redirect("/login")

        password_hash = generate_password_hash(
            password
        )

        UserModel.create_user(
            username,
            email,
            password_hash
        )

        flash(
            "Registration successful! Please log in.",
            "success"
        )

        return redirect("/login")

    return render_template(
        "register.html"
    )

# Login route
@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # Prevent logged-in users from accessing login page
    if "user_id" in session:
        return redirect("/dashboard")

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = UserModel.get_user_by_email(
            email
        )

        if user and check_password_hash(
            user["password_hash"],
            password
        ):

            session["user_id"] = user["user_id"]
            session["username"] = user["username"]

            flash(
                f"Welcome, {user['username']}!",
                "success"
            )

            return redirect(
                "/dashboard"
            )

        flash(
            "Invalid email or password. Please use a registered account.",
            "error"
        )

        return redirect("/login")

    return render_template(
        "login.html"
    )

# Dashboard route
@auth_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please log in first.", "error")
        return redirect("/login")

    search = request.args.get("search", "")
    category_id = request.args.get("category_id", "")

    categories = CategoryModel.get_all_categories()

    recipes = RecipeModel.get_filtered_by_user(
        session["user_id"],
        search,
        category_id
    )

    return render_template(
        "dashboard.html",
        categories=categories,
        recipes=recipes
    )

# Logout route
@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect("/login")