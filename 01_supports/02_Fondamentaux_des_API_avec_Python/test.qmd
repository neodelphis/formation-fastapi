# Fondamentaux des API avec Python

## FastAPI · Pydantic · REST · OpenAPI · Swagger UI

---

# Objectifs

À la fin de cette séance, vous serez capables de :

* comprendre ce qu'est une API ;
* expliquer le fonctionnement d'une communication client / serveur ;
* comprendre les principes fondamentaux d'une API REST ;
* utiliser les principales méthodes HTTP ;
* créer une API REST avec **FastAPI** ;
* définir des routes et leurs paramètres ;
* recevoir et retourner des données JSON ;
* créer des modèles avec **Pydantic** ;
* valider automatiquement les données reçues ;
* définir le contrat de réponse d'une API ;
* comprendre le rôle d'**OpenAPI** ;
* utiliser **Swagger UI** pour tester une API ;
* comprendre comment FastAPI génère automatiquement sa documentation.

---

# 1. Pourquoi avons-nous besoin d'APIs ?

Imaginez un jeu vidéo sur smartphone. L'application doit afficher le score et le niveau de la joueuse, Alice.

Ces informations sont stockées sur un serveur distant, dans une **base de données**.


```{mermaid}
graph TD
    A["Application du jeu<br><br>Alice<br>Score : 1250<br>Niveau : 12"] -->|???| B[("Base de données centrale<br><br>Alice : 1250<br>Bob : 840")]
    
    classDef client_data fill:#2B5E83,stroke:#fff,stroke-width:2px,color:#fff
    classDef result_db fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#000
    class A client_data
    class B result_db
```

L'application de votre téléphone pourrait-elle **se connecter directement à cette base de données** pour lire et modifier les scores ?

**Techniquement, oui. Mais ce serait une très mauvaise idée.**

Si l'application communique directement avec la base de données, cela signifie que le téléphone contient les codes d'accès à cette base. Un joueur un peu bricoleur pourrait intercepter la connexion et dire à la base de données : _"Modifie mon score et mets 999 999 points"_.

De plus, l'application devrait calculer elle-même si le joueur a le droit de passer au niveau supérieur, ce qui rend les mises à jour complexes si l'on sort le jeu sur d'autres supports.

C'est pour cela que l'on intercale un **arbitre** : l'API.

```{mermaid}
graph TD
    A[Application du jeu] -->|Requête HTTP<br>J'ai battu un monstre| B{API<br>L'Arbitre}
    B -->|Vérifie les règles<br>Met à jour les points| C[(Base de données)]
    C -.->|Nouveau score : 1260| B
    B -.->|Affiche 1260| A

    classDef client fill:#2B5E83,stroke:#fff,stroke-width:2px,color:#fff
    classDef api fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef db fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#000
    
    class A client
    class B api
    class C db
```

L'application ne parle plus à la base de données. Elle envoie une requête à l'API : _"Alice vient de battre un monstre"_.

L'API, qui contient toutes les règles du jeu, vérifie que l'action est valide, calcule les points gagnés, met elle-même la base de données à jour en toute sécurité, puis renvoie le nouveau score au téléphone.

Cette couche intermédiaire est une **API**.

---

# 2. Qu'est-ce qu'une API ?

API signifie :

> **Application Programming Interface**

Une API est une **interface permettant à un programme d'interagir avec un autre programme ou service**.

L'API définit notamment :

* comment demander une information ;
* quelles informations envoyer ;
* comment les données sont structurées ;
* quelles réponses sont possibles ;
* quelles erreurs peuvent être retournées.

---

## Une API comme contrat

On peut voir une API comme un contrat entre deux applications.

```{mermaid}
flowchart TD
    C1["CLIENT<br>« Je voudrais le joueur 42 »"] -->|Requête| A["API (SERVEUR)"]
    A -->|Réponse| C2["CLIENT<br>« Voici le joueur 42 »"]

    %% Styles
    classDef client_data fill:#2B5E83,stroke:#fff,stroke-width:2px,color:#fff
    classDef process_api fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000

    class C1,C2 client_data
    class A process_api
```


Le client n'a pas besoin de connaître :

* le langage utilisé par le serveur ;
* la base de données ;
* l'architecture interne ;
* le code du serveur.

Il doit simplement connaître **le contrat de l'API**.

---

# 3. Exemple : utiliser une API existante

Python peut communiquer avec une API grâce à HTTP.

Par exemple :

```python
import requests

response = requests.get(
    "https://api.github.com/users/python"
)

print(response.status_code)
print(response.json())
```

La fonction `requests.get()` envoie une requête HTTP.

Le serveur retourne une réponse.


```{mermaid}
flowchart TD
    P1[Python] -->|GET /users/python| G[GitHub API]
    G -->|JSON| P2[Python]

    %% Styles
    classDef client_data fill:#2B5E83,stroke:#fff,stroke-width:2px,color:#fff
    classDef process_api fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000

    class P1,P2 client_data
    class G process_api
```
---

## Que contient une réponse HTTP ?

Une réponse possède notamment :

* un **code de statut** ;
* des **en-têtes** ;
* un **contenu**.

Exemple :

```text
HTTP/1.1 200 OK

Content-Type: application/json

{
    "login": "python",
    "id": 1525981
}
```

---

# 4. Les codes HTTP

Quelques codes sont particulièrement importants.

|  Code | Signification                    |
| ----: | -------------------------------- |
| `200` | La requête a réussi              |
| `201` | Une ressource a été créée        |
| `204` | Succès, sans contenu à retourner |
| `400` | Requête incorrecte               |
| `401` | Authentification nécessaire      |
| `403` | Accès interdit                   |
| `404` | Ressource inexistante            |
| `422` | Données reçues invalides         |
| `500` | Erreur interne du serveur        |

Une API ne doit donc pas seulement retourner des données.

Elle doit également indiquer **ce qui s'est passé**.

---

# 5. Le format JSON

Les APIs REST utilisent très souvent le format **JSON**.

JSON permet de représenter des données structurées.

```json
{
    "id": 42,
    "name": "Alice",
    "score": 1250
}
```

Un objet JSON peut contenir :

* des chaînes de caractères ;
* des nombres ;
* des booléens ;
* des tableaux ;
* d'autres objets.

Par exemple :

```json
{
    "id": 42,
    "name": "Alice",
    "score": 1250,
    "weapons": [
        "sword",
        "bow"
    ],
    "active": true
}
```

---

# 6. API REST

REST signifie :

> **Representational State Transfer**

REST est un ensemble de principes permettant notamment d'organiser une API autour de **ressources**.

Dans notre jeu, les ressources pourraient être :

```text
players
games
weapons
scores
```

On peut alors imaginer :

```text
GET    /players
GET    /players/42

POST   /players

PUT    /players/42

DELETE /players/42
```

---

# 7. Les méthodes HTTP

Les quatre méthodes principales que nous utiliserons sont :

| Méthode  | Action    |
| -------- | --------- |
| `GET`    | Lire      |
| `POST`   | Créer     |
| `PUT`    | Modifier  |
| `DELETE` | Supprimer |

On peut les rapprocher des opérations CRUD :

| HTTP   | CRUD   |
| ------ | ------ |
| GET    | Read   |
| POST   | Create |
| PUT    | Update |
| DELETE | Delete |

---

# 8. Notre fil rouge : Game API

Nous allons construire progressivement une API pour un petit jeu.

Notre API devra gérer des joueurs.

Un joueur possède :

```text
id
name
score
level
```

Notre API devra permettre de :

```text
Récupérer tous les joueurs

GET /players
```

```text
Récupérer un joueur

GET /players/{player_id}
```

```text
Créer un joueur

POST /players
```

```text
Modifier un joueur

PUT /players/{player_id}
```

```text
Supprimer un joueur

DELETE /players/{player_id}
```

---

# 9. Pourquoi FastAPI ?

Nous pourrions construire nous-mêmes un serveur HTTP en Python.

Mais il faudrait gérer beaucoup de choses :

* réception des requêtes ;
* routage ;
* parsing du JSON ;
* validation ;
* gestion des erreurs ;
* sérialisation ;
* documentation ;
* etc.

C'est précisément le rôle d'un framework.

Pour notre API, nous utiliserons :

# FastAPI

FastAPI est un framework Python permettant de construire des APIs modernes.

Il s'appuie fortement sur :

* les **Type Hints Python** ;
* **Pydantic** ;
* un serveur **ASGI** ;
* **OpenAPI**.

---

# 10. Installer FastAPI

Créons un environnement virtuel :

```bash
python -m venv .venv
```

Activation sous Linux / macOS :

```bash
source .venv/bin/activate
```

Sous Windows :

```powershell
.venv\Scripts\activate
```

Puis :

```bash
pip install "fastapi[standard]"
```

---

# 11. Notre première API

Créons un fichier :

```text
main.py
```

Avec seulement quelques lignes :

```python
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the Game API"}
```

---

# 12. Lancer le serveur

Depuis le terminal :

```bash
fastapi dev main.py
```

Le serveur démarre localement.

Par défaut :

```text
http://127.0.0.1:8000
```

Ouvrons cette adresse dans un navigateur.

Nous obtenons :

```json
{
    "message": "Welcome to the Game API"
}
```

---

# 13. Que s'est-il passé ?

Lorsque nous avons écrit :

```python
@app.get("/")
```

nous avons indiqué à FastAPI :

> Lorsqu'une requête `GET` est envoyée vers `/`, exécute cette fonction.

```{mermaid}
flowchart TD
    A["GET /"] --> B{FastAPI}
    B --> C["home()"]
    C --> D["{ &quot;message&quot;: &quot;...&quot; }"]

    %% Styles
    classDef client_data fill:#2B5E83,stroke:#fff,stroke-width:2px,color:#fff
    classDef process_api fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef result_db fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#000

    class A client_data
    class B,C process_api
    class D result_db
```

Cette association entre une URL et une fonction est appelée une **route**.

---

# 14. Les routes

Pour manipuler nos données, simulons une petite base de données avec un dictionnaire :

```python
PLAYERS = {
    "1": {"id": 1, "name": "Alice", "score": 1200},
    "2": {"id": 2, "name": "Bob", "score": 950},
    "42": {"id": 42, "name": "Zelda", "score": 3000}
}

```

Une route est définie par :

```python
@app.get("/players")
def get_players():
    ...

```

On peut lire cela comme :

> Pour une requête GET vers `/players`, exécuter `get_players()`.

Exemple :

```python
@app.get("/players")
def get_players():
    # On retourne la liste de tous les joueurs
    return list(PLAYERS.values())

```

Tester :

```text
http://127.0.0.1:8000/players
GET /players

```

Résultat :

```json
[
    {
        "id": 1,
        "name": "Alice",
        "score": 1200
    },
    {
        "id": 2,
        "name": "Bob",
        "score": 950
    },
    {
        "id": 42,
        "name": "Zelda",
        "score": 3000
    }
]

```

---

# 15. Paramètres de chemin

Comment récupérer uniquement le joueur `42` ?

Nous pouvons utiliser un paramètre variable dans l'URL :

```python
@app.get("/players/{player_id}")
def get_player(player_id):
    # Par défaut, player_id est du texte (str)
    return PLAYERS.get(player_id)

```

Une requête :

```text
http://127.0.0.1:8000/players/42
GET /players/42

```

donne :

```json
{
    "id": 42,
    "name": "Zelda",
    "score": 3000
}

```
