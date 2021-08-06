# gonews-back
Backend (API + Admin) for gonews web
This project used Django and Django-rest Frameworks.

## Requirements

- python3
- pip
- python-dev

### Database
- Mysql

### Production
- Web server, like Apache or Nginx

## Setup
`gonewsBack/settings.py` Contains all settings for the project.
### Important:
_Set Database credentials before installation step._

## Installation

(optional) Create Virtualenv and Active.

1. Run `python pip install -r requirements.txt` on main directory.
2. Run `python manage.py migrate`.
3. Run `python manage.py createsuperuser` for create a first user with all privileges.

## Run 
- Run `python manage.py runserver` this run development server of django

## Production
Make sure run `python manage.py collectstatics` before go to porduction, this copy all static files to `staticfiles` folder on root of projects and make it accessible for anothers webservers.



# API END POINTS
- Get all notes
  - `notes/`
- Filter by category
  - `notes/?category=<category_Slug>`
- Search (by title o Tags)
  - `notes/?search=<String>`
- Get an specific note(including body) 
  - `note/<note_slug>`

- get menu list (is divided on main and second, each one with your top note)
  - `menu/`

- Get Home config. Return 3 items:
 `main`: Is destaque note of all site.
 `latests`: notes with `last news` tag. 
 `categories` : JSON with all categories and our respectives notes with tag `top`
  - `home/`

- Get Banners: if `category_slug` is null  return set of banner for individual note.
  -`banner/:<category_slug>`



# Code Structure
- `upload` and `mediafiles` folders = *Inactives*, replace by S3 bucket storage
- `gonewsBack` = Django project Folder
  - `statics` : Contain all static files (js, css, images) used by custom templates of project
  - `templates`: Contain all custom or overwrited templates of project.
  - `settings.py`: contain all configurations for the entired project.
  - `urls.py` : set the urls for entired project
  - `wsgi.py` : used by gunicorn for launch project on porduction.

- `api` = Application Folder
  - `statics` : Contain all static files (js, css, images) used by specific app.
  - `templates`: Contain all custom or overwrited templates of the app.
  - `admin.py`: classes for admin pages of the app
  - `customAdminViews.py`: some custom views uses by custom pages of admin (Home and Menu)
  - `models.py`: Define all models of the app (this is read for create news migrations)
  - `serializers.py`: Define all serializers used by `Django-rest` framework.
  - `urls.py`: Define routes of the app
  - `utils.py`: define some utils functions used on anothers classes or modules.
  - `views.js`: Define all Rest views with `Django-rest`.
