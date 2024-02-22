from django.db import models

CATEGORY = (
    ("tv_show", "TV Show"),
    ("movie", "Movie"),
    ("book", "Book")
)


class Fiction(models.Model):
    name = models.CharField(max_length=400)
    category = models.CharField(max_length=200, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="fictionImages")

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField()
    fiction = models.ForeignKey(Fiction, on_delete=models.CASCADE)
    character = models.CharField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="quoteImages")


class Type(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    number = models.IntegerField(default=None)
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    primaryType = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='primaryType')
    secondaryType = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='secondaryType', default=None, blank=True, null=True)
    abilities = models.TextField(default=None)
    generation = models.IntegerField(default=None)
    attack = models.IntegerField(default=None)
    defense = models.IntegerField(default=None)
    special_attack = models.IntegerField(default=None)
    special_defense = models.IntegerField(default=None)
    speed = models.IntegerField(default=None)
    bst_total = models.IntegerField(default=None)

    def __str__(self):
        return self.name