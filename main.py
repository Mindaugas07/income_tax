# Create an income tax calculator:
#  - Generate at least 500 documents , with fields: name, surname, date of birth ,
# age (determined from date of birth), anual salary before tax (EUR, round to 2 numbers after comma)
#  - Create a CLI application that would let us get first 10 people from database within the age bracket [min_age, max_age]
#  - Those people name surname and age should be shown as an option to choose.
#  - When one of ten options is chosen, there should be calculated tax return (it should be created a document as a tax card,
# values taken from database).
# Lets say GPM tax is 20% and HealtTax is 15% from 90% of the income left after GPM deduction.
#  - The final values should be show and wrriten to database (like a generated data and taxes paid, take home pay etc.)
# and portrayed in a web page (use flask and docker, show the url were to click )

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Union
from faker import Faker
from random import random, randint
from datetime import date
import random
import datetime


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    print(f"Printed result: {result}")
    return str(result.inserted_id)


def create_a_person():
    fake = Faker()
    name = fake.first_name()
    surname = fake.last_name()
    date_of_birth = fake.date_between("-60y", "-20y")
    age = date.today().year - date_of_birth.year
    salary_before_tax = round(random.uniform(60000.00, 200000.00), 2)
    return name, surname, date_of_birth, age, salary_before_tax


if __name__ == "__main__":
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "income_tax"
    collection_name = "people"

    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    collection = db[collection_name]
    fake = Faker()
    for _ in range(500):
        name, surname, date_of_birth, age, salary_before_tax = create_a_person()
        document = {
            "name": name,
            "surname": surname,
            "date of birth": str(date_of_birth),
            "age": age,
            "salary before taxes": salary_before_tax,
        }
        inserted_id = insert_document(collection, document)
        print(f"Inserted document with ID: {inserted_id}")
        print(f"This person was inserted into the database: {document}")
