### Hexlet tests and linter status:
[![Actions Status](https://github.com/Acemore/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Acemore/python-project-83/actions)
[![linter-check](https://github.com/Acemore/python-project-83/actions/workflows/linter.yml/badge.svg)](https://github.com/Acemore/python-project-83/actions/workflows/linter.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/2392e743a0093c6236fd/maintainability)](https://codeclimate.com/github/Acemore/python-project-83/maintainability)

**Page analyzer** is web app for analyzing websites for SEO suitability

## Deployment

**Page analyzer** is deployed on **Railway**:

https://python-project-83-production-45c8.up.railway.app/

## To run Page Analyzer

Clone repo: 

```bash
git clone git@github.com:Acemore/python-project-83.git
```

Create .env file in root project dir and add local environment variables:

```
SECRET_KEY = <your secret key>
DATABASE_URL = <your Postgres Connection URL>
```

Install dependencies:

```bash
make install
```

Launch server with the app:

```bash
make start
```

Go to address http://localhost:8000/ or http://127.0.0.1:8000/