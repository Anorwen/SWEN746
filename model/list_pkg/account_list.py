from model.list_pkg.list import List
from model.list_pkg.singleton import Singleton
from model.account_pkg.account import Account
from model.account_pkg.author_account import AuthorAccount
from model.account_pkg.administrator_account import AdministratorAccount
from model.account_pkg.pcm_account import PCMAccount
from model.account_pkg.pcc_account import PCCAccount


class AccountList(List, Singleton):
    """
    Collection of all the Accounts for the System. Maps AccountID to the corresponding Account. Concrete class in the
    Template Method design pattern. Also incorporates the Singleton design pattern to prevent different collections of
    Accounts from existing within the System at the same time.
    """

    # ----------
    # Attributes
    # ----------
    E = Account
    # See List Class

    # ------------
    # Constructors
    # ------------
    # See List Class

    # -------
    # Methods
    # -------
    def mongo_save_entry(self, entry: E):
        """
        Saves a new entry to the Mongo Database.
        :param entry: Instance of the object to add to the database.
        :return: void.
        """
        new_entry = {"accountID": entry.account_id, "username": entry.username, "password": entry.password,
                     "role": entry.role.value}
        self._collection.insert_one(new_entry)

    def mongo_delete_entry(self, entry: E):
        """
        Deletes an existing entry from the Mongo Database.
        :param entry: Instance of the object to remove from the database.
        :return: void.
        """
        self._collection.delete_one({"accountID": entry.account_id})

    def mongo_update_entry(self, old_entry: E, new_entry: E):
        """
        Updates an existing entry in the Mongo Database.
        :param old_entry: Instance of the entry to override in the database.
        :param new_entry: Instance of the entry to enter into the database.
        :return: void.
        """
        updated_entry = {"accountID": new_entry.account_id, "username": new_entry.username,
                         "password": new_entry.password, "role": new_entry.role.value}
        self._collection.update_one({"accountID": old_entry.account_id}, {"$set": updated_entry})

    def populate_list(self):
        """
        Pulls existing information from the Mongo Database and creates all of the instances that should exist for the
        List's corresponding object type. Should only be called by the constructor.
        :return: void.
        """
        for entry in self._collection.find():
            account = self.create_entry_object(entry)
            self._entries[entry["accountID"]] = account

    def create_entry_object(self, entry):
        """
        Create and return an instance of an object. Parses the parameters to create an instance of the object. This does
        not add the object to the collection if called directly.
        :param entry: Hash of information to create the object.
        :return: Instance of the appropriate object based on the type of List.
        """
        account = None
        account_id = entry.get("accountID", self.create_unique_id())
        username = entry["username"]
        password = entry["password"]
        role = entry["role"]
        if role == Account.Role.AUTHOR.value:
            account = AuthorAccount(account_id, username, password)
        elif role == Account.Role.PCM.value:
            account = PCMAccount(account_id, username, password)
        elif role == Account.Role.PCC.value:
            account = PCCAccount(account_id, username, password)
        elif role == Account.Role.ADMIN.value:
            account = AdministratorAccount(account_id, username, password)
        return account

    def get_list_json(self):
        """
        Creates and returns a JSON file representing the Dictionary for the List object. The first JSON object will be
        the lowercase name of the type of entry being stored.
        :return: JSON file representing the collection.
        """
        accounts = []

        for entry_id in self._entries.keys():
            accounts.append({
                "accountID": self._entries[entry_id].account_id,
                "username": self._entries[entry_id].username,
                "password": self._entries[entry_id].password,
                "role": self._entries[entry_id].role.value,
            })
        return accounts

    def get_entry_json(self, entry_id: int):
        """
        Create and return a JSON representing the entry at the corresponding id location.
        :param entry_id: int id of the entry.
        :return: JSON format for the entry.
        """
        return {
                "accountID": self._entries[entry_id].account_id,
                "username": self._entries[entry_id].username,
                "password": self._entries[entry_id].password,
                "role": self._entries[entry_id].role.value,
            }