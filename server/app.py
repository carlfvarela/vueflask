from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api
import uuid

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
cors = CORS(app, resources={r"*":{"origins": "*"}})
api = Api(app)

class Book(Resource):
    def get(self,title):
        for book in BOOKS:
            if book['title'] == title:
                return book
        return {'item':None}, 404

    def post(self,title):
        data = request.get_json()


        book = {'title':title, 'author':123}
        BOOKS.append(book)
        return book, 201

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
