from config.database import get_db


class UserModel:

    @staticmethod
    def create_user(
        username,
        email,
        password_hash
    ):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (
                username,
                email,
                password_hash
            )
            VALUES
            (%s, %s, %s)
        """, (
            username,
            email,
            password_hash
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_email(email):

        conn = get_db()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email = %s
        """, (email,))

        user = cursor.fetchone()

        conn.close()

        return user