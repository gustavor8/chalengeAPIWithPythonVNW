from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Only required the first time you run the app
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        category TEXT NOT NULL,
                        author TEXT NOT NULL,
                        image_url TEXT NOT NULL
                        )''')  
        print("Banco de dados inicializado com sucesso!!!")

init_db()

# Homepage
@app.route('/')
def home():
    return '<h1>Bem-vindo a API do desafio Vai Na Web, espero que consiga utilizar com sabedoria! </h1>'

# Get books
@app.route('/books', methods=['GET'])
def get_books():
  with sqlite3.connect('database.db') as conn:
    books = conn.execute('''SELECT * FROM books''').fetchall()  
  formated_books = []  
  for book in books:
    dic_books = {
      'id': book[0],
      'title': book[1],
      'category': book[2],
      'author': book[3],
      'image_url': book[4]
    }
    formated_books.append(dic_books)
  
  
  return jsonify(formated_books), 200

# Donate Books
@app.route('/donate', methods=['POST'])
def donate():
  data = request.get_json()
  if not data:
    return jsonify({'error': 'JSON inválido ou ausente!'}), 400

  title = data.get('title')
  category = data.get('category')
  author = data.get('author')
  image_url = data.get('image_url')

  if not all ([title, category, author, image_url]):
    return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400
  
  with sqlite3.connect('database.db') as conn:
    conn.execute('''INSERT INTO books (title, category, author, image_url) VALUES (?,?,?,?)''', (title, category, author, image_url))
    conn.commit()
    return jsonify({'message': 'Livro doado com sucesso'}), 201



if __name__ == '__main__':
    app.run(debug=True)