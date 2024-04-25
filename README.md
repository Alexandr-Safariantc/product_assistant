<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<div align='center'>
  <a href="https://www.python.org/" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/skills/python-colored.svg" height="95" alt="Python">
  </a>
  <a>
    <img src="https://cdn.pixabay.com/photo/2024/02/18/16/10/soda-8581561_1280.png" height="110" alt="Fridge" hspace="0">
  </a>
  </a>
  <a>
    <img src="https://cdn.pixabay.com/photo/2014/12/21/23/28/recipe-575434_1280.png" height="100" alt="Database" hspace=10>
  </a>

<h3 align="center">Foodgram</h3>

  <p align="center">
    A simple app to find new amaizing recipes
    <br />
    <a href="#getting-started"><strong>--> Quick start <--</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#features">Features</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Get project">Get project</a></li>
        <li><a href="#Run as python script">Run as python script</a></li>
        <li><a href="#Setting up CI/CD pipeline on GitHub Actions">CI/CD pipeline</a></li>
        <li><a href="#Secrets">Secrets</a></li>
      </ul>
    </li>
    <li><a href="#explanation">Explanations</a></li>
    <li><a href="#restrictions">Restrictions</a></li>
    <li><a href="#contacts">Contact</a></li>
  </ol>
</details>

## Features
- Addind your fantastic recipes to feed and show them for other users.
- Editing post with your recipe if you want to make it perfect.
- Watching other users' recipes and adding them to your favorites.
- Following to authors which you like and watching their new recipes first.
- Adding recipes to shopping list and download file with ingredients for cooking them.

## Built With
![](https://img.shields.io/badge/python-3.9.19-blue)
![](https://img.shields.io/badge/Django-3.2.3-blue)
![](https://img.shields.io/badge/DRF-3.12.4-blue)
![](https://img.shields.io/badge/PostgreSQL-13.10-blue)
![](https://img.shields.io/badge/djoser-2.1.0-blue)
![](https://img.shields.io/badge/Node.js-13.12.0-blue)
![](https://img.shields.io/badge/nginx-1.22.1-blue)
![](https://img.shields.io/badge/gunicorn-20.1.0-blue)

[![Main Foodgram workflow](https://github.com/Alexandr-Safariantc/foodgram/actions/workflows/main.yml/badge.svg)](https://github.com/Alexandr-Safariantc/foodgram/actions/workflows/main.yml)

# Getting Started

## Get project

#### Go to <a href="https://kaif.artof.dev/">Project</a>

#### Get <a href="https://kaif.artof.dev/api/docs/">API documentation</a>

## Run as python script
### Prerequisites

* python **3.9.19**
* pip

### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/Alexandr-Safariantc/foodgram
   ```
2. Activate virtual environment
   ```sh
   $ cd foodgram
   $ python3 -m venv venv
* for Linux/macOS
    ```sh
    $ source .venv/bin/activate
    ```
* for windows
    ```sh
    $ source .venv/scripts/activate
    ```

3. Upgrage pip
    ```sh
    (venv) $ python3 -m pip install --upgrade pip
    ```

4. Install requirements
    ```sh
    (venv) $ cd backend/
    (venv) $ pip install -r requirements.txt
    ```

5. Migrate database
    ```sh
    (venv) $ python3 manage.py migrate
    ```

6. Add test data to database
    ```sh
    (venv) $ python3 manage.py import_csv
    ```

7. Run app
    ```sh
    (venv) $ python3 manage.py runserver
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Setting up CI/CD pipeline on GitHub Actions

- Fork this repository on GitHub
- Configure secrets for your project in GitHub UI
- Add a remote origin to the local repo
- Configure .env secrets
- Push the code
- Open the GitHub Actions for your project to verify the state of the deployment pipeline

### Secrets
#### GitHub secrets

`DOCKER_PASSWORD`: your password for https://hub.docker.com/<br>
`DOCKER_USERNAME`: your username for https://hub.docker.com/<br>
`HOST`: IP address of server you want to deploy<br>
`SSH_KEY`: SSH key for deploy server access<br>
`SSH_PASSPHRASE`: passphrase for deploy server access<br>
`USER`: login for deploy server access<br>
`TELEGRAM_TOKEN`: Telegram bot's authorization token that will send the message<br>
`TELEGRAM_TO`: Unique identifier for chat you want to get message with deploy info

#### .env secrets

`ALLOWED_HOSTS`: {IP address of server you want to deploy},127.0.0.1,localhost,{your domane name if exists}<br>
`DEBUG_VALUE`: if not setted debug mode is off, **not required**<br>
`DB_HOST`: your PostgreSQL db host name<br>
`DB_PORT`: your PostgreSQL db port, **not required**<br>
`POSTGRES_DB`: your PostgreSQL db host name, **not required**<br>
`POSTGRES_PASSWORD`:your PostgreSQL db password access<br>
`POSTGRES_USER`:your PostgreSQL db username access, **not required**<br>
`SECRET_DJANGO_KEY`: secret key for Django app<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Explanation
### Database Structure

  `Recipe` <br>
  Contains recipe's author, cooking_time, created_at, image, name, ingredients, tags, text.

  `Ingredient` <br>
  Contains recipe ingredients' name, measurement_unit.

  `Tag` <br>
  Contains recipe tags' name, color, slug.

  `IngredientRecipe` <br>
  Linked model for ingredient - recipe relation, moreover contains ingredient amount.

  `TagRecipe` <br>
  Linked model for tag - recipe relation.

  `Follow` <br>
  Process following to recipe authors.

  `Favorite` <br>
  Proccess adding recipes to favorites, moreover contains created_at.

  `ShoppingCartRecipe` <br>
  Proccess adding recipes to user's shopping cart and download ingredients list for chosen recipes cooking.

## Restrictions

**1. Media files size** <br>
We know that you can share lots of delishes recipes so we have to set the maximum media files size for 20M to ensure all your wonderful dishes are featured in our feed.

**2. Recipe's cooking time limits** <br>
Cooking time can't be less then 1 minute, isn't it? Too high values are also restricted.

**3. Recipe's ingredient amount limits** <br>
Limits are same as for cooking time.

**4. Tags are required** <br>
We really want to meet your expectations so to make it easier and faster to find the needed recipe you have to add at least one tag to your recipe.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contacts

**Alexandr Safariants** Backend developer

[![Gmail Badge](https://img.shields.io/badge/-safariantc.aa@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:safariantc.aa@gmail.com)](mailto:safariantc.aa@gmail.com)<p align='left'>

<p align="right">(<a href="#readme-top">back to top</a>)</p>