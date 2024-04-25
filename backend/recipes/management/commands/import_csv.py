import csv

from django.conf import settings
from django.db.transaction import atomic
from django.core.management.base import BaseCommand

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

    csv_path = settings.CSV_DATA_DIRECTORY_PATH
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
                    csv_data = [row for row in csv.DictReader(csvfile)]
            except FileNotFoundError:
                raise FileExistsError(f'Ошибка {file_path} не найден')
            else:
                self.create_object(
                    cls=self.tables[table], csv_data=csv_data, table=table,
                )

    @atomic
    def create_object(self, cls, csv_data, table):
        """Create objects with data from .csv file."""
        self.print_info(name=table)
        for obj_data in csv_data:

            if table in ['ingredients', 'tags', 'users']:
                cls.objects.create(**obj_data).save()

            elif table == 'recipes':
                Recipe.objects.create(
                    author=User.objects.get(
                        id=int(obj_data.get('author'))
                    ),
                    cooking_time=obj_data.get('cooking_time'),
                    image=obj_data.get('image'),
                    name=obj_data.get('name'),
                    text=obj_data.get('text'),
                ).save()

            elif table == 'follows':
                Follow.objects.create(
                    following_author=User.objects.get(
                        id=int(obj_data.get('following_author'))
                    ),
                    user=User.objects.get(id=int(obj_data.get('user'))),
                ).save()

            elif table == 'favorites' or table == 'shopping_cart_recipes':
                cls.objects.create(
                    recipe=Recipe.objects.get(
                        id=int(obj_data.get('recipe'))
                    ),
                    user=User.objects.get(id=int(obj_data.get('user')))
                ).save()

            elif table == 'ingredients_recipes':
                IngredientRecipe.objects.create(
                    amount=int(obj_data.get('amount')),
                    ingredient=Ingredient.objects.get(
                        id=int(obj_data.get('ingredient'))
                    ),
                    recipe=Recipe.objects.get(
                        id=int(obj_data.get('recipe'))
                    ),
                ).save()

            elif table == 'tags_recipes':
                TagRecipe.objects.create(
                    recipe=Recipe.objects.get(
                        id=int(obj_data.get('recipe'))
                    ),
                    tag=Tag.objects.get(id=int(obj_data.get('tag')))
                ).save()

        self.print_info(name=table, obj_count=len(csv_data))

    def print_info(self, name, obj_count=None):
        """Print process and success import message."""
        if obj_count is None:
            self.stdout.write(self.style.NOTICE(
                settings.CSV_IMPORT_PROCCESSING.format(filename=name)
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                settings.CSV_IMPORT_SUCCESS.format(
                    count=obj_count, filename=name
                )
            ))
