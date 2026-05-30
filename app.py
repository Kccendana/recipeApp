from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

from dotenv import load_dotenv
import os

load_dotenv()

from controllers.auth_controller import auth_bp
from controllers.recipe_controller import (
    recipe_bp
)

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
# Set the upload folder for recipe images
app.config["UPLOAD_FOLDER"] = "static/uploads"

@app.route("/")
def home():

    if "user_id" in session:
        return redirect("/dashboard")

    return redirect("/login")

app.register_blueprint(auth_bp)

app.register_blueprint(
    recipe_bp
)
if __name__ == "__main__":
    app.run(debug=True)