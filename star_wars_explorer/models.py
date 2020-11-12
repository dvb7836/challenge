from django.db import models
from marshmallow import Schema, fields


class Person(Schema):
    name = fields.Str()
    height = fields.Str()
    mass = fields.Str()
    hair_color = fields.Str()
    skin_color = fields.Str()
    eye_color = fields.Str()
    birth_year = fields.Str()
    gender = fields.Str()
    homeworld = fields.Str()
    date = fields.Date()


class Collection(models.Model):
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %-I:%-M %p")
