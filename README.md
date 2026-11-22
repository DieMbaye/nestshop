# NestShop

Boutique en ligne de produits artisanaux sénégalais.
Projet de fin de formation DevOps & DevSecOps (DevNest Academy).

## Workflow Git

Ce projet suit **Git Flow** :

| Branche | Rôle |
|---|---|
| `main` | Code en production (versions stables) |
| `develop` | Intégration des fonctionnalités, déployée en staging |
| `feature/*` | Une fonctionnalité en cours, créée depuis `develop` |
| `release/*` | Préparation d'une version |
| `hotfix/*` | Correction urgente en production |

- `main` et `develop` sont **protégées** : aucun push direct, fusion uniquement par **pull request**.
- Les messages de commit suivent **Conventional Commits** (`feat:`, `fix:`, `docs:`, `ci:`...).