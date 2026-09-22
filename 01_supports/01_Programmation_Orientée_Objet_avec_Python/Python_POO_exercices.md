
# 🧠 Exercices Programmation Orientée Objet (POO)

Renforcer la compréhension des concepts suivants :
- Classes et objets
- Constructeurs et méthodes
- Encapsulation et gestion des attributs
- Méthodes spéciales (`__str__`, `__eq__`, etc.)
- Organisation en modules

---

## 📌 Exercice 1 : Gestion de compte bancaire sécurisé

### Énoncé :

Créez une classe `CompteBancaire` qui permet de :
- Créer un compte avec un solde initial
- Faire des dépôts et retraits
- Vérifier le solde
- Empêcher les retraits supérieurs au solde

➡️ Ajoutez également :
- Une méthode pour appliquer des intérêts (`appliquer_interets(taux)`)
- Des vérifications robustes
- Des noms d’utilisateurs uniques (ex. empêcher deux comptes avec le même nom)

💡 Utilisez :
- Attributs privés
- Getters/setters ou `@property`
- Méthodes de validation

---

## 📌 Exercice 2 : Héritage – Formes géométriques

### Énoncé :

Implémentez une hiérarchie de classes représentant différentes formes géométriques :
- Classe mère : `Forme`
- Sous-classes : `Rectangle`, `Cercle`

Chaque forme doit avoir :
- Une méthode `.aire()`
- Une méthode `.perimetre()`

➡️ Bonus : 
- Comparez les aires via `__lt__`, `__eq__`
- Affichez chaque objet avec `__str__`

📌 Objectif : Pratiquer l’héritage, le polymorphisme et la réutilisation de code.

---

## 📌 Exercice 3 : Système de gestion de bibliothèque

### Énoncé :

Concevez un système orienté objet pour une bibliothèque, avec les classes suivantes :
- `Livre` : titre, auteur, isbn, disponibilité
- `Membre` : nom, identifiant, livres empruntés
- `Bibliotheque` : liste de livres, méthodes pour emprunter/rendre/lister

➡️ Fonctionnalités attendues :
- Recherche par titre ou auteur
- Emprunt/retour de livre
- Liste des livres disponibles
- Sauvegarde/restauration depuis un fichier JSON

💡 Utilisez :
- POO complète
- Modules standards (`json`)
- Organisation en fichiers (si temps)

---

## 📌 Exercice 4 : Modélisation d’un système de véhicules

### Énoncé :

Modélisez une hiérarchie de véhicules :
- Classe mère : `Vehicule`
- Sous-classes : `Voiture`, `Moto`, `Camion`

➡️ Chaque véhicule aura :
- Un constructeur
- Des attributs : marque, modèle, année, vitesse
- Des méthodes : `accelerer()`, `freiner()`, `__str__()`

➡️ Bonus :
- Implémentez une interface `Roulable` avec `rouler()` implémentée différemment selon le type
- Utilisez des classes abstraites (`abc.ABC`, `@abstractmethod`)

📌 Objectif : Maîtriser l’héritage multiple, les méthodes abstraites et le polymorphisme.

---

## 📌 Exercice 5 : Générateur de formulaires dynamiques

### Énoncé :

Créez un système de formulaires basé sur des classes :
- Une classe `Champ` avec :
  - Nom
  - Type (texte, nombre, email, etc.)
  - Valeur
  - Validation
- Des sous-classes spécialisées : `ChampTexte`, `ChampEmail`, `ChampNombre`
- Une classe `Formulaire` qui gère plusieurs champs et valide le formulaire complet

➡️ Exemple :
```python
nom = ChampTexte('nom', 'Jean')
email = ChampEmail('email', 'jean@mail.com')

formulaire = Formulaire([nom, email])
print(formulaire.valider())  # True ou False
```

💡 Ce projet est idéal pour explorer :
- L’héritage
- Le polymorphisme
- La modularité

---

## 📌 Exercice 6 : Journalisation orientée objet

### Énoncé :

Écrivez un système de journalisation simple en POO :
- Une classe `Journal` qui stocke des messages
- Des sous-classes :
  - `FichierJournal` : sauvegarde dans un fichier texte
  - `ConsoleJournal` : affichage immédiat
  - `JSONJournal` : sauvegarde dans un fichier JSON

➡️ Chaque classe devra implémenter une méthode commune :
```python
def log(self, message):
    pass
```

💡 Objectif : Explorer le **polymorphisme** et la **programmation modulaire**

---

## 📌 Exercice 7 : Gestion de parc informatique

### Énoncé :

Modélisez un système de gestion de matériel informatique :
- Classes : `Equipement`, `Ordinateur`, `Imprimante`, `Serveur`
- Chaque équipement aura :
  - Numéro de série
  - Date d’achat
  - Statut (en service, hors service)
  - Méthode `.afficher_info()`

➡️ Enrichissez avec :
- Une classe `ParcInformatique` pour gérer tous les appareils
- Des recherches par statut, date, type
- Export vers CSV

📌 Idéal pour pratiquer :
- L’héritage
- Les listes d’objets
- La gestion de données structurées

---
