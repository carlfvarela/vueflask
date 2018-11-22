from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

import uuid
import pdb;
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '12321'
cors = CORS(app, resources={r"*":{"origins": "*"}})
api = Api(app)

jwt = JWT(app, authenticate, identity)

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author',
        type=string,
        required=True,
        help="this field cannot be left blank"
    )
    data = parser.parse_args()

    @jwt_required()
    def get(self,title):
        book = [book for book in BOOKS if book['title'] == title]
        #book = next(filter(lambda x: x['title'] == title, BOOKS), None)  using lambda function
        return {'book':book}, 200 if book else 404

    def post(self,title):
        if [book for book in BOOKS if book['title'] == title]:
            return {'message':"item with title '{}' already exists".format(title)}, 400
        data = Item.parser.parse_args()
        book = {'title':title, 'author': data['author']}
        BOOKS.append(book)
        return book, 201

    def delete(self, title):
        global BOOKS
        BOOKS = [book for book in BOOKS if book['title'] != title]
        return {'message':'item deleted'}

    def put(self, title):
        data = Item.parser.parse_args()
        book = next(filter(lambda x: x['title'] == title, BOOKS),None)
        if book is None:
            book = {'title':title, 'author':data['author']}
            BOOKS.append(book)
        else:
            book.update(data)
        return book


class BookList(Resource):
    def get(self):
        return {'books':BOOKS}


api.add_resource(Book, '/book/<string:title>')
api.add_resource(BookList, '/books')



def remove_book(book_id):
    #[BOOKS.remove(book) for book in BOOKS if book['id'] == book_id]

    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return true
        return False


# @app.route('/books', methods=['GET','POST'])
# def all_books():
#
#     response_object = {'status':'success'}
#     if request.method == 'POST':
#         post_data = request.get_json()
#
#         BOOKS.append({
#             'id':uuid.uuid4().hex,
#             'title':post_data.get('title'),
#             'author':post_data.get('author'),
#             'read':post_data.get('read')
#         })
#         response_object['message'] = 'book added'
#     else:
#         response_object['books'] = BOOKS
#
#     return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status':'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id':uuid.uuid4().hex,
            'title':post_data.get('title'),
            'author':post_data.get('author'),
            'read':post_data.get('read')
        })
        response_object['message'] = 'book updated!'

    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'book removed'

    return jsonify(response_object)

BOOKS = []

if __name__ == '__main__':
    app.run()
