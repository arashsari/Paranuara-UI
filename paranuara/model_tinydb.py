from flask import current_app
from werkzeug.exceptions import BadRequest
from tinydb import TinyDB, Query
import json


class Model():
    def __init__(self, db_name, resource_name):
        resource_address = 'paranuara/resources/{}.json'.format(resource_name)
        with open(resource_address) as file:
            self.data = json.load(file)

    def list(self):
            return self.db


    # def __init__(self, db_name, resource_name):
    #     resource_address = 'paranuara/resources/{}.json'.format(resource_name)
    #     self.db = TinyDB('paranuara/resources/{}.json'.format(db_name))
    #     if len(self.db) == 0 :
    #         with open(resource_address) as file:
    #             for item in json.load(file):
    #                 self.db.insert(item)
    #         print(len(self.db))
    #     else:
    #         print(len(self.db))
    #         print('DB File exist!')
    #
    # def list(self):
    #         return self.db.all()
