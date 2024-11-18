from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import TableForm
from .models import Table
from .utils import neo4j_get_or_404

def ajouter_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        form.update_relation_choices(request.POST.get('type'))
        
        if form.is_valid():
            data = form.cleaned_data
            
            # Créer la nouvelle table
            nouvelle_table = Table(
                nom_table=data['nom_table'],
                zone=data['zone'],
                database=data['database'],
                description=data['description'],
                frequence_ingestion=data['frequence_ingestion'],
                commentaire=data['commentaire'],
                heure_de_lancement=data['heure_de_lancement'],
                type=data['type'],
                db_refined=data['db_refined'],
                frequence_kpi=data['frequence_kpi'],
                suivie=data['suivie'],
                qualite=data['qualite'],
                exhaustivite=data['exhaustivite'],
                precision=data['precision'],
                coherence=data['coherence'],
                conformite=data['conformite'],
                unicite=data['unicite'],
                integrite=data['integrite']
            )
            nouvelle_table.save()

            # Créer les relations avec les tables cibles
            if data['type'] in ['source', 'les deux'] and data['tables_cibles']:
                for nom_cible in data['tables_cibles']:
                    table_cible = Table.nodes.get(nom_table=nom_cible)
                    nouvelle_table.ajouter_relation_cible(table_cible)

            # Créer les relations avec les tables sources
            if data['type'] in ['cible', 'les deux'] and data['tables_sources']:
                for nom_source in data['tables_sources']:
                    table_source = Table.nodes.get(nom_table=nom_source)
                    table_source.ajouter_relation_cible(nouvelle_table)

            messages.success(request, 'Table ajoutée avec succès!')
            return redirect('liste_tables')
    else:
        form = TableForm()
    
    return render(request, 'ajouter_tables.html', {'form': form})

def get_available_tables(request):
    selected_type = request.GET.get('type')
    form = TableForm()
    form.update_relation_choices(selected_type)
    
    return JsonResponse({
        'tables_cibles': dict(form.fields['tables_cibles'].choices),
        'tables_sources': dict(form.fields['tables_sources'].choices)
    })

def liste_tables(request):
    tables = Table.nodes.all()
    return render(request, 'liste_tables.html', {'tables': tables})


def voir_table(request, nom_table):
    table = neo4j_get_or_404(Table, nom_table=nom_table)
    return render(request, 'voir_table.html', {'table': table})

def modifier_table(request, nom_table):
    table = neo4j_get_or_404(Table, nom_table=nom_table)
    
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)  # Passez l'instance ici
        form.update_relation_choices(request.POST.get('type'))
        
        if form.is_valid():
            data = form.cleaned_data
            
            # Mise à jour des champs de base
            for field in ['zone', 'database', 'description', 'frequence_ingestion', 
                         'commentaire', 'heure_de_lancement', 'type', 'db_refined', 
                         'frequence_kpi', 'suivie', 'qualite', 'exhaustivite', 
                         'precision', 'coherence', 'conformite', 'unicite', 'integrite']:
                setattr(table, field, data.get(field))
            
            # Sauvegarde des modifications
            table.save()
            
            # Mise à jour des relations seulement si elles ont changé
            current_cibles = set(t.nom_table for t in table.toutes_tables_cibles)
            new_cibles = set(data.get('tables_cibles', []))
            current_sources = set(t.nom_table for t in table.toutes_tables_sources)
            new_sources = set(data.get('tables_sources', []))

            # Supprimer uniquement les relations qui ne sont plus présentes
            if data['type'] in ['source', 'les deux']:
                # Supprimer les relations cibles qui ne sont plus sélectionnées
                for cible in current_cibles - new_cibles:
                    table_cible = Table.nodes.get(nom_table=cible)
                    table.supprimer_relation_cible(table_cible)
                # Ajouter les nouvelles relations cibles
                for cible in new_cibles - current_cibles:
                    table_cible = Table.nodes.get(nom_table=cible)
                    table.ajouter_relation_cible(table_cible)

            if data['type'] in ['cible', 'les deux']:
                # Supprimer les relations sources qui ne sont plus sélectionnées
                for source in current_sources - new_sources:
                    table_source = Table.nodes.get(nom_table=source)
                    table_source.supprimer_relation_cible(table)
                # Ajouter les nouvelles relations sources
                for source in new_sources - current_sources:
                    table_source = Table.nodes.get(nom_table=source)
                    table_source.ajouter_relation_cible(table)
            
            messages.success(request, 'Table modifiée avec succès!')
            return redirect('voir_table', nom_table=table.nom_table)
    else:
        # Créer le formulaire avec l'instance et les données initiales
        initial_data = {
            'tables_cibles': [t.nom_table for t in table.toutes_tables_cibles],
            'tables_sources': [t.nom_table for t in table.toutes_tables_sources]
        }
        form = TableForm(instance=table, initial=initial_data)
        form.update_relation_choices(table.type)
    
    return render(request, 'ajouter_tables.html', {
        'form': form,
        'mode': 'modification',
        'table': table
    })

def supprimer_table(request, nom_table):
    if request.method == 'POST':
        table = neo4j_get_or_404(Table, nom_table=nom_table)
        
        # Supprimer toutes les relations avant de supprimer la table
        for rel in table.tables_cibles.all():
            table.supprimer_relation_cible(rel)
        for rel in table.tables_sources.all():
            rel.supprimer_relation_cible(table)
        
        # Supprimer la table
        table.delete()
        messages.success(request, 'Table supprimée avec succès!')
        
    return redirect('liste_tables')

def rechercher_table(request):
    query = request.GET.get('q', '')
    resultats = []
    message = ''
    
    if query:
        # Chercher la table source
        try:
            table = Table.nodes.get(nom_table=query)
            if table.type in ['source', 'les deux']:
                resultats = table.toutes_tables_cibles
                if not resultats:
                    message = f"La table '{query}' n'alimente aucune table cible."
            else:
                message = f"La table '{query}' n'est pas une table source."
        except Table.DoesNotExist:
            message = f"Aucune table trouvée avec le nom '{query}'."
    
    return render(request, 'rechercher_table.html', {
        'query': query,
        'resultats': resultats,
        'message': message
    })