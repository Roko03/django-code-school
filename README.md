# Django Code School Project

![](./backend/public/django-backend.gif)

Basic Django REST API project created for [Code school app](https://github.com/Roko03/code-school). Includes:
- Authentication route providing [JWT token](https://jwt.io/)
- Routes for managing users, organizations and workshops

## Time Spent

I need 60-70 hours of work to make this project.
## How to Use

Make sure you have the following installed on your computer:

- [git](https://git-scm.com/)
- [node.js](https://nodejs.org/en)
- [npm](https://www.npmjs.com/)

Clone the repository

```bash
git clone https://github.com/Roko03/django-code-school.git
```
Set up virtual enviroment and install package

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

Changing models and create database schema

```bash
pyhton manage.py makemigrations
python manage.py migrate
```

Create superuser

```bash
python3 manage.py createsuperuser
```

Running the Project

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000/) to view the project
