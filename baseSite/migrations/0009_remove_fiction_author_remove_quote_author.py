# Generated by Django 4.2.9 on 2024-02-22 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseSite', '0008_pokemon_abilities_pokemon_attack_pokemon_bst_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fiction',
            name='author',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='author',
        ),
    ]