import os

from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import g, app
from flask import redirect


project_dir =dir, "bo os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_okdatabase.db"))

# initialize a flask application,
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
def get_db():
  global db
  if not db:
    db = SQLAlchemy(app)
  return db

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

#  this maps the main part of our application (/) to the home()
@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
    # load all of the books stored in our database
    books = Book.query.all()
    # tells Flask to look for the home.html file inside the templates directory
    return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    # gets the old and updated title from the form
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)