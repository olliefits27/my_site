from rest_framework import serializers
from .models import Pokemon, Type

class PokemonSerializer(serializers.ModelSerializer):
    primaryType = serializers.CharField(source='primaryType.name')
    secondaryType = serializers.CharField(allow_blank=True, allow_null=True, source='secondaryType.name')

    class Meta:
        model = Pokemon
        fields = ["number", "name", "primaryType", "secondaryType", "abilities", "attack", "defense", "special_attack",
                  "special_defense", "speed", "bst_total", "generation"]