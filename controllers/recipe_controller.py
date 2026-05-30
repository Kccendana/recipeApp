from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)
import os
from werkzeug.utils import secure_filename
from models.recipe_model import RecipeModel
from models.category_model import CategoryModel

# Blueprint for recipe-related routes
recipe_bp = Blueprint(
    "recipe",
    __name__
)

# Route to handle recipe creation
@recipe_bp.route("/recipes/add", methods=["POST"])
def add_recipe():

    # Ensure user is logged in
    if "user_id" not in session:
        return redirect("/login")

    # Extract form data
    title = request.form["title"]
    category_id = request.form["category_id"]
    description = request.form["description"]
    image = request.files["image"]

    image_url = None

    # Handle image upload if a file was provided
    if image and image.filename != "":

        filename = secure_filename(image.filename)

        filepath = os.path.join(
            "static/uploads",
            filename
        )

        image.save(filepath)
    image_url = filepath

    # Create recipe first
    recipe_id = RecipeModel.create_recipe(
        session["user_id"],
        category_id,
        title,
        description,
        image_url
    )

    # INGREDIENTS
    ingredient_names = request.form.getlist("ingredient_name[]")
    quantities = request.form.getlist("quantity[]")
    units = request.form.getlist("unit[]")

    for i in range(len(ingredient_names)):

        # strip() to remove extra whitespace, and check if name is not empty
        name = ingredient_names[i].strip()
        qty = quantities[i].strip() if quantities[i] else None
        unit = units[i].strip() if units[i] else None

        # Add ingredient if name is provided
        if name:
            RecipeModel.add_ingredient(
                recipe_id,
                name,
                qty,
                unit
            )

    # INSTRUCTIONS
    instructions = request.form.getlist("instructions[]")

    # Use step number starting from 1, and only add non-empty instructions
    step = 1
    for text in instructions:
        if text.strip():
            RecipeModel.add_instruction(recipe_id, step, text)
            step += 1

    flash("Recipe created successfully!", "success")

    return redirect("/dashboard")

# Route to handle recipe deletion
@recipe_bp.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):

    if "user_id" not in session:
        return redirect("/login")

    RecipeModel.delete_recipe(recipe_id)

    flash("Recipe deleted successfully.", "success")

    return redirect("/dashboard")

# Route to show edit form
@recipe_bp.route("/recipes/edit/<int:recipe_id>", methods=["GET"])
def edit_recipe(recipe_id):

    if "user_id" not in session:
        return redirect("/login")

    recipe = RecipeModel.get_by_id(recipe_id)
    ingredients = RecipeModel.get_ingredients(recipe_id)
    instructions = RecipeModel.get_instructions(recipe_id)
    categories = CategoryModel.get_all_categories()

    return render_template(
        "recipe_form.html",   # SAME FORM for add + edit
        recipe=recipe,
        ingredients=ingredients,
        instructions=instructions,
        categories=categories,
        is_edit=True
    )

@recipe_bp.route("/recipes/update/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):

    # Ensure user is logged in
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    category_id = request.form["category_id"]
    description = request.form["description"]
    instruction_ids = request.form.getlist("instruction_id[]")
    instructions = request.form.getlist("instructions[]")

    for i in range(len(instruction_ids)):

        ins_id = instruction_ids[i]
        text = instructions[i]

        if ins_id and text.strip() != "":
            RecipeModel.update_instruction(ins_id, text)

    RecipeModel.update_recipe(recipe_id, title, category_id, description)

    # delete old ingredients + instructions first
    RecipeModel.delete_ingredients(recipe_id)
    RecipeModel.delete_instructions(recipe_id)

    # re-insert new ones
    ingredient_names = request.form.getlist("ingredient_name[]")
    quantities = request.form.getlist("quantity[]")
    units = request.form.getlist("unit[]")

    instructions = request.form.getlist("instructions[]")

    for i in range(len(ingredient_names)):
        RecipeModel.add_ingredient(
            recipe_id,
            ingredient_names[i],
            quantities[i],
            units[i]
        )

    step = 1
    for text in instructions:
        RecipeModel.add_instruction(recipe_id, step, text)
        step += 1

    flash("Recipe updated successfully!", "success")

    return redirect("/dashboard")