# Collection Model Admin

## Installation

```shell script
pip install wagtail-collectionmodeladmin
```

## Development

Checkout this repo, create a local virtual environment and install dependencies:
```shell script
pip install -e .
```

Create a new `demo` wagtail project:
```shell script
wagtail start demo
```

We will use the `home` app as the base for our demo. Add a new `Model` in `demo/home/models.py`:
```python
from django.db import models

from wagtail.core.models import CollectionMember


class Demo(CollectionMember, models.Model):
    demo_field = models.CharField()
```

Add the `wagtail.contrib.modeladmin` to the demo `INSTALLED_APPS` at `demo/demo/settings/base.py`:
```python
INSTALLED_APPS = [
   ...
   'wagtail.contrib.modeladmin',
]
```

Create the wagtail hooks that will inject the model admin in `demo/home/wagtail_hooks.py`:
```python
from wagtail.contrib.modeladmin.options import modeladmin_register

from collectionmodeladmin.base import CollectionModelAdmin
from home.models import Demo


class DemoModelAdmin(CollectionModelAdmin):
    model = Demo


modeladmin_register(DemoModelAdmin)
```

Then as usual make migrations, apply them, create a superuser and start the Django server.
```shell script
cd demo
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```