# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Ressource, Equipe, Esms, Document
from django.forms import inlineformset_factory


class EsmsForm(forms.ModelForm):
    class Meta:
        model = Esms
        fields = ('nombre', 'clientele', 'autreinfo', 'autresservices')
        exclude = ()


class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        exclude = ('author','province')


class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        exclude = ()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ()


RessourceFormSet = inlineformset_factory(Ressource, Equipe, form=RessourceForm,
                                         extra=3, can_delete=True)

DocumentFormSet = inlineformset_factory(Ressource, Document, form=DocumentForm,
                                         extra=2, can_delete=True)

EsmsFormSet = inlineformset_factory(Ressource, Esms, form=EsmsForm,
                                         extra=0, can_delete=True)