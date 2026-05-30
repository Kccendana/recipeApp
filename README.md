# Overview

This project is a full-stack web application designed to strengthen my skills as a software engineer in building scalable CRUD systems using Flask, MVC architecture, and relational databases. The goal is to create a real-world recipe management system where users can register, log in, and manage their own recipes with ingredients, instructions, and categories.

The application integrates a SQL relational database (MySQL) to store and manage structured data efficiently. It uses multiple related tables including users, recipes, categories, ingredients, and instructions to demonstrate proper database normalization and relationships such as one-to-many relationships.

Users can:
- Register and log in securely
- Create, edit, and delete recipes
- Add multiple ingredients and instructions per recipe
- Categorize recipes for better organization
- Upload images for recipes
- Search and filter recipes

The purpose of this software is to simulate a real-world recipe management system while improving my understanding of backend development, database design, authentication, and MVC architecture.

[Software Demo Video](http://youtube.link.goes.here)

---

# Relational Database

This project uses a MySQL relational database to store all application data. The database is designed following normalization principles to ensure data consistency and avoid redundancy.

The main tables include:

- **users**
  - user_id (PK)
  - username
  - email
  - password_hash

- **recipes**
  - recipe_id (PK)
  - user_id (FK)
  - category_id (FK)
  - title
  - description
  - image_url
  - created_at

- **categories**
  - category_id (PK)
  - category_name

- **recipe_ingredients**
  - ingredient_id (PK)
  - recipe_id (FK)
  - ingredient_name
  - quantity
  - unit

- **recipe_instructions**
  - instruction_id (PK)
  - recipe_id (FK)
  - step_number
  - instruction_text

Relationships:
- One user can create many recipes
- One recipe belongs to one category
- One recipe has many ingredients
- One recipe has many instructions

---

# Development Environment

The application was developed using:

- Visual Studio Code
- MySQL Server (XAMPP / local MySQL)
- Flask (Python web framework)
- Jinja2 templating engine
- Tailwind CSS for frontend styling
- Git & GitHub for version control

Programming Language:
- Python (backend logic)
- HTML, CSS (Tailwind), JavaScript (frontend interactivity)
- SQL (database queries)

Libraries used:
- Flask
- mysql-connector-python
- Werkzeug (for password hashing)

---

# Useful Websites

These resources were helpful during development:

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [W3Schools SQL Tutorial](https://www.w3schools.com/sql/)
- [Stack Overflow](https://stackoverflow.com/)

---

# Future Work

Future improvements planned for this project include:

- Improve UI with a modern responsive dashboard layout
- Add drag-and-drop ordering for instructions
- Implement recipe sharing between users
- Add password reset functionality
- Improve search with ingredient-based filtering
- Deploy application to a cloud platform with CI/CD pipeline