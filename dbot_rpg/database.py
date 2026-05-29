import os
import sys
from pymongo import MongoClient, HASHED
from pymongo.errors import OperationFailure

class MongoDB:

    def __init__(self):
        username = os.environ.get('MONGO_DB_USERNAME')
        password = os.environ.get('MONGO_DB_PASSWORD')
        
        uri = f"mongodb+srv://{username}:{password}@dbot.1at0vdy.mongodb.net/?retryWrites=true&w=majority&appName=dBot"
        self.client = MongoClient(uri)
        
        try:
            self.client.admin.command('ping')
            print("dBotRPG successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            sys.exit(1)

        self.db = self.client["dBotRPG"]
        
        user_dice_schema = {
            "bsonType": "object",
            "required": ["_id", "user_name", "last_roll_sum"],
            "properties": {
                "_id": {
                    "bsonType": "string",
                    "description": "User ID (Author ID)"
                },
                "user_name": {
                    "bsonType": "string",
                    "description": "User Name (Author Name)"
                },
                "last_roll_sum": {
                    "bsonType": ["int", "long"],
                    "description": "Sum of the last dice rolls"
                }
            }
        }

        if "user_dice" not in self.db.list_collection_names():
            self.db.create_collection(
                "user_dice",
                validator={"$jsonSchema": user_dice_schema},
                validationLevel="strict"
            )
        else:
            try:
                self.db.command(
                    "collMod", "user_dice",
                    validator={"$jsonSchema": user_dice_schema},
                    validationLevel="strict"
                )
            except OperationFailure as e:
                print(f"Error, updating the Schema will be skipped: {e.codeName}")

        self.user_dice_table = self.db["user_dice"]

        # Hashed Index for lookup
        self.user_dice_table.create_index(
            [("_id", HASHED)],
            name="idx_id_hashed"
        )
