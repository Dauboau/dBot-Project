import os
import sys
from pymongo import MongoClient,HASHED
from pymongo.errors import OperationFailure

class MongoDB:

    def __init__(self):
        username = os.environ.get('MONGO_DB_USERNAME')
        password = os.environ.get('MONGO_DB_PASSWORD')
        
        uri = f"mongodb+srv://{username}:{password}@dbot.1at0vdy.mongodb.net/?retryWrites=true&w=majority&appName=dBot"
        self.client = MongoClient(uri)
        
        try:
            self.client.admin.command('ping')
            print("dBotMod successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            sys.exit(1)

        self.db = self.client["dBotMod"]
        guild_schema = {
            "bsonType": "object",
            "required": ["_id","name","moderating_hystory","message_hystory"],
            "properties": {
                "_id": {
                    "bsonType": "string",
                    "description": "Server ID (Guild ID)"
                },
                "name": {
                    "bsonType": "string",
                    "description": "Server Name (Guild Name)"
                },
                "moderating_hystory": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["bad_author_id", "problem", "moderated_at"],
                        "properties": {
                            "bad_author_id": {
                                "bsonType": "string",
                                "description": "User ID (Author ID) of the author of the message that was moderated"
                            },
                            "problem": {
                                "bsonType": "string",
                                "description": "Problem found in the messages"
                            },
                            "moderated_at": {
                                "bsonType": "date",
                                "description": "Date when the messages were moderated"
                            }
                        }
                    }
                },
                "message_hystory": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["author_id", "author_name", "content", "created_at"],
                        "properties": {
                            "author_id": {
                                "bsonType": "string",
                                "description": "User ID (Author ID)"
                            },
                            "author_name": {
                                "bsonType": "string",
                                "description": "User Name (Author Name)"
                            },
                            "content": {
                                "bsonType": "string",
                                "description": "Message Content"
                            },
                            "created_at": {
                                "bsonType": "date",
                                "description": "Message Creation Date"
                            }
                        }
                    }
                }
            }
        }

        if "guild" not in self.db.list_collection_names():
            self.db.create_collection(
                "guild",
                validator={"$jsonSchema": guild_schema},
                validationLevel="strict"
            )
        else:
            try:
                self.db.command(
                    "collMod", "guild",
                    validator={"$jsonSchema": guild_schema},
                    validationLevel="strict"
                )
            except OperationFailure as e:
                print(f"Error, updating the Schema will be skipped: {e.codeName}")

        self.guild_table = self.db["guild"]

        # Hashed Index for lookup
        self.guild_table.create_index(
            [("_id", HASHED)],
            name="idx_id_hashed"
        )

class RedisDB:

    def __init__(self):
        print("RedisDB is not implemented yet.")