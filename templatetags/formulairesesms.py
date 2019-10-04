from __future__ import unicode_literals
from django import template
from django.apps import apps
from django import forms

register = template.Library()


@register.simple_tag
def fait_choix(id, choixs, *args, **kwargs):
    name = "q" + str(id)
    liste = choixs
    question = forms.Select(choices=liste, attrs={'id': id ,'name': name, })

    return question.render(name, '')


@register.simple_tag
def verbose_name_tag(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name
