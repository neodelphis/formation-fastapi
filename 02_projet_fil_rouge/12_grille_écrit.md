# 📝 Grille d'évaluation – **Dépôt Git et Qualité du code**
*Évaluation sur **20 points***

---

Cette grille évalue :
- La **propreté du dépôt** et sa documentation,
- L’**architecture du code** et les bonnes pratiques,
- Le **respect du cahier des charges** fonctionnel.

---

## 📊 Critères d'évaluation

| **Critères**                          | **Compétences évaluées** | **Points** | **Observations / Commentaires** |
|---------------------------------------|---------------------------|------------|----------------------------------|
| **1. Documentation & README**         | README **clair et professionnel** avec instructions de lancement (ex: `uvicorn app.main:app --reload`). Scénario et univers du jeu documentés. Présence de **diagrammes de classes** (ex: *Mermaid*). | **4 pts**  | |
| **2. Architecture Cohérente & Bonnes Pratiques** | Séparation claire des responsabilités : `app/domain/` (métier), `app/routers/` (API REST), `app/schemas/` (Pydantic). Utilisation **systématique** des *Type Hints* et des *Dataclasses*. | **4 pts**  | |
| **3. Code Fonctionnel & Respect du Brief** | Code **exécutable sans erreur**. Implémentation pertinente de l’**héritage** et du **polymorphisme** (ex: classes `GameElement`, `Item`, `Door`, et classe abstraite `Puzzle` déclinée en `CodePuzzle` et `HashPuzzle`). Endpoints REST (exploration des salles, soumission des puzzles) **fonctionnels**. | **5 pts**  | |
| **4. Validation & Sécurité**          | Schémas Pydantic **validant correctement** les requêtes (ex: levée d’exception pour un code soumis vide). Logique de vérification cryptographique (**SHA-256 / MD5**) fonctionnelle dans `HashPuzzle`. | **3 pts**  | |
| **5. Tests Fonctionnels et Unitaires** | Présence de **tests pertinents**. Couverture des méthodes critiques du domaine métier (ex: `check_solution`) et des routes d’API (avec `TestClient` de FastAPI). **Tous les tests passent**. | **4 pts**  | |
| **Total**                             |                           | **20 pts** | |

---