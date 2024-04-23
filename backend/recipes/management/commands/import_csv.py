from time import sleep

from django.core.management.base import BaseCommand

from foodgram_backend.settings import (
    CSV_DATA_DIRECTORY_PATH, CSV_IMPORT_PROCCESSING, CSV_IMPORT_SUCCESS
)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCartRecipe,
    Tag,
    TagRecipe,
)
from users.models import Follow, User


class Command(BaseCommand):
    """Describe custom Django commands."""

    csv_path = CSV_DATA_DIRECTORY_PATH
    tables = {
        'ingredients': Ingredient,
        'tags': Tag,
        'users': User,
        'recipes': Recipe,
        'follows': Follow,
        'favorites': Favorite,
        'ingredients_recipes': IngredientRecipe,
        'shopping_cart_recipes': ShoppingCartRecipe,
        'tags_recipes': TagRecipe,
    }

    def handle(self, *args, **options):
        """Extract data from .csv file and call create_object func."""
        for table in self.tables:
            file_path = f'{self.csv_path}/{table}.csv'
            try:
                with open(file_path, mode="r", encoding="utf-8") as csvfile:
                    csv_data = [
                        [
                            int(value) if value.isnumeric() else value
                            for value in row
                        ]
                        for row in [
                            row.split('",') if '"' in row else row.split(',')
                            for row in csvfile.read().splitlines()
                        ]]
            except FileNotFoundError:
                raise FileExistsError(f'Ошибка {file_path} не найден')
            else:
                self.create_object(
                    cls=self.tables[table], csv_data=csv_data, table=table,
                )

    def create_object(self, cls, csv_data, table):
        """Create objects with data from .csv file."""
        if table == 'ingredients':
            self.print_info(name=table)
            for name, measurement_unit in csv_data:
                Ingredient.objects.create(
                    name=name, measurement_unit=measurement_unit
                ).save()
            self.print_info(name=table, obj_count=len(csv_data))

        elif table == 'tags':
            self.print_info(name=table)
            for name, color, slug in csv_data:
                Tag.objects.create(name=name, color=color, slug=slug).save()
            self.print_info(name=table, obj_count=len(csv_data))

        elif table == 'users':
            self.print_info(name=table)
            for (email, first_name, last_name, password, role,
                 username) in csv_data:
                User.objects.create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    role=role,
                    username=username,
                ).save()
            self.print_info(name=table, obj_count=len(csv_data))

        elif table == 'recipes':
            self.print_info(name=table)
            for author_id, cooking_time, image, name, text in csv_data:
                Recipe.objects.create(
                    author=User.objects.get(id=author_id),
                    cooking_time=cooking_time,
                    image=image,
                    name=name,
                    text=text,
                ).save()
            self.print_info(name=table, obj_count=len(csv_data))

        elif table == 'follows':
            self.print_info(name=table)
            for following_author_id, user_id in csv_data:
                Follow.objects.create(
                    following_author=User.objects.get(id=following_author_id),
                    user=User.objects.get(id=user_id),
                ).save()
            self.print_info(name=table, obj_count=len(csv_data))

        elif table == 'favorites' or table == 'shopping_cart_recipes':
            self.print_info(name=table)
            for recipe_id, user_id in csv_data:
                cls.objects.create(
                    recipe=Recipe.objects.get(id=recipe_id),
                    user=User.objects.get(id=user_id)
                ).save()
            self.print_info(name=table, obj_count=len(csv_data))

        elif table == 'ingredients_recipes':
            self.print_info(name=table)
            for amount, ingredient_id, recipe_id in csv_data:
                IngredientRecipe.objects.create(
                    amount=amount,
                    ingredient=Ingredient.objects.get(id=ingredient_id),
                    recipe=Recipe.objects.get(id=recipe_id),
                ).save()
            self.print_info(name=table, obj_count=len(csv_data))

        elif table == 'tags_recipes':
            self.print_info(name=table)
            for recipe_id, tag_id in csv_data:
                TagRecipe.objects.create(
                    recipe=Recipe.objects.get(id=recipe_id),
                    tag=Tag.objects.get(id=tag_id)
                ).save()
            self.print_info(name=table, obj_count=len(csv_data))

    def print_info(self, name, obj_count=None):
        """Print process and success import message."""
        if obj_count is None:
            sleep(0.25)
            self.stdout.write(self.style.NOTICE(
                CSV_IMPORT_PROCCESSING.format(filename=name)
            ))
        else:
            sleep(0.25)
            self.stdout.write(self.style.SUCCESS(
                CSV_IMPORT_SUCCESS.format(count=obj_count, filename=name)
            ))
