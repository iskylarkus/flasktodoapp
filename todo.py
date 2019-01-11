from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////MMC/VSCode/TODO/todo.db'
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)
    #username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/")
def index():
    todos = ToDo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/todo/delete/<string:id>")
def todo_delete(id):
    todo = ToDo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/todo/edit/<string:id>")
def todo_edit(id):
    todo = ToDo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/todo/add", methods=["POST"])
def todo_add():
    title = request.form.get("title")
    new = ToDo(title=title, complete=False)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
