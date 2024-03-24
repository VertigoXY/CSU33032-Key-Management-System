from user import User


class SecureCloudStorageGroup:
    def __init__(self):
        self.users = dict()  # This variable contains all the existing users in our application (i.e. all potential users)
        self.group_users = dict()

    def add_user(self, user: User, admin=False):
        self.group_users[user.name] = user
        user.group = self
        user.admin = admin

    def remove_user(self, user: User):
        del self.group_users[user.name]
        user.group = None
