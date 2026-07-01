# ATM10 Discord Manager

> Bot Discord Python pour gérer un serveur Minecraft All the Mods 10: To the Sky hébergé dans Docker.

![Version](https://img.shields.io/badge/version-v0.6.0-blue)
![Python](https://img.shields.io/badge/Python-3.13-yellow)
![discord.py](https://img.shields.io/badge/discord.py-2.6%2B-5865F2)
![Docker](https://img.shields.io/badge/Docker-SDK-2496ED)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Description

ATM10 Discord Manager transforme Discord en panneau d'administration pour un serveur Minecraft Docker. Le bot permet de consulter l'état du serveur, de démarrer, arrêter et redémarrer le conteneur, puis de piloter tout cela depuis un dashboard Discord permanent.

L'objectif long terme est de remplacer les actions courantes faites dans Portainer par une interface Discord propre, maintenable et extensible.

---

## Fonctionnalités

### Disponible en v0.6.0

- Commandes slash avec discord.py 2.6+
- Architecture modulaire avec Cogs
- Architecture orientée services
- Configuration via .env et configuration persistante
- Connexion au Docker SDK
- Gestion du conteneur Minecraft Docker
- Permissions par rôle Discord
- Embeds Discord dédiés
- Boutons interactifs
- Dashboard Discord permanent
- Boutons persistants après redémarrage du bot
- Actualisation automatique du dashboard toutes les 15 secondes
- Sauvegarde du message dashboard dans data/dashboard.json

### Dashboard permanent

Le dashboard crée un seul message Discord et enregistre guild_id, channel_id et message_id dans data/dashboard.json.

Boutons disponibles :

- Start
- Stop
- Restart
- Refresh

Chaque bouton possède un custom_id, ce qui permet à Discord de continuer à router les interactions après un redémarrage du bot.

---

## Commandes

```text
/ping
/status

/setup [container]

/server status
/server start
/server stop
/server restart

/dashboard create
/dashboard delete
/dashboard refresh
```

### /setup

Configure le conteneur Docker Minecraft utilisé par le bot.

- Avec un nom : /setup container:nom_du_conteneur
- Sans argument : le bot affiche une liste de conteneurs Docker disponibles

Le conteneur peut aussi être défini avec la variable d'environnement DOCKER_CONTAINER.

### /dashboard create

Crée le dashboard permanent dans le salon courant. Si un dashboard existe déjà dans data/dashboard.json, la commande refuse d'en créer un deuxième.

### /dashboard delete

Supprime le message dashboard enregistré, puis nettoie data/dashboard.json.

### /dashboard refresh

Force la mise à jour du dashboard enregistré.

---

## Installation

### Prérequis

- Python 3.13
- Docker
- Accès au socket Docker
- Un bot Discord avec les intents nécessaires

### Dépendances

```bash
pip install -r requirements.txt
```

### Configuration

Créer un fichier .env à la racine du projet :

```env
DISCORD_TOKEN=token_du_bot
AUTHORIZED_ROLE=Admin
DOCKER_CONTAINER=nom_du_conteneur_minecraft
```

DOCKER_CONTAINER est optionnel si le conteneur est configuré avec /setup.

### Lancement

```bash
python -m bot.main
```

---

## Déploiement Portainer

Le projet fournit un Dockerfile, un docker-compose.yml et une image GitHub Container Registry.

Image par défaut :

```text
ghcr.io/choupivip/atm10-discord-manager:latest
```

Dans Portainer :

1. Créer une nouvelle Stack.
2. Coller le contenu de docker-compose.yml.
3. Ajouter les variables DISCORD_TOKEN, AUTHORIZED_ROLE et DOCKER_CONTAINER.
4. Déployer la stack.

Le compose monte le socket Docker pour permettre au bot de gérer le conteneur Minecraft :

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Les données persistantes du bot sont stockées dans les volumes Docker atm10-discord-manager-data et atm10-discord-manager-logs.

### Build local

```bash
docker build -t atm10-discord-manager:local .
docker compose up -d
```

### Publication GitHub automatique

Le workflow .github/workflows/docker.yml construit et publie automatiquement l'image sur GHCR lors des push sur main/master et lors des tags v*.*.*.

---
## Docker

Le bot communique avec Docker via le Docker SDK Python. Sur un hôte Linux, il doit avoir accès au socket Docker :

```text
/var/run/docker.sock
```

Exemple de montage avec Docker Compose :

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

---

## Architecture

```text
atm10-discord-manager/
├── bot/
│   ├── cogs/
│   │   ├── dashboard.py
│   │   ├── ping.py
│   │   ├── server.py
│   │   ├── setup.py
│   │   └── status.py
│   ├── embeds/
│   │   ├── dashboard_embed.py
│   │   └── server_embed.py
│   ├── services/
│   │   ├── dashboard_service.py
│   │   ├── docker_service.py
│   │   └── minecraft_service.py
│   ├── tasks/
│   │   └── dashboard_task.py
│   ├── views/
│   │   ├── confirm_view.py
│   │   └── dashboard_view.py
│   ├── config.py
│   ├── config_manager.py
│   ├── logger.py
│   └── main.py
├── data/
├── logs/
├── tests/
├── .dockerignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── README.md
├── CHANGELOG.md
└── requirements.txt
```

### Flux principal

```text
Discord Slash Commands / Buttons
        |
        v
Cogs and Views
        |
        v
MinecraftService
        |
        v
DockerService
        |
        v
Docker Engine
```

### Services

- DashboardService : persistance du message dashboard dans data/dashboard.json
- MinecraftService : actions métier start, stop, restart, status
- DockerService : communication avec le Docker SDK

---

## Roadmap

### v0.6.0

- Dashboard permanent
- Actualisation automatique
- Boutons persistants
- Sauvegarde de l'ID du message

### v0.7.0

- Connexion RCON
- Liste des joueurs réelle
- Commandes Minecraft depuis Discord
- Sauvegarde du monde

### v0.8.0

- Lecture des logs Minecraft
- Détection des connexions et déconnexions
- Détection des morts
- Détection des crashs

### v0.9.0

- Backups automatiques
- Notifications Discord
- Monitoring avancé
- CPU, RAM, disque, TPS en temps réel

### v1.0.0

- Version stable
- Dashboard complet proche de Pterodactyl
- Gestion serveur, logs, backups, monitoring et notifications

---

## Qualité

Le projet vise une base professionnelle : PEP8, Cogs Discord propres, slash commands, services séparés, logger centralisé et code extensible vers RCON, logs, backups et monitoring.

---

## Auteur

Développé par Choupivip pour un serveur privé All the Mods 10: To the Sky.
