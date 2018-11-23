from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from user import User, UserRegister
from book import Book, BookList

import uuid
import pdb;
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '12321'
cors = CORS(app, resources={r"*":{"origins": "*"}})
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Book, '/book/<string:title>')
api.add_resource(BookList, '/books')
api.add_resource(UserRegister, '/register')

# def remove_book(book_id):
#     #[BOOKS.remove(book) for book in BOOKS if book['id'] == book_id]
#
#     for book in BOOKS:
#         if book['id'] == book_id:
#             BOOKS.remove(book)
#             return true
#         return False
#
#
# @app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
# def single_book(book_id):
#     response_object = {'status':'success'}
#     if request.method == 'PUT':
#         post_data = request.get_json()
#         remove_book(book_id)
#         BOOKS.append({
#             'id':uuid.uuid4().hex,
#             'title':post_data.get('title'),
#             'author':post_data.get('author'),
#             'read':post_data.get('read')
#         })
#         response_object['message'] = 'book updated!'
#
#     if request.method == 'DELETE':
#         remove_book(book_id)
#         response_object['message'] = 'book removed'
#
#     return jsonify(response_object)

if __name__ == '__main__':
    app.run()
