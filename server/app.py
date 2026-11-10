#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

class Books(Resource):
    def get(self):
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=5, type=int)
        pagination = Book.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        books = [BookSchema().dump(b) for b in pagination.items]
        response_data = {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": books,
        }
        return response_data, 200


api.add_resource(Books, '/books', endpoint='books')

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)


if __name__ == '__main__':
    app.run(port=5555, debug=True)