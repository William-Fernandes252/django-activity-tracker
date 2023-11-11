# Django Activity Tracker

[![pypi](https://img.shields.io/pypi/v/django-activity-tracker.svg)](https://pypi.org/project/django-activity-tracker/)
[![python](https://img.shields.io/pypi/pyversions/django-activity-tracker.svg)](https://pypi.org/project/django-activity-tracker/)
[![Build Status](https://github.com/William-Fernandes252/django-activity-tracker/actions/workflows/dev.yml/badge.svg)](https://github.com/William-Fernandes252/django-activity-tracker/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/William-Fernandes252/django-activity-tracker/branch/main/graphs/badge.svg)](https://codecov.io/github/William-Fernandes252/django-activity-tracker)

A reusable Django application to track user actions through the database.

-   Documentation: <https://William-Fernandes252.github.io/django-activity-tracker>
-   GitHub: <https://github.com/William-Fernandes252/django-activity-tracker>
-   PyPI: <https://pypi.org/project/django-activity-tracker/>
-   Free software: MIT

## Introduction

I once worked on a project where user interactions about business entities needed to be recorded, in a detailed and consistent manner, in the database for auditing reasons. When a user changed the state of an object, the change, along with its author and time, should be saved. Furthermore, the object in question should be easily located. As I came up with a conveniently generic solution, I decided to turn this into a reusable application for Django projects.

Currently it works only in [Django REST Framework](https://www.django-rest-framework.org/) projects, and with [`ModelViewSet`s](https://www.django-rest-framework.org/api-guide/viewsets/), but in the future I plan to support Django CBVs and view functions as well.

## Features

-   Track users interations with any model of your project in a _generic_ way;
-   Retrive and protect this information;
-   Use the full capabilities of the Django ORM to gather information about what a specific user did to an object, what users interacted with it, and more!

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
