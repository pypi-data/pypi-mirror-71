<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/v/django-configurations-apps.svg?maxAge=3600)](https://pypi.org/project/django-configurations-apps/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-configurations-apps.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-configurations-apps.py/)

#### Installation
```bash
$ [sudo] pip install django-configurations-apps
```

#### Features
key  | default value  | env
-|-|-
`INSTALLED_APPS` | `[]` | `DJANGO_INSTALLED_APPS`
`INSTALLED_APPS_FILE` | `None` | `DJANGO_INSTALLED_APPS_FILE`
`INSTALLED_APPS_FIND` | `True` | `DJANGO_INSTALLED_APPS_FIND`  ('yes', 'y', 'true', '1')

##### `settings.py`
```python
from django_configurations_apps import AppsConfiguration

class Base(AppsConfiguration,...):
    INSTALLED_APPS_FILE = 'apps.txt'
    INSTALLED_APPS_FIND = True # default True
```

`apps.txt`
```
django.contrib.admin
django.contrib.auth
django.contrib.contenttypes
django.contrib.sessions
django.contrib.messages
django.contrib.sites
django.contrib.staticfiles

django_gravatar
```

##### `.env`
```bash
DJANGO_APPS_FILE='apps.txt' # optional
DJANGO_APPS_FIND=true # optional
DJANGO_INSTALLED_APPS=app1,app2 # optional
```

#### Examples
`apps.txt`
```
django.contrib.admin
django.contrib.auth
django.contrib.contenttypes
django.contrib.sessions
django.contrib.messages
django.contrib.sites
django.contrib.staticfiles

django_gravatar
```

#### Links
+   [django-configurations](https://github.com/jazzband/django-configurations)
+   [django-find-apps](https://pypi.org/project/django-find-apps/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>