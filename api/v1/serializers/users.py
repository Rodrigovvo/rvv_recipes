from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import Chef


class ChefSerializer(serializers.ModelSerializer):
    """ Serializer for Chef """

    class Meta:
        model = Chef
        fields = '__all__'
