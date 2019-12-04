from flask import Flask
import urllib.parse
from flask_pymongo import PyMongo
from model.list_pkg.list import List
from model.list_pkg.singleton import Singleton
from model.artifact import Artifact


class ArtifactList(List, Singleton):
    """
    Collection of all the Artifacts for the System. Maps ArtifactID to the corresponding Artifact. Concrete class in the
    Template Method design pattern. Also incorporates the Singleton design pattern to prevent different collections of
    Artifacts from existing within the System at the same time.
    """

    # ----------
    # Attributes
    # ----------
    E = Artifact
    # See List Class

    # ------------
    # Constructors
    # ------------
    def __init__(self):
        app = Flask(__name__, template_folder="view")
        app.config["MONGO_URI"] = "mongodb+srv://" + urllib.parse.quote_plus("USER2") + ":" + urllib.parse.quote_plus(
            "1q2w3e4r") + "@cluster0-tk7v1.mongodb.net/SAM2020?retryWrites=true&w=majority"
        mongo = PyMongo(app)
        super().__init__(mongo.db['Artifacts'])

    # -------
    # Methods
    # -------
    def _mongo_save_entry(self, entry: E):
        """
        Saves a new entry to the Mongo Database.
        :param entry: Instance of the object to add to the database.
        :return: void.
        """
        self._collection.insert_one(entry.create_entry_dictionary())

    def _mongo_delete_entry(self, entry: E):
        """
        Deletes an existing entry from the Mongo Database.
        :param entry: Instance of the object to remove from the database.
        :return: void.
        """
        self._collection.delete_one({"artifactID": entry.get_entry_id()})

    def _mongo_update_entry(self, old_entry: E, new_entry: E):
        """
        Updates an existing entry in the Mongo Database.
        :param old_entry: Instance of the entry to override in the database.
        :param new_entry: Instance of the entry to enter into the database.
        :return: void.
        """
        self._collection.update_one({"artifactID": old_entry.get_entry_id()},
                                    {"$set": new_entry.create_entry_dictionary()})

    def _populate_list(self):
        """
        Pulls existing information from the Mongo Database and creates all of the instances that should exist for the
        List's corresponding object type. Should only be called by the constructor.
        :return: void.
        """
        for entry in self._collection.find():
            artifact = Artifact(0, 0, None, 0, "")
            artifact.set_entry_attributes(entry)
            self._entries[entry["artifactID"]] = artifact
