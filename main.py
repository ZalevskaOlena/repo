from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, primary_key=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/welcome', methods=['POST','GET'])
def index():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        article = Article(username=username,email=email,password=password)

        try:
            db.session.add(article)
            db.session.commit()
            return "Успіх!"
        except:
            return "Виникла помилка!"
    else:
        return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug = True)
