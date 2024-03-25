from flask import Flask, render_template, request, jsonify
from models.User import db, Article
from flask_restful import Api
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
api = Api(app)
db.init_app(app)
headers = {'Content-Type': 'application/json'}


@app.route('/welcome', methods=['GET'])
def indexget():
    return render_template('welcome.html')


@app.route('/welcome', methods=['POST'])
def indexpost():
    if request.method == "POST":

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        data = {
            'username': username,
            'email': email,
            'password': password
        }

        url = 'http://127.0.0.1:5000/welcome/jsonn'
        response = requests.post(url, json=data)
        print(response.text)

        article = Article(username=username, email=email, password=password)

        try:
            db.session.add(article)
            db.session.commit()
            return "Успіх!"
        except Exception as e:
            return f"Виникла помилка! {str(e)}"
    else:
        return render_template('welcome.html'), jsonify({"message": "Успішно"})


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Article.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    else:
        return jsonify({'error': 'Користувача з таким id нема'}), 404


@app.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Article.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Видалено'}), 200
    else:
        return jsonify({'error': 'Користувача по id нема'}), 404


@app.route('/welcome/jsonn', methods=['POST'])
def json_post():
    data = request.json
    if data:
        print(data)
        return jsonify({"message": "супер"}), 200
    else:
        return jsonify({"message": "не супер"}), 400


if __name__ == '__main__':
    app.run(debug=True)
