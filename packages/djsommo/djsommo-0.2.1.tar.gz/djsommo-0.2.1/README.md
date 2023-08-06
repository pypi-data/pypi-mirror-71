# djsommo

Django safe optional model `Meta` options.

Django doesn't support adding third-party fields to the model class Meta.
It raises an exception if one is encountered.

Many installable apps inject a model `Meta` option name into Django
during initialisation, after which it is safe to use them.

However what happens if the installable app isnt working for some reason,
and you want to disable it.

Then you need to remove all use of the `Meta` option from the models.

This app provides a `Meta` class which detects unknown options,
issues a warning and discards them before Django can raise an exception.

## Usage

In `models.py`

```py
from django.db import models

from djsommo import SafeOptionalMeta


class MyModel(models.Model):
    uuid = models.TextField()
    ...
    class Meta(SafeOptionalMeta):
        unknown_option = True
```
