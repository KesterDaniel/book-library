from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-books-collection.db"
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False, unique=True)
    rating = db.Column(db.Float(250), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.title


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_dict = {
            "title": request.form["name"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        new_book = Book(title=book_dict['title'], author=book_dict['author'],
                        rating=book_dict['rating'])
        db.session.add(new_book)
        db.session.commit()

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
