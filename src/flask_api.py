"""
Module for FlaskAPI Class.

This module provides the `FlaskAPI` class, which creates a RESTful API for basic CRUD (Create, Read, Update, Delete) operations on a specified database table. The class uses Flask to set up endpoints for accessing, creating, updating, and deleting records in the database.

Author: Isabeça Yabe
Last Modified: 06/11/2024
Status: Put logs

Dependencies:
    - flask.Flask
    - flask.jsonify
    - flask.request
    - flask_cors.CORS (optional for handling CORS, if needed)

Classes:
    - FlaskAPI: Class for setting up and running a RESTful API for a database table.

Usage Example:
    db_table = YourDatabaseTable()
    api = FlaskAPI(db_table)
    api.run(debug=True)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

class FlaskAPI:
    """
    FlaskAPI class.

    This class provides a RESTful API interface for performing CRUD operations on a specified database table.
    It uses Flask to create API endpoints based on the table name and allows for seamless data handling between
    the client and database.

    Attributes:
        - _db_table: An instance of a database table class providing CRUD operations.
        - _app (Flask): The Flask app instance for setting up and running the API.

    Methods:
        - _setup_routes(): Sets up all API routes for CRUD operations.
        - _get_record_api(record_id): Handles GET requests to retrieve a specific record by its ID.
        - _create_record_api(*data): Handles POST requests to create a new record in the database.
        - _update_record_api(record_id, **kwargs): Handles PUT requests to update a specific record by ID.
        - _delete_record_api(record_id): Handles DELETE requests to delete a specific record by ID.
        - run(debug): Starts the Flask API server.

    API Endpoints:
        - GET /api/<table_name>/<record_id>: Retrieves a specific record by its ID.
        - POST /api/<table_name>: Creates a new record with data from the request body.
        - PUT /api/<table_name>/<record_id>: Updates a specific record by its ID with data from the request body.
        - DELETE /api/<table_name>/<record_id>: Deletes a specific record by its ID.
    """
    def __init__(self, db_table):
        """
        Initializes the FlaskAPI instance with the specified database table.

        Args:
            db_table: An instance of a database table class providing methods for CRUD operations.
        """
        self._db_table = db_table
        self._app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        """
        Sets up all API routes for CRUD operations.
        """
        @self._app.route(f"/api/{self._db_table._table_name}/<record_id>", methods=["GET"])
        def _get_record(record_id):
            return self._get_record_api(record_id)

        @self._app.route(f"/api/{self._db_table._table_name}", methods=["POST"])
        def _create_record():
            data = request.json
            return self._create_record_api(*data)

        @self._app.route(f"/api/{self._db_table._table_name}/<record_id>", methods=["PUT"])
        def _update_record(record_id):
            data = request.json
            return self._update_record_api(record_id, **data)

        @self._app.route(f"/api/{self._db_table._table_name}/<record_id>", methods=["DELETE"])
        def _delete_record(record_id):
            return self._delete_record_api(record_id)
        
    def _get_record_api(self, record_id):
        """
        Handles GET requests to retrieve a specific record by its ID.

        Args:
            record_id (str): The ID of the record to retrieve.

        Returns:
            JSON response: The record data in JSON format, or an error message if not found.
            HTTP status code: 200 if found, 404 if not found.
        """
        record = self._db_table.get_by_id(record_id) 
        if record:
            return jsonify(record), 200
        else:
            return jsonify({"error": "Record not found"}), 404
        
    def _create_record_api(self, *data):
        """
        Handles POST requests to create a new record in the database.

        Args:
            *data: The data for the new record, extracted from the request JSON.

        Returns:
            JSON response: A success message if creation is successful, or an error message otherwise.
            HTTP status code: 201 if created, 400 if an error occurs.
        """
        try:
            self._db_table.insert_row(*data)
            return jsonify({"message": "Record created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    def _update_record_api(self, record_id, **kwargs):
        """
        Handles PUT requests to update a specific record by its ID.

        Args:
            record_id (str): The ID of the record to update.
            **kwargs: The data fields to update in the record.

        Returns:
            JSON response: A success message if update is successful, or an error message otherwise.
            HTTP status code: 200 if updated, 400 if an error occurs.
        """
        try:
            self._db_table.update_row(record_id, **kwargs)
            return jsonify({"message": "Record update"}), 200       
        except Exception as e: 
            return jsonify({"error": str(e)}), 400
        
    def _delete_record_api(self, record_id):
        """
        Handles DELETE requests to delete a specific record by its ID.

        Args:
            record_id (str): The ID of the record to delete.

        Returns:
            JSON response: A success message if deletion is successful, or an error message otherwise.
            HTTP status code: 200 if deleted, 400 if an error occurs.
        """
        try:
            self._db_table.delete_row(record_id)
            return jsonify({"message": "Record deletes"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def run(self, debug=False):
        """
        Starts the Flask API server.

        Args:
            debug (bool): Whether to enable Flask's debug mode. Default is False.
        """
        self._app.run(debug=debug)