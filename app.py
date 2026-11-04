from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
# Use the provided DB_CONNECTION_STRING environment variable, or SQLite as fallback
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING') or 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Fetch all tasks from database and display them."""
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    """Receive a new task from form, save it to database, and redirect back to /."""
    task_title = request.form.get('title')
    if task_title:
        new_task = Task(title=task_title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)