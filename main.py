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
        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    book_id = request.args.get("book_id")
    book_to_update = Book.query.filter_by(id=book_id).first()
    if request.method == "GET":
        return render_template("edit_rating.html", book=book_to_update)
    else:
        book = Book.query.get(book_id)
        book.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
