"""Tests for the starter Recipe & Meal Planner."""

import json
import app

from recipe_utils import (
    Search_by_Ingredient,
    filter_by_category,
    load_config,
    load_recipes,
    search_by_name,
)


def test_search_by_name_finds_partial_match():
    recipes = [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Berry Smoothie", "category": "Snack"},
    ]
    result = search_by_name(recipes, "chicken")
    assert result == [{"name": "Chicken Alfredo", "category": "Dinner"}]


def test_search_by_name_is_case_insensitive():
    recipes = [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Berry Smoothie", "category": "Snack"},
    ]
    result = search_by_name(recipes, "SMOOTHIE")
    assert result == [{"name": "Berry Smoothie", "category": "Snack"}]


def test_search_by_name_returns_empty_list_when_no_match():
    recipes = [{"name": "Chicken Alfredo", "category": "Dinner"}]
    assert search_by_name(recipes, "pizza") == []


def test_search_by_ingredient_finds_partial_match():
    recipes = [
        {
            "name": "Chicken Alfredo",
            "ingredients": [{"name": "Chicken breast"}],
        },
        {"name": "Berry Smoothie", "ingredients": [{"name": "Blueberries"}]},
    ]
    assert Search_by_Ingredient(recipes, "chick") == [recipes[0]]


def test_search_by_ingredient_is_case_insensitive_and_trims_whitespace():
    recipes = [
        {
            "name": "Olive Pasta",
            "ingredients": [{"name": "Extra Virgin Olive Oil"}],
        }
    ]
    assert Search_by_Ingredient(recipes, "  OLIVE OIL  ") == recipes


def test_search_by_ingredient_returns_empty_list_when_no_match():
    recipes = [{"name": "Berry Smoothie", "ingredients": [{"name": "Banana"}]}]
    assert Search_by_Ingredient(recipes, "spinach") == []

def test_random_meal_suggestion_handles_empty_recipe_list(capsys):
    app.Random_Meal_Suggestion([])

    assert "No recipes found." in capsys.readouterr().out

def test_random_meal_suggestion_displays_randomly_selected_recipe(monkeypatch):
    recipes = [
        {"name": "First recipe"},
        {"name": "Second recipe"},
    ]
    selected_recipe = recipes[1]
    displayed = []

    monkeypatch.setattr(app.random, "choice", lambda choices: selected_recipe)
    monkeypatch.setattr(app, "display_recipe", displayed.append)

    app.Random_Meal_Suggestion(recipes)

    assert displayed == [selected_recipe]

def test_filter_by_category_returns_matching_recipes():
    recipes = [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Berry Smoothie", "category": "Snack"},
        {"name": "Tomato Pasta", "category": "Dinner"},
    ]
    result = filter_by_category(recipes, "Dinner")
    assert result == [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Tomato Pasta", "category": "Dinner"},
    ]


def test_filter_by_category_is_case_insensitive():
    recipes = [{"name": "Chicken Alfredo", "category": "Dinner"}]
    assert filter_by_category(recipes, "dinner") == [
        {"name": "Chicken Alfredo", "category": "Dinner"}
    ]


def test_load_config_reads_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(
        json.dumps(
            {
                "app_title": "Test Planner",
                "recipe_file": "recipes.json",
                "default_servings": 2,
            }
        ),
        encoding="utf-8",
    )
    result = load_config(config_file)
    assert result["app_title"] == "Test Planner"
    assert result["default_servings"] == 2


def test_load_recipes_reads_json(tmp_path):
    recipe_file = tmp_path / "recipes.json"
    sample = [
        {
            "name": "Test Recipe",
            "category": "Lunch",
            "servings": 2,
            "prep_time": 5,
            "cook_time": 10,
            "ingredients": [],
        }
    ]
    recipe_file.write_text(json.dumps(sample), encoding="utf-8")
    assert load_recipes(recipe_file) == sample
