from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from esms.esms_constants import CHOIX
from dataentry.models import Province
from django.urls import reverse


## Détails des ressources décrites et catégorisées
class Ressource(models.Model):
    nom = models.CharField(verbose_name=_("Nom de la ressource "), help_text=_("Obligatoire"), max_length=200,)
    ville = models.CharField(verbose_name=_("Municipalité "), help_text=_("Obligatoire"), max_length=100,)
    codepostal = models.CharField(max_length=10, verbose_name=_("Code postal "), null=True, blank=True)
    web = models.CharField(verbose_name=_("Adresse du site web "), max_length=250, null=True, blank=True)
    telephone = models.CharField(verbose_name=_("Numéro de tel public "), max_length=20, null=True, blank=True)
    courriel = models.CharField(verbose_name=_("Courriel public "), max_length=200, null=True, blank=True)
    objectif = models.TextField(verbose_name=_("Objectifs de cette ressource "), null=True, blank=True)
    region = models.TextField(verbose_name=_("Région(s) déservie(s) "), null=True, blank=True)
    anciennete = models.CharField(max_length=100, verbose_name=_("Année de la création de laressource ou ancienneté "), null=True, blank=True)
    lieutravail = models.TextField(verbose_name=_("Lieux principaux d'exercice (si plusieurs sites) "), null=True, blank=True)
    financement = models.TextField(verbose_name=_("Quelles sont les sources de financement "), help_text=_("Par exemple RI, RE, RTF, MSSS, fondation etc."), null=True, blank=True)
    heuresouverture = models.TextField(verbose_name=_("Heures et jours d'ouverture "), null=True, blank=True)
    profilpatient = models.TextField(verbose_name=_("Profil général des patients pris en charge, limites d'âge, genre etc "), null=True, blank=True)
    exclusion = models.TextField(verbose_name=_("Critères d'exclusion "), null=True, blank=True)
    forensicpatient = models.BooleanField(verbose_name=_("Acceptez-vous les cas de patients psycholégaux? "))
    forensicpatientnombre = models.TextField(verbose_name=_("Si oui combien et dans quelles conditions "), null=True, blank=True)
    multipleproblematique = models.BooleanField(verbose_name=_("Acceptez-vous les cas de patients avec des problématiques multiples? "))
    multipleproblematiquenombre = models.TextField(verbose_name=_("Si oui combien et dans quelles conditions "), null=True, blank=True)
    approche = models.TextField(verbose_name=_("Type de thérapie ou approche "), null=True, blank=True)
    autochtones =  models.BooleanField(verbose_name=_("Offrez-vous des services culturellement adaptés aux Autochtones? "))
    autochtonestexte =  models.TextField(verbose_name=_("Si oui détaillez ces services"), null=True, blank=True)
    reference = models.TextField(verbose_name=_("Origine des patients (source des références) "), null=True, blank=True)
    delais = models.TextField(verbose_name=_("Quels sont les délais moyens de prise en charge (En dehors des temps de liste d'attente) "), null=True, blank=True)
    durees = models.TextField(verbose_name=_("Quelles sont les durées moyennes des prises en charge "), null=True, blank=True)
    listeattenteyn = models.BooleanField(verbose_name=_("Cliquer s'il y a une liste d'attente "))
    listeattenteduree = models.TextField(verbose_name=_("Si liste d'attente, durée moyenne de l'attente "), null=True, blank=True)
    commentaire = models.TextField(verbose_name=_("Autres informations pertinantes "), null=True, blank=True)
    autreservice = models.TextField(verbose_name=_("Services ou activités secondaires "), help_text=_("Par exemple soutien téléphonique, cuisines collectives, cours etc"), null=True, blank=True)
    noncontactable = models.BooleanField(verbose_name=_("Pas de réponse après 5 tentatives "))
    accepte = models.BooleanField(verbose_name=_("Accepte que certaines données soient rendues publiques sur le site de l'observatoire "))
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       ordering = ['nom']

    def __str__(self):
        return '%s' % self.nom


class Document(models.Model):
    titrecourt = models.CharField(max_length=100, verbose_name=_("Non court et évocateur du document"))
    documentation = models.FileField(upload_to='DocsReferences', verbose_name=_("Documents pertinants"), help_text=_("ATTENTION PAS D'ACCENT DANS LE NOM DES FICHIERS"))
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.titrecourt


class Professionnels(models.Model):
    description = models.CharField(max_length=100, verbose_name=_("Professionnel"))

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Equipe(models.Model):
    profession = models.ForeignKey(Professionnels, on_delete=models.CASCADE, verbose_name=_("Professionnel"))
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20, verbose_name=_("Nombre d'équivalent temps plein"), blank=True, null=True)
    duree = models.CharField(max_length=250, verbose_name=_("Temps moyen de travail"), blank=True, null=True)
    tache = models.TextField(verbose_name=_("Tâche"), blank=True, null=True)

    class Meta:
        ordering = ['ressource', 'nombre']

    def __str__(self):
        return '%s %s %s %s' % (self.profession, self.nombre, self.duree, self.tache)


# Table permettant d'enregistrer les codes ESMS pour chaque ressource.
class Esms(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, verbose_name=_("Ressource"))
    code = models.CharField(choices=CHOIX, max_length=20, verbose_name=_("Code ESMS"))
    nombre = models.IntegerField(default=0, verbose_name=_("Nombre de places"))
    clientele = models.CharField(max_length=250, verbose_name=_("Clientèle cible pour cette branche"), blank=True, null=True)
    autreinfo = models.TextField(verbose_name=_("Autres informations"),blank=True, null=True)
    autresservices = models.TextField(verbose_name=_("Autres services dispensés en plus du service codé"), help_text=_("Par exemple insertion professionnelle en plus de l'hébergement"), blank=True, null=True)

    class Meta:
        ordering = ['ressource', 'code']

    def choix_final(self):
        return dict(CHOIX)[self.code]

    def __str__(self):
        return '%s %s' % (self.ressource, self.code)
