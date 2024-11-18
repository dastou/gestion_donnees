from django import forms
from .models import Table

class TableForm(forms.Form):
    nom_table = forms.CharField(max_length=100, required=True)
    zone = forms.CharField(max_length=100, required=False)
    database = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    frequence_ingestion = forms.CharField(max_length=100, required=False)
    commentaire = forms.CharField(widget=forms.Textarea, required=False)
    heure_de_lancement = forms.CharField(
        max_length=5,
        help_text="Format: HH:MM (24 heures)",
        required=False
    )
    type = forms.ChoiceField(
        choices=[
            ('source', 'Source'),
            ('cible', 'Cible'),
            ('les deux', 'Les deux')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    db_refined = forms.CharField(
        max_length=100,
        required=False,
        label="DB Refined"
    )
    frequence_kpi = forms.CharField(
        max_length=100,
        required=False,
        label="Fréquence KPI"
    )
    suivie = forms.ChoiceField(
        choices=[('oui', 'Oui'), ('non', 'Non')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Suivie",
        required=False
    )
    qualite = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Qualité (%)",
        required=False
    )
    exhaustivite = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Exhaustivité (%)",
        required=False
    )
    precision = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Précision (%)",
        required=False
    )
    coherence = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Cohérence (%)",
        required=False
    )
    conformite = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Conformité (%)",
        required=False
    )
    unicite = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Unicité (%)",
        required=False
    )
    integrite = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Intégrité (%)",
        required=False
    )

    def __init__(self, *args, **kwargs):
         # Extraire instance si elle existe
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # Si on a une instance, initialiser les champs avec ses valeurs
        if instance:
            # Mettre à jour les valeurs initiales avec les données de l'instance
            for field_name, field in self.fields.items():
                if hasattr(instance, field_name):
                    self.initial[field_name] = getattr(instance, field_name)
            
            # Gérer spécialement les relations
            self.initial['tables_cibles'] = [t.nom_table for t in instance.toutes_tables_cibles]
            self.initial['tables_sources'] = [t.nom_table for t in instance.toutes_tables_sources]

        self.fields['tables_cibles'] = forms.MultipleChoiceField(
            required=False,
            choices=[],
            widget=forms.SelectMultiple(attrs={'class': 'form-control'})
        )
        self.fields['tables_sources'] = forms.MultipleChoiceField(
            required=False,
            choices=[],
            widget=forms.SelectMultiple(attrs={'class': 'form-control'})
        )

    def update_relation_choices(self, selected_type):
        # Récupérer toutes les tables existantes selon leur type
        tables_cibles_possibles = Table.nodes.filter(type__in=['cible', 'les deux'])
        tables_sources_possibles = Table.nodes.filter(type__in=['source', 'les deux'])
        
        # Créer les listes de choix pour le formulaire
        choices_cibles = [(table.nom_table, table.nom_table) for table in tables_cibles_possibles]
        choices_sources = [(table.nom_table, table.nom_table) for table in tables_sources_possibles]

        # Mettre à jour les choix selon le type sélectionné
        if selected_type in ['source', 'les deux']:
            self.fields['tables_cibles'].choices = choices_cibles
        
        if selected_type in ['cible', 'les deux']:
            self.fields['tables_sources'].choices = choices_sources
