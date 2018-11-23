import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author', required=True, help="this field cannot be left blank")

    @jwt_required()
    def get(self,title):
        book = self.find_by_title(title)
        if book:
            return book
        return {'message':'item not found'}, 404

    @classmethod
    def find_by_title(cls,title):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM books where title =?"
        result = cursor.execute(query,(title,))
        row = result.fetchone()

        if row:
            return {'book': {'name':row[0], 'author':row[1]}}

    def post(self,title):
        if self.find_by_title(title):
            return {'message':"item with title '{}' already exists".format(title)}, 400
        data = Book.parser.parse_args()
        book = {'title':title, 'author': data['author']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO books VALUES (?, ?)"
        cursor.execute(query, (book['title'], book['author']))
        
        connection.commit()
        connection.close()

        return book, 201

    def delete(self, title):
        global BOOKS
        BOOKS = [book for book in BOOKS if book['title'] != title]
        return {'message':'item deleted'}

    def put(self, title):
        data = Book.parser.parse_args()
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
