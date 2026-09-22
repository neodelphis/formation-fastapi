# Environnement technique recommandé

## Langage

- Python 3.11 ou supérieur.

## Dépendances principales

```text
fastapi
uvicorn
pydantic
pydantic-settings
sqlalchemy
alembic
psycopg2-binary
pytest
httpx
requests
python-dotenv
```

## Sécurité authentification

Selon votre préférence :

```text
python-jose
pyjwt
passlib
bcrypt
argon2-cffi
```

Je recommande une solution simple et maintenable, par exemple :

- `PyJWT` pour les tokens ;
- `argon2-cffi` ou `bcrypt` pour le hash des mots de passe.

## Base de données

- PostgreSQL via Docker Compose.

Exemple minimal :

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: securesoc
      POSTGRES_PASSWORD: securesoc_password
      POSTGRES_DB: securesoc
    ports:
      - "5432:5432"
```

## Outils utiles

- curl ;
- Swagger UI ;
- VS Code ou PyCharm ;
- git ;
- pytest ;
- éventuellement httpie.


