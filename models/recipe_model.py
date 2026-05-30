from config.database import get_db


class RecipeModel:

    @staticmethod
    def create_recipe(
        user_id,
        category_id,
        title,
        description,
        image_url
    ):

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO recipes
            (
                user_id,
                category_id,
                title,
                description,
                image_url
            )
            VALUES
            (%s, %s, %s, %s, %s)
        """, (
            user_id,
            category_id,
            title,
            description,
            image_url
        ))

        recipe_id = cursor.lastrowid

        conn.commit()
        conn.close()
        

        return recipe_id
    
    @staticmethod
    def add_instruction(recipe_id, step_number, instruction_text):

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO recipe_instructions
            (
                recipe_id,
                step_number,
                instruction_text
            )
            VALUES (%s, %s, %s)
        """, (
            recipe_id,
            step_number,
            instruction_text
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def add_ingredient(recipe_id, ingredient_name, quantity, unit):

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO recipe_ingredients
            (
                recipe_id,
                ingredient_name,
                quantity,
                unit
            )
            VALUES (%s, %s, %s, %s)
        """, (
            recipe_id,
            ingredient_name,
            quantity,
            unit
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_by_user(user_id):

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                r.recipe_id,
                r.title,
                r.description,
                r.image_url,
                r.created_at,
                c.category_name
            FROM recipes r
            JOIN categories c ON r.category_id = c.category_id
            WHERE r.user_id = %s
            ORDER BY r.created_at DESC
        """, (user_id,))

        recipes = cursor.fetchall()
        conn.close()

        return recipes  


    @staticmethod
    def delete_recipe(recipe_id):

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM recipes
            WHERE recipe_id = %s
        """, (recipe_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(recipe_id):

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM recipes
            WHERE recipe_id = %s
        """, (recipe_id,))

        recipe = cursor.fetchone()

        conn.close()
        return recipe 
    
    @staticmethod
    def update_recipe(recipe_id, title, category_id, description):

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE recipes
            SET title = %s,
                category_id = %s,
                description = %s
            WHERE recipe_id = %s
        """, (title, category_id, description, recipe_id))

        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_ingredients(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id=%s", (recipe_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_instructions(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipe_instructions WHERE recipe_id=%s", (recipe_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_ingredients(recipe_id):

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM recipe_ingredients
            WHERE recipe_id = %s
        """, (recipe_id,))

        ingredients = cursor.fetchall()
        conn.close()

        return ingredients
    
    @staticmethod
    def get_instructions(recipe_id):

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM recipe_instructions
            WHERE recipe_id = %s
            ORDER BY step_number ASC
        """, (recipe_id,))

        instructions = cursor.fetchall()
        conn.close()
       
        return instructions
    
    # update instructions
    @staticmethod
    def update_instruction(instruction_id, instruction_text, step_number=None):

        conn = get_db()
        cursor = conn.cursor()

        if step_number is not None:
            cursor.execute("""
                UPDATE recipe_instructions
                SET instruction_text = %s,
                    step_number = %s
                WHERE instruction_id = %s
            """, (instruction_text, step_number, instruction_id))
        else:
            cursor.execute("""
                UPDATE recipe_instructions
                SET instruction_text = %s
                WHERE instruction_id = %s
            """, (instruction_text, instruction_id))

        conn.commit()
        conn.close()
    
    # search recipes by title or description
    @staticmethod
    def get_filtered_by_user(user_id, search="", category_id=""):

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT r.*, c.category_name
            FROM recipes r
            LEFT JOIN categories c ON r.category_id = c.category_id
            WHERE r.user_id = %s
        """

        params = [user_id]

        if search:
            query += " AND r.title LIKE %s"
            params.append(f"%{search}%")

        if category_id:
            query += " AND r.category_id = %s"
            params.append(category_id)

        cursor.execute(query, tuple(params))
        recipes = cursor.fetchall()

        conn.close()
        return recipes