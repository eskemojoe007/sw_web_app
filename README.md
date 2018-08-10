# sw_web_app
[![CircleCI](https://circleci.com/gh/eskemojoe007/sw_web_app.svg?style=shield)](https://circleci.com/gh/eskemojoe007/sw_web_app)

## Background
Why this project?  A couple of reasons:

- I wanted to learn to make a full stack real website myself...so I chose something I actually care about.
- I fly a lot of SW, so I wanted to enable my multi-airport and multi-date search options (eventually adding complexity)

From reading blogs and other online resources, I settled on using `django` to power the backend, `vue` to power the front end, and a `rest-api` to communicate between.  There are other technologies used, but these describe the basics.


## Contributing
I use this paradigm for keeping my github branches clean: https://nvie.com/posts/a-successful-git-branching-model/?

All master commits should be done through pull requests through the develop branch.  CircleCI is used to check all passing requirements.

As this project is still in infancy, the master branch is often quite outdated.

## Installation (Locally) and setup

### Django Backend
I use `pipenv` for everything.  To install follow these steps:

1. Install python 3-64 bit.
2. Install pipenv globablly `pip install pipenv`
3. Clone this repository
4. In the repository run `pipenv install --dev`

#### Launching the server
within the `sw_site` folder run `pipenv run python manage.py runserver`

#### Running all the tests
within the `sw_site` folder run `pipenv run python -m pytest`

#### Deploy the backend using Heroku
`git push heroku master`

or use `git push heroku develop:master` to deploy `develop` branch

### Vue CLI Frontend
I power the vue front end with `npm` and [vue clie](https://cli.vuejs.org/).  

After installing `npm`, runing `npm install` in the `frontend` directory should install all the `node.js` requirements.

#### Launching the frontend server
runing `npm run serve` in the `frontend` folder will run the front end.  You often need the backend temp server running as well ( to connect and pull proper data)

#### Running Tests
`npm run test:unit` from within the `frontend` folder.

#### Deploy Frontent
`npm run build`
`surge dist/ sw.davidfolkner.com`
