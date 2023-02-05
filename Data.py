import traceback
from .File import File


class Data(File):
    def __init__(self):
        super().__init__("data.txt", """{"users": {}, "logged": []}""")
        try:
            self.users: dict = self.data['users']
            self.logged: list = self.data['logged']
        except Exception:
            traceback.print_exc()
            self.recreate()

    def add_logged(self, id):
        self.logged.append(id)
        self.save()

    def rem_logged(self, id):
        if self.is_logged(id):
            self.logged.remove(id)
            self.save()

    def is_logged(self, id):
        return id in self.logged

    def is_user(self, username):
        return username in self.users

    def get_password(self, username):
        return self.users.get(username)

    def save(self):
        data = {"users": self.users,
                "logged": self.logged}
        self.write(data)
