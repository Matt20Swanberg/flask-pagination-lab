#!/usr/bin/env python3

"""
Flask API for retrieving books with server-side pagination

This application uses Flask-RESTful, Flask-SQLAlchemy, and
Marshmallow to retrieve, paginate, and serialize book records
"""

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

class Books(Resource):
    """
    RESTful resource for retrieving paginated book records

    Supports optional query parameters:
        page (int): Page number to retrieve. Defaults to 1
        per_page (int): Number of books per page. Defaults to 5

    Returns:
        A JSON response containing the requested books and
        pagination metadata
    """

    def get(self):
        """
        Retrieve a paginated collection of books

        Example:
            GET /books?page=2&per_page=5

        Returns:
            tuple: A dictionary containing pagination metadata
            and serialized books, along with HTTP status 200
        """

        # Retrieve pagination parameters from the request URL
        # Use default values when parameters are not provided
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=5, type=int)
        # Query the database for only the requested page of books
        # error_out=False prevents an automatic 404 response when
        # the requested page exceeds the available records
        pagination = Book.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Serialize the Book objects belonging to the current page
        # pagination.items contains only the records for this page
        books = [BookSchema().dump(b) for b in pagination.items]

        # Construct the API response with pagination metadata
        # total represents all matching books in the database,
        # while total_pages represents the number of available pages
        response_data = {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": books,
        }

        # Return the structured response with HTTP status 200
        return response_data, 200

# Register the Books resource before initializing the Flask app
# This ensures Flask-RESTful attaches the /books route correctly
api.add_resource(Books, '/books', endpoint='books')

# Load the appropriate application configuration
# Defaults to the development environment
env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

# Start the development server when this file is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)