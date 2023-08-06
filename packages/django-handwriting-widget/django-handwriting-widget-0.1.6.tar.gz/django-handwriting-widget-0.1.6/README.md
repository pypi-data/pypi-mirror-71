# Django Handwriting Widget

[![CircleCI](https://circleci.com/gh/arthurc0102/django-handwriting-widget.svg?style=svg)](https://circleci.com/gh/arthurc0102/django-handwriting-widget)

> A handwriting widget for django  

## Installation

Install with `pip`

```
pip install django-handwriting-widget
```

Add this app to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    ...
    'handwriting',
]
```

## Usage

[Example model](e_signatures/models.py)

### Form

```python
from django import forms

from handwriting.forms import HandwritingPad

from .models import Signature


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = '__all__'
        widgets = {
            'image': HandwritingPad(),
        }
```

### Admin

```python
from django.contrib import admin

from handwriting.admin import HandwritingPadModelAdmin

from .models import Signature


@admin.register(Signature)
class SignatureAdmin(HandwritingPadModelAdmin):
    list_display = ('name', 'create_at')
```

or 

```python
from django.contrib import admin

from handwriting.admin import HandwritingPadAdminMixin

from .models import Signature


@admin.register(Signature)
class SignatureAdmin(HandwritingPadAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'create_at')
```

or

```python
from django.contrib import admin

from .forms import SignatureForm
from .models import Signature


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    form = SignatureForm
    list_display = ('name', 'create_at')
```
