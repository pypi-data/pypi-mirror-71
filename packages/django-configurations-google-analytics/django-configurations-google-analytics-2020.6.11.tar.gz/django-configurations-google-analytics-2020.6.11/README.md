<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/v/django-configurations-google-analytics.svg?maxAge=3600)](https://pypi.org/project/django-configurations-google-analytics/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-configurations-google-analytics.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-configurations-google-analytics.py/)

#### Installation
```bash
$ [sudo] pip install django-configurations-google-analytics
```

##### `settings.py`
```python
from django_configurations_google_analytics import GoogleAnalyticsConfiguration

class Base(GoogleAnalyticsConfiguration,...):
    # GA_ID = 'UA-XXXXXXXX-Y'
```

##### `.env`
```bash
DJANGO_GA_ID="UA-XXXXXXXX-Y"
```

#### Templates
```html
{% load google_analytics %}
...
{% google_analytics %}
```

#### Links
+   [django-configurations](https://github.com/jazzband/django-configurations)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>