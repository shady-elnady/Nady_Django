
# [Nady System For Laboratories] 


> ### [Nady-Back-End-Django]() codebase containing (CRUD, auth, advanced patterns, etc) .

A Graphql server implementation using [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/#graphene-django)

<img src="logo.png" height="200" width="400"/>

This codebase was created to demonstrate a fully fledged fullstack application built with Django including CRUD operations, authentication, routing, pagination, and more.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.
## Screenshots

<img src="article_query.png" width="800" height="400"/>

<img src="add_article.png" width="800" height="400"/>

<img src="add_comment.png" width="800" height="400"/>

<img src="get_profile.png" width="800" height="400"/>

<img src="current_user.png" width="800" height="400"/>

# How it works
A Graphql Implementation using facebook relay specs

Full graphql schema can be found at [`schema.graphql`]()

**Folder Structure:**
1) `GraphQL`: contains all core functionalites ex (BaseModel, BaseMutation)
2) `User` contains user related mutation, models, types, queries
3) `Article` contains all article related models, mutation, types, queries
4) `Config` contains all django urls, settings, and others.

# Getting started

1) Install dependancies
`poetry install`

2) create `.env` file with this content
`DEBUG=True ` 
`SECRET_KEY=test-secret-key`
 `DATABASE_URL=mongodb://localhost:27017`
 3) run migration
 `poetry run python manage.py migrate`
4) run server
`poetry  run python manage.py runserver 8000`
5) open graphql playground using http://localhost:8000/playground
6) to connect to it via API use http://localhost:8000/graphql


## Third Party Packages
1) `graphene-django`: Add Graphql to a django server
2) `python-decouple`: manage django settings using .env file
3) `django-graphql-jwt`: Add JWT authentication
4) `graphene-django-optimizer`: Optimize database queries to avoid N+1 problem
5) `graphene-file-upload`: Add mutlipart file upload mutations to graphene

### Testing
some tests were added to `tests` directory, packages used for testing:
1) `pytest`
****
