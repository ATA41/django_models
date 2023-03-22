from django.db import models


class User(models.Model):
    username = models.CharField(verbose_name="Username", max_length=20,)
    password = models.CharField(verbose_name="Password", max_length=20,)


class Client(models.Model):
    name = models.CharField(verbose_name="ClientName", max_length=50,)
    card_number = models.IntegerField(verbose_name="Card_number")
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Worker(models.Model):
    name = models.CharField(verbose_name="WorkerName", max_length=50,)
    position = models.CharField(verbose_name="Position", max_length=50,)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(verbose_name="IngredientName", max_length=50, )
    extra_price = models.IntegerField(verbose_name="ExtraPrice")


class Food(models.Model):
    name = models.CharField(verbose_name="FoodName", max_length=50, )
    start_price = models.IntegerField(verbose_name="StartPrice")
    ingredients = models.ManyToManyField(Ingredient, through='FoodIngredient')


class FoodIngredient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    extra_price = models.IntegerField()


class Order(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_auto_now = models.DateTimeField(auto_now=True)

    def full_price(self):
        ingredient_cost = sum(i.extra_price for i in self.ingredient.all())
        return self.food.start_price + ingredient_cost


