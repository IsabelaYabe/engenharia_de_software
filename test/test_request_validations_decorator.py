import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify, request
from decorators import request_validations
from banned_words_strategy import BannedWordsStrategy
from sql_injection_strategy import SQLInjectionStrategy

class TestRequestValidationsDecorator(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.testing()