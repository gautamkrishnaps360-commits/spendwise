from django.contrib.auth.models import User
from rest_framework import serializers
from spending.models import Expense
class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","email","password"]

        read_only=["id"]

class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:

        model=Expense

        fields="__all__"

        read_only_fields=["id","owner","created_at","updated_at"]