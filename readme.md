# Projet de Gestion des Tables de Données

## 📋 Description
Application web Django permettant de gérer les relations et les métadonnées des tables de données dans une base Neo4j. Elle permet de suivre les dépendances entre les tables sources et cibles, ainsi que diverses métriques de qualité.

## 🔑 Fonctionnalités principales
- Création, modification et suppression de tables
- Gestion des relations entre tables (source → cible)
- Suivi des métriques de qualité (exhaustivité, précision, cohérence, etc.)
- Visualisation des dépendances entre tables
- Interface dynamique avec mise à jour en temps réel des relations disponibles

## 🛠️ Prérequis
- Python 3.8+
- Django 5.1+
- Neo4j 4.4+
- pip (gestionnaire de paquets Python)

## 📦 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/dastou/gestion_donnees.git
cd gestion_donnees
```

2. **Créer et activer un environnement virtuel**
```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur Unix ou MacOS
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer Neo4j**
- Installer et démarrer Neo4j
- Créer une nouvelle base de données
- Modifier les identifiants dans `settings.py` ou créer un fichier `.env`

5. **Configurer les variables d'environnement**
Créer un fichier `.env` à la racine du projet :
```env
DEBUG=True
DJANGO_SECRET_KEY=votre-clé-secrète
NEO4J_URL=bolt://neo4j:votre-mot-de-passe@localhost:7687
```

6. **Appliquer les migrations**
```bash
python manage.py migrate
```

## 🚀 Démarrage
1. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

2. **Accéder à l'application**
- Ouvrir un navigateur et aller à `http://localhost:8000`

## 📱 Utilisation

### Ajouter une table
1. Cliquer sur "Ajouter une table"
2. Remplir les informations requises :
   - Nom de la table (obligatoire)
   - Type (source, cible, ou les deux)
   - Heure de lancement (format HH:MM)
3. Remplir les informations optionnelles :
   - Zone
   - Base de données
   - Description
   - Métriques de qualité
4. Sélectionner les relations avec d'autres tables si nécessaire
5. Cliquer sur "Enregistrer"

### Gérer les relations
- Le type de table détermine les relations disponibles :
  - Table source : peut avoir des tables cibles
  - Table cible : peut avoir des tables sources
  - Les deux : peut avoir les deux types de relations

### Métriques de qualité
Les métriques suivantes peuvent être suivies (0-100%) :
- Qualité globale
- Exhaustivité
- Précision
- Cohérence
- Conformité
- Unicité
- Intégrité

## 🔧 Configuration

### Configuration de la base de données
Dans `settings.py` :
```python
NEOMODEL_NEO4J_BOLT_URL = 'bolt://neo4j:mot-de-passe@localhost:7687'
NEOMODEL_MAX_CONNECTION_POOL_SIZE = 50
```

### Configuration des fichiers statiques
```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
```

## 🌐 Structure du projet
```
project/
│
├── formulaire/                 # Application principale
│   ├── models.py              # Modèles Neo4j
│   ├── views.py               # Vues
│   ├── forms.py               # Formulaires
│   └── templates/             # Templates
│       ├── ajouter_tables.html
│       ├── liste_tables.html
│       └── voir_table.html
│
├── static/                    # Fichiers statiques
├── templates/                 # Templates globaux
├── manage.py                  # Script Django
└── requirements.txt          # Dépendances
```

