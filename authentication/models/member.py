from typing import List
from authentication.models.restaurant import Restaurant
from restrofin.base_model import BaseModel
from django.db import models
from django.contrib.auth.models import User


class Member(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("user", "restaurant")
