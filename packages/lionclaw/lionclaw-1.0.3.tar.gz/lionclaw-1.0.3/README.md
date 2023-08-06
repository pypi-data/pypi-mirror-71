# Longclaw


[![Pypi Version](https://badge.fury.io/py/longclaw.svg)](https://badge.fury.io/py/longclaw)
[![Codecov Status](https://codecov.io/gh/JamesRamm/longclaw/branch/master/graph/badge.svg)](https://codecov.io/gh/JamesRamm/longclaw)
[![Build Status](https://travis-ci.org/JamesRamm/longclaw.svg?branch=master)](https://travis-ci.org/JamesRamm/longclaw)
[![Code Health](https://landscape.io/github/JamesRamm/longclaw/master/landscape.svg?style=flat)](https://landscape.io/github/JamesRamm/longclaw/master)

An e-commerce extension for [Wagtail CMS](https://github.com/wagtail/wagtail)


![Image of the dashboard](docs/assets/dashboard.png)

## Quickstart

Install Lionclaw:

```bash
  $ pip install lionclaw
```

Setup a Lionclaw project

```bash
  $ lionclaw start my_project
```

Go to project directory and create missing migrations 

```bash
  $ python manage.py makemigrations home catalog
```

Do migrations for whole project and run 

```bash
  $ python manage.py migrate
  $ python manage.py loadcountries
  $ python manage.py createsuperuser
  $ python manage.py runserver
```

## Features

- Tightly integrated with Wagtail. Create products, manage orders, configure shipping and view statistics all from the Wagtail admin.
- Multiple payment backends. Longclaw currently supports Stripe, Braintree and PayPal (v.zero) payments.
- Comprehensive REST API & javascript client easily loaded via a template tag
- Create your catalogue as Wagtail pages, with complete control over your product fields
- Easy setup. Just run `lionclaw start my_project` to get going
- Simple to use, simple to change. Write your frontend as you would any other wagtail website. No complicated overriding, forking etc in order to customise behaviour.


### Screenshots

![Order Detail](docs/assets/order_detail.png)


## Support


Please raise bugs/feature requests using the github issue tracker and ask questions on stackoverflow.
For further support contact us
