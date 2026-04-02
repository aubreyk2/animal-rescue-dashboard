import pandas as pd
from pymongo import MongoClient
import os

class AnimalShelter:
    """CRUD operations for Animal collection in MongoDB with CSV fallback"""

    def __init__(self, username, password):
        USER = username
        PASS = password
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        self.csv_path = os.path.join("datasets", "aac_shelter_outcomes.csv")
        self.use_csv = False

        try:
            self.client = MongoClient(
                f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource={DB}'
            )
            self.database = self.client[DB]
            self.collection = self.database[COL]

            #Create indexes
            self.collection.create_index("animal_type")
            self.collection.create_index("name")
            self.collection.create_index("breed")
            self.collection.create_index("age")

        except Exception as e:
            print("MongoDB connection failed, using CSV fallback:", e)
            self.use_csv = True
            self.df_csv = pd.read_csv(self.csv_path)

    def create(self, data):
        if data is None:
            raise Exception("Nothing to save, because data parameter is empty")

        try:
            if self.use_csv:
                self.df_csv = pd.concat([self.df_csv, pd.DataFrame([data])], ignore_index=True)
                self.df_csv.to_csv(self.csv_path, index=False)
                return True
            else:
                result = self.collection.insert_one(data)
                return bool(result.inserted_id)
        except Exception as e:
            print("Error inserting document:", e)
            return False

    def read(self, query={}):
        try:
            if self.use_csv:
                df = self.df_csv.copy()
                for k, v in query.items():
                    df = df[df[k] == v]
                return df.to_dict(orient='records')
            else:
                return list(self.collection.find(query))
        except Exception as e:
            print("Error reading documents:", e)
            return []

    def read_filtered(self, animal_type=None, breed=None, min_age=None, max_age=None):
        try:
            if self.use_csv:
                df = self.df_csv.copy()
                if animal_type:
                    df = df[df['animal_type'] == animal_type]
                if breed:
                    df = df[df['breed'] == breed]
                if min_age is not None:
                    df = df[df['age'] >= min_age]
                if max_age is not None:
                    df = df[df['age'] <= max_age]
                return df.sort_values(by='name').to_dict(orient='records')
            else:
                pipeline = []
                if animal_type:
                    pipeline.append({"$match": {"animal_type": animal_type}})
                if breed:
                    pipeline.append({"$match": {"breed": breed}})
                age_filter = {}
                if min_age is not None:
                    age_filter["$gte"] = min_age
                if max_age is not None:
                    age_filter["$lte"] = max_age
                if age_filter:
                    pipeline.append({"$match": {"age": age_filter}})
                pipeline.append({"$sort": {"name": 1}})
                return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print("Error with filtered read:", e)
            return []

    def update(self, query, new_values):
        if query is None or new_values is None:
            raise Exception("Query or new_values parameter is empty")

        try:
            if self.use_csv:
                df = self.df_csv.copy()
                mask = pd.Series([True] * len(df))
                for k, v in query.items():
                    mask &= df[k] == v
                self.df_csv.loc[mask, list(new_values.keys())] = list(new_values.values())
                self.df_csv.to_csv(self.csv_path, index=False)
                return mask.sum()
            else:
                result = self.collection.update_many(query, {"$set": new_values})
                return result.modified_count
        except Exception as e:
            print("Error updating documents:", e)
            return 0

    def delete(self, query):
        if query is None:
            raise Exception("Query parameter is empty")

        try:
            if self.use_csv:
                df = self.df_csv.copy()
                mask = pd.Series([True] * len(df))
                for k, v in query.items():
                    mask &= df[k] == v
                deleted_count = mask.sum()
                self.df_csv = self.df_csv.loc[~mask]
                self.df_csv.to_csv(self.csv_path, index=False)
                return deleted_count
            else:
                result = self.collection.delete_many(query)
                return result.deleted_count
        except Exception as e:
            print("Error deleting documents:", e)
            return 0
