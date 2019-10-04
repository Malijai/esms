# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from esms.esms_constants import CHOIX_FINAL, EXPLICATIONSFR, EXPLICATIONSEN, CHOIXEN, CHOIXFR
from .forms import RessourceFormSet, RessourceForm, EsmsForm, DocumentFormSet, EsmsFormSet
from .models import Ressource, Equipe, Esms
from django.views import generic
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.core.paginator import InvalidPage
from django.utils import translation
from esms.paginationalpha import NamePaginator
from django.utils.translation import ugettext_lazy as _


@login_required(login_url=settings.LOGIN_URI)
def faitinstitution(request, pk, choix='', histoire=''):
    # 'b': {'name': 'Génériques aigus', 'choices': ['c', 'd']},
    langue = translation.get_language()

    if langue == 'fr':
        CHOIX = CHOIXFR
        EXPLICATIONS = EXPLICATIONSFR
    else:
        CHOIX = CHOIXEN
        EXPLICATIONS = EXPLICATIONSEN
    ressource = Ressource.objects.get(pk=pk)
    liste = ('z', 'o', 'x', 'qq', 'rr', 'ss')
    if not choix:
        entrees = [(c, CHOIX[c]['name'], EXPLICATIONS[c]) for c in liste]
        return render(
            request,
            'classification_esms.html',
                {'choisi': '',
                 'choixs': '',
                 'choixprecedent': '',
                 'historiques': '',
                 'dernier': '',
                 'dernier2': '',
                 'entrees': entrees,
                 'ressource': ressource,
                 'langue': langue
                 }
            )
    else:
        choisi = CHOIX[choix]['name']
        choixs = []
        historiques = []
        choixprecedent = histoire + choix
        dernier = ''
        dernier2 = ''
        code = ''
        if len(CHOIX[choix]['choices']) > 0:
            choixs = [(c, CHOIX[c]['name'], EXPLICATIONS[c]) for c in CHOIX[choix]['choices']]
        else:
            dernier = choisi
            dernier2 = CHOIX_FINAL[choixprecedent]
            code = choixprecedent
        for a in histoire:
            if a == choix:
                dernier = CHOIX_FINAL[histoire]
            else:
                historiques.append(CHOIX[a]['name'])
        if dernier:
            if request.method == 'POST':
                form = EsmsForm(request.POST)
                if form.is_valid():
                    codeder = form.save(commit=False)
                    codeder.ressource = ressource
                    codeder.code = request.POST.get('code')
                    codeder.save()
                    textemessage = _(u"{}  a été codée {}").format(ressource.nom,dernier2)
                    messages.add_message(request, messages.WARNING, textemessage)
                    return redirect('listeressources')
        return render(
                    request,
                    'classification_esms.html',
                    {'choisi': choisi,
                     'choixs': choixs,
                     'choixprecedent': choixprecedent,
                     'historiques': historiques,
                     'dernier': dernier,
                     'dernier2': dernier2,
                     'entrees': '',
                     'ressource': ressource,
                     'code': code,
                     'esms_form': EsmsForm()
                     }
                )


@login_required(login_url=settings.LOGIN_URI)
def ressource_new(request):
    entete = "Nouvelle ressource"
    if request.method == "POST":
        form = RessourceForm(request.POST)
        prof_instances = RessourceFormSet(request.POST)
        doc_instances = DocumentFormSet(request.POST)

        if form.is_valid() and prof_instances.is_valid() and doc_instances.is_valid():
            entree = form.save(commit=False)
            entree.author = request.user
            entree.province_id = request.user.profile.province
            entree.save()
            # Now save the data for each form in the formset
            new_prof = []
            for prof_form in prof_instances:
                profession = prof_form.cleaned_data.get('profession')
                nombre = prof_form.cleaned_data.get('nombre')
                tache = prof_form.cleaned_data.get('tache')
                duree = prof_form.cleaned_data.get('duree')
                if profession:
                    new_prof.append(Equipe(ressource=entree, profession=profession, nombre=nombre, tache=tache, duree=duree))
            try:
                with transaction.atomic():
                    Equipe.objects.bulk_create(new_prof)
                    # And notify our users that it worked
                    messages.success(request, _(u"L'équipe est enregistrée."))

            except IntegrityError:  # If the transaction failed
                messages.error(request, _(u"Il y a une erreur dans l'enregistrement de l'equipe."))
                ress_form = RessourceForm()
                prof_formset = RessourceFormSet()
                doc_formset = DocumentFormSet()
                context = {
                    'form': ress_form,
                    'prof_formset': prof_formset,
                    'doc_formset': doc_formset,
                    'entete': entete
                }
                return render(request, "ressource_edit.html", context)
            new_doc = []
            for doc_form in doc_instances:
                titrecourt = doc_form.cleaned_data.get('titrecourt')
                documentation = doc_form.cleaned_data.get('documentation')

                if documentation:
                    new_doc.append(Equipe(ressource=entree, titrecourt=titrecourt, documentation=documentation))
            try:
                with transaction.atomic():
                    Equipe.objects.bulk_create(new_doc)
                    # And notify our users that it worked
                    messages.success(request, _(u"La documentation est enregistrée."))

            except IntegrityError:  # If the transaction failed
                messages.error(request, _(u"Il y a une erreur dans l'enregistrement de la documentation."))
                ress_form = RessourceForm()
                prof_formset = RessourceFormSet()
                doc_formset = DocumentFormSet()
                context = {
                    'form': ress_form,
                    'prof_formset': prof_formset,
                    'doc_formset': doc_formset,
                    'entete': entete
                }
                return render(request, "ressource_edit.html", context)
            if 'Savesurplace' in request.POST:
                return redirect(ressource_edit, entree.id)
            else:
                return redirect('ressource_detail', entree.id)
        else:
            ress_form = RessourceForm()
            prof_formset = RessourceFormSet()
            doc_formset = DocumentFormSet()
            context = {
                'form': ress_form,
                'prof_formset': prof_formset,
                'doc_formset': doc_formset,
                'entete': entete
            }
            return render(request, "ressource_edit.html", context)
    else:
        #  return render(request, "entree_edit.html", {'form': form, 'tags':tag_list, 'groupes':group_list,})
        ress_form = RessourceForm()
        prof_formset = RessourceFormSet()
        doc_formset = DocumentFormSet()
        context = {
            'form': ress_form,
            'prof_formset': prof_formset,
            'doc_formset': doc_formset,
            'entete': entete
        }
        return render(request, "ressource_edit.html", context)


@login_required(login_url=settings.LOGIN_URI)
def ressource_edit(request, pk):
    ressource = Ressource.objects.get(pk=pk)
    entete = _(u"Mise a jour de la ressource ") + ressource.nom

    if request.method == 'POST':
        ress_form = RessourceForm(request.POST, instance=ressource)
        if ress_form.is_valid():
            ressource = ress_form.save()
        prof_formset = RessourceFormSet(request.POST, request.FILES, instance=ressource)
        doc_formset = DocumentFormSet(request.POST, request.FILES, instance=ressource)
        esms_formset = EsmsFormSet(request.POST, request.FILES, instance=ressource)
        if prof_formset.is_valid() and doc_formset.is_valid() and esms_formset.is_valid :
            prof_formset.save()
            doc_formset.save()
            esms_formset.save()

            messages.success(request, _(u"La ressource, son équipe et sa documentation sont mises à jour."))
            if 'Savesurplace' in request.POST:
                return redirect(ressource_edit, ressource.id)
            else:
                return redirect('ressource_detail', ressource.id)
        else:
            messages.error(request,  _(u"Il y a une erreur dans l'enregistrement de l'equipe ou de la documentation."))
            return redirect(ressource_edit, ressource.id)
    else:
        ress_form = RessourceForm(instance=ressource)
        prof_formset = RessourceFormSet(instance=ressource)
        doc_formset = DocumentFormSet(instance=ressource)
        esms_formset = EsmsFormSet(instance=ressource)

    context = {
        'form': ress_form,
        'prof_formset': prof_formset,
        'doc_formset': doc_formset,
        'esms_formset':esms_formset,
        'entete': entete,
        'pk': pk
    }
    return render(request, "ressource_edit.html", context)


class RessourceDetail(generic.DetailView):
    template_name = 'ressource_detail.html'
    model = Ressource


@login_required(login_url=settings.LOGIN_URI)
def rlisting(request):
    province = request.user.profile.province
    ressource_list = Ressource.objects.filter(province__id=province)
    paginator = NamePaginator(ressource_list, on="nom", per_page=5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        page = paginator.page(page)
    except InvalidPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'ressources_list.html', {'page': page})


