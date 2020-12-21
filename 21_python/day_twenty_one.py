from collections import defaultdict
import time

start_time = time.time()


def load_data():
    with open('day_twenty_one_data.txt') as fh:
        foods = [get_data(line) for line in fh.readlines()]
    return foods


def get_data(line):
    ingredients, allergens = line.strip()[:-1].split('(')
    ingredients = ingredients.strip().split(' ')
    allergens = allergens.replace('contains ', '').split(', ')
    return [ingredients, allergens]


def part_one():
    foods = load_data()
    allergen_ingredients = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in allergen_ingredients:
                allergen_ingredients[allergen] = set(ingredients)
            else:
                allergen_ingredients[allergen] = (
                    allergen_ingredients[allergen] & (set(ingredients)))
    allergen_to_ingredient = {}
    while len(allergen_ingredients):
        for allergen in allergen_ingredients:
            if len(allergen_ingredients[allergen]) == 1:
                ingredient_found = allergen_ingredients.pop(allergen)
                allergen_to_ingredient[allergen] = list(ingredient_found)[0]
                for ingredients in allergen_ingredients.values():
                    ingredients -= ingredient_found
                break
    total = 0
    print(len([ingredient
               for ingredients, allergens in foods
               for ingredient in ingredients
               if ingredient not in allergen_to_ingredient.values()]))
    return allergen_to_ingredient


def part_two():
    allergen_to_ingredient = part_one()
    print(','.join([allergen_to_ingredient[allergen]
                    for allergen in sorted(allergen_to_ingredient)]))


# part_one()
part_two()

print("--- %s seconds ---" % (time.time() - start_time))
