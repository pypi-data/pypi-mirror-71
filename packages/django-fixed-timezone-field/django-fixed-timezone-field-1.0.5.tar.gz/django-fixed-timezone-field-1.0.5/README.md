# django-fixed-timezone-field

## What problem does this solve?

[There's a detailed description here](https://matix.io/django-fixed-timezone-dates-datetimes/).

## Installation

`pip install django-fixed-timezone-field`

## Usage

Basic example:

```python
from django import forms
from django.db import models
from fixed_timezone_field import FixedTimezoneDateTimeField
import pytz


class Event(models.Model):
	starts_at = models.DateTimeField()


class EventForm(forms.ModelForm):
	starts_at = FixedTimezoneDateTimeField()

	class Meta:
		model = Event
		fields = ['starts_at']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['starts_at'].timezone = pytz.UTC # or whatever timezone you want
```

If the model also contains the timezone, and the same form is used to submit both the timezone and the time, you need to use some other tricks.

```python
from django import forms
from django.db import models
from fixed_timezone_field import FixedTimezoneDateTimeField
from timezone_field import TimeZoneField
import pytz


class Event(models.Model):
	starts_at = models.DateTimeField()
	timezone = TimeZoneField()


class EventForm(forms.ModelForm):
	starts_at = FixedTimezoneDateTimeField()

	class Meta:
		model = Event
		fields = ['starts_at']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['starts_at'].timezone = self.instance.timezone

	def clean(self, *args, **kwargs):
		cleaned_data = super().clean(*args, **kwargs)
		timezone = cleaned_data['timezone']
		cleaned_data['starts_at'] = tz.localize(cleaned_data['starts_at'].replace(tzinfo=None))
		self.instance.starts_at = cleaned_data['starts_at']
		return cleaned_data
```
