<h1 align = "center">
    Visitor Management System
</h1>

---

<img alt="PyPI - Python Version" src="https://img.shields.io/badge/python%20vesion-3.8.2-green"> <img alt="PyPI - Django Version" src="https://img.shields.io/badge/django%20version-3.0.6-blue">

<p>
<img src = "VMS.png">
</p>

<h1>Table of Content</h1>

- [Introduction](#introduction)
- [Technology Stack](#technology-stack)
- [Installations and Running](#installations-and-running)
- [Contributors](#contributors)



## Introduction

---

Vistior Management System, also known as <strong>VMS</strong>, is a System to guide visitors who are visiting the college.
This System helps to track the number of visitors who come to your place.

## Technology Stack

---

- HTML/CSS/JavaScript
- Bootstrap
- Django
- Sqlite3

## Installations and Running

---

- Clone this repository

  ```
  git clone https://github.com/parth-27/Visitor-Management-System.git
  ```

- If you are not going to use Sqlite3 Database, change the DATABASES variable in settings.py file accordingly. You can Refer to [Django documentation](https://docs.djangoproject.com/en/3.0/ref/databases/)

- Please Don't forgot to add the <strong> Email </strong> and <strong>Password </strong> in <strong> settings </strong> file from which you want to send confirmation mail or visitor pass mail. Path to the settings file is <strong> visitor_manage/visitor_manage/settings.py </strong>

- Also add your own API key in the location.html file and path to the file is <strong>visitor_manage/src/templates/src/location.html </strong>

- Make Initial Migrations

  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```

- Run the Website on LocalHost
  ```
  python3 manage.py runserver
  ```

- Name and Password both for the SuperAdmin of the website is <strong>superadmin</strong>

Licensed under the [MIT License](LICENSE).

## Contributors

| [Parth Patel](https://github.com/parth-27)                                                                                                            
| [Dipika Pawar](https://github.com/DipikaPawar12)
