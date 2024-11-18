from django.urls import path
from .views import ajouter_table, liste_tables, get_available_tables, voir_table, modifier_table, supprimer_table, rechercher_table

urlpatterns = [
    path('', ajouter_table, name='ajouter_table'),  
    path('tables/', liste_tables, name='liste_tables'), 
    path('get_available_tables/', get_available_tables, name='get_available_tables'), 
    path('table/<str:nom_table>/', voir_table, name='voir_table'),
    path('table/<str:nom_table>/modifier/', modifier_table, name='modifier_table'),
    path('table/<str:nom_table>/supprimer/', supprimer_table, name='supprimer_table'),
    path('rechercher/', rechercher_table, name='rechercher_table'),
]