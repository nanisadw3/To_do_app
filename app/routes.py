from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Todo
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@main.route("/add", methods=["POST"])
def add():
    todo_text = request.form.get("todo_text")
    if todo_text:
        new_todo = Todo(text=todo_text)
        db.session.add(new_todo)
        db.session.commit()
        flash("¡Tarea añadida con éxito!", "success")
    else:
        flash("El texto de la tarea no puede estar vacío.", "error")
    return redirect(url_for("main.index"))


@main.route("/toggle/<int:id>")
def toggle(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete
    db.session.commit()
    flash(f"Tarea '{todo.text}' actualizada.", "success")
    return redirect(url_for("main.index"))


@main.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"Tarea '{todo.text}' eliminada.", "success")
    return redirect(url_for("main.index"))
