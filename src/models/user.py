from mongoengine import Document, StringField


class User(Document):
    """
    TASK: Create a model for user with minimalistic
          information required for user authentication

    HINT: Do not store password as is.
    """
    def __int__(self, username, password):
        self.username = username
        self.password = password

    username = StringField(unique=True, required=True)
    password = StringField(required=True)
