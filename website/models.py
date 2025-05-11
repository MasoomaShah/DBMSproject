from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, first_name):
        self.id = id
        self.email = email
        self.first_name = first_name
