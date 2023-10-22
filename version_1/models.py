from mongoengine import (
    connect,
    Document,
    StringField,
    ReferenceField,
    CASCADE,
    ListField,
)


class Authors(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()
