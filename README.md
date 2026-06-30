# 🎮 ATM10 Discord Manager

> Modern Discord bot to manage a **Minecraft All the Mods 10: To the Sky** server running in Docker.

![Version](https://img.shields.io/badge/version-v0.5.0-blue)
![Python](https://img.shields.io/badge/Python-3.13-yellow)
![Discord.py](https://img.shields.io/badge/discord.py-2.6-5865F2)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Description

ATM10 Discord Manager est un bot Discord développé en **Python** permettant d'administrer un serveur **Minecraft All the Mods 10: To the Sky** hébergé dans **Docker**.

L'objectif est de remplacer progressivement Portainer pour toutes les opérations courantes grâce à une interface moderne utilisant :

- 🎮 Commandes Slash
- 🎨 Embeds Discord
- 🔘 Boutons interactifs
- 🐳 Docker
- 📡 RCON *(prochainement)*

---

# ✨ Fonctionnalités

## ✅ Actuellement disponibles

- Bot Discord
- Architecture modulaire (Cogs)
- Logger personnalisé
- Configuration via `.env`
- Docker SDK
- Architecture en couches
- Gestion des erreurs Docker
- Permissions
- Embeds personnalisés
- Boutons de confirmation
- Dashboard Discord (première version)

### Commandes

```
/ping
/status

/server status
/server start
/server stop
/server restart

/dashboard
```

---

# 🗂 Architecture

```
atm10-discord-manager/
│
├── bot/
│   ├── cogs/
│   ├── embeds/
│   ├── exceptions/
│   ├── models/
│   ├── services/
│   ├── tasks/
│   ├── utils/
│   ├── views/
│   ├── config.py
│   ├── logger.py
│   └── main.py
│
├── config/
├── data/
├── docker/
├── logs/
├── tests/
│
├── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
└── .env
```

---

# 🏗 Architecture logicielle

```
Discord

      │

      ▼

Discord Cogs

      │

      ▼

MinecraftService

      │

      ▼

DockerService

      │

      ▼

Docker Engine
```

---

# 🐳 Docker

Le bot est conçu pour fonctionner sur Debian.

Connexion via :

```
/var/run/docker.sock
```

Montage Docker :

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

---

# 🛠 Technologies

- Python 3.13
- discord.py
- Docker SDK for Python
- python-dotenv
- Docker
- Git
- GitHub

---

# 🗺 Roadmap

## ✅ v0.1.0

- Création du bot
- Première commande Slash

---

## ✅ v0.2.0

- Architecture modulaire
- Logger
- Configuration

---

## ✅ v0.3.0

- Docker SDK
- DockerService

---

## ✅ v0.4.0

- MinecraftService
- Architecture en couches
- `/server status`

---

## ✅ v0.5.0

- `/server start`
- `/server stop`
- `/server restart`
- Gestion des permissions
- Gestion des erreurs Docker
- Embeds personnalisés
- Boutons de confirmation
- Dashboard Discord (v1)

---

## 🚧 v0.6.0

- Dashboard permanent
- Actualisation automatique
- Boutons persistants
- Sauvegarde de l'ID du message

---

## 🚧 v0.7.0

- Connexion RCON
- Liste des joueurs
- Messages Minecraft
- Sauvegarde du monde

---

## 🚧 v0.8.0

- Lecture des logs
- Détection des connexions
- Détection des morts
- Détection des crashs

---

## 🚧 v0.9.0

- Sauvegardes automatiques
- Notifications Discord
- Statistiques serveur

---

## 🎉 v1.0.0

Première version stable.

Fonctionnalités prévues :

- Gestion complète du serveur
- Dashboard interactif
- Docker
- RCON
- Sauvegardes
- Surveillance
- Gestion des permissions
- Déploiement Docker Compose

---

# 🎯 Objectif

Créer un véritable panneau d'administration Discord permettant de gérer entièrement un serveur Minecraft sans ouvrir Portainer.

---

# 👨‍💻 Auteur

Développé par **Choupivip**

Projet personnel réalisé autour d'un serveur privé **All the Mods 10: To the Sky**.