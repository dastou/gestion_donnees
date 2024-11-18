from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, IntegerProperty, BooleanProperty
import re

class Table(StructuredNode):
    nom_table = StringProperty(required=True, unique_index=True)
    zone = StringProperty()
    database = StringProperty()
    description = StringProperty()
    frequence_ingestion = StringProperty()
    commentaire = StringProperty()
    heure_de_lancement = StringProperty(required=False)
    type = StringProperty(choices=[('source', 'Source'), ('cible', 'Cible'), ('les deux', 'Les deux')])
    #nouveaux champs
    db_refined = StringProperty()
    frequence_kpi = StringProperty()
    suivie = StringProperty(choices=[('oui', 'Oui'), ('non', 'Non')])
    qualite = IntegerProperty(min_value=0, max_value=100)
    exhaustivite = IntegerProperty(min_value=0, max_value=100)
    precision = IntegerProperty(min_value=0, max_value=100)
    coherence = IntegerProperty(min_value=0, max_value=100)
    conformite = IntegerProperty(min_value=0, max_value=100)
    unicite = IntegerProperty(min_value=0, max_value=100)
    integrite = IntegerProperty(min_value=0, max_value=100)

    # Relation orientée: une table source pointe vers ses tables cibles
    tables_cibles = RelationshipTo('Table', 'ALIMENTE')
    # Relation inverse pour faciliter la navigation
    tables_sources = RelationshipFrom('Table', 'ALIMENTE')

    def save(self, *args, **kwargs):
        if self.heure_de_lancement:  # Vérifier seulement si une heure est fournie
            if not re.match(r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$', self.heure_de_lancement):
                raise ValueError("Le format de l'heure doit être HH:MM (24 heures).")
        super().save(*args, **kwargs)

    def ajouter_relation_cible(self, table_cible):
        """Ajoute une relation orientée vers une table cible"""
        return self.tables_cibles.connect(table_cible)

    def supprimer_relation_cible(self, table_cible):
        """Supprime une relation avec une table cible"""
        return self.tables_cibles.disconnect(table_cible)
    
    @property
    def toutes_tables_sources(self):
        """Retourne toutes les tables sources qui alimentent cette table"""
        return self.tables_sources.all()

    @property
    def toutes_tables_cibles(self):
        """Retourne toutes les tables cibles alimentées par cette table"""
        return self.tables_cibles.all()