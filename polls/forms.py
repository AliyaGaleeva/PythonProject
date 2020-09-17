from django import forms
from django.utils.translation import ugettext as _

# получение адреса из формы
class IndexForm(forms.Form):
    long_address = forms.CharField(label=_(u'long url'), max_length=30)
