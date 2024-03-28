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
from mongo import MongoDB
import click
import random
import datetime
import os


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


def people_from_age_bracket(
    min_age: int, max_age: int, number_of_people: int, data_base
) -> List:
    query = {"age": {"$gt": min_age, "$lt": max_age}}
    person_details = data_base.find_documents(
        query,
        {},
        # query, {"_id": 0, "date of birth": 0, "salary before taxes": 0}
    )[:number_of_people]
    return person_details


if __name__ == "__main__":
    tax_db = MongoDB(
        host="localhost",
        port=27017,
        db_name="income_tax",
        collection_name="people",
    )

    os.system("cls")

    def show_app_menu() -> str:

        return input(
            f"""
If you want view ten people information press {"--y--":^35}

Press --9-- to quit our app                          
"""
        )

    os.system("cls")
    while True:

        try:
            user_option = show_app_menu()
        except:
            print("Wrong input. Please enter a number from the list...")
            break

        if user_option == "y":
            os.system("cls")
            try:
                user_option_min_age = int(input("Enter minimum age: "))
                user_option_max_age = int(input("Enter max age: "))
                os.system("cls")
                group_of_people = people_from_age_bracket(
                    user_option_min_age, user_option_max_age, 10, tax_db
                )

                print("People:")
                for index, person in enumerate(group_of_people):
                    index += 1
                    print(
                        f"{index}.-- {person['name']} {person['surname']} {person['age']} years old"
                    )
                person_id = int(input("Person id.. "))

                try:
                    selected_person = group_of_people[int(person_id) - 1]

                    if len(selected_person) > 6:
                        print(
                            f"{selected_person['name']} {selected_person['surname']} has to pay {selected_person['gpm tax']} EUR GPM tax, {selected_person['health tax']} EUR health tax. Gross salary after taxes will be {selected_person['final salary']} EUR"
                        )
                    else:
                        gpm_deduction = round(
                            selected_person["salary before taxes"] * 0.1, 2
                        )
                        salary_after_gpm_deduction = round(
                            selected_person["salary before taxes"] * 0.9, 2
                        )
                        gpm_taxes = round(salary_after_gpm_deduction * 0.2, 2)
                        health_taxes = round(salary_after_gpm_deduction * 0.15, 2)
                        final_salary = round(salary_after_gpm_deduction * 0.65, 2)
                        query = {"_id": selected_person["_id"]}
                        document_update = {
                            "gpm deduction": gpm_deduction,
                            "salary after gpm deduction": salary_after_gpm_deduction,
                            "gpm tax": gpm_taxes,
                            "health tax": health_taxes,
                            "final salary": final_salary,
                        }
                        print("updatinam dokument")
                        tax_db.update_one_document(query, document_update)

                        print(tax_db.find_documents(query, {}))
                except:
                    # os.system("cls")
                    print("Wrong input. Please enter a integers...")
                    break

            except:
                # os.system("cls")
                print("Wrong input. Please enter a integers...")
                break
        else:
            os.system("cls")
            print("You exited the program, Bye!")
            break
