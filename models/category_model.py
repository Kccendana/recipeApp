from config.database import get_db


class CategoryModel:

    @staticmethod
    def get_all_categories():

        conn = get_db()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT *
            FROM categories
            ORDER BY category_name
        """)

        categories = cursor.fetchall()

        conn.close()

        return categories