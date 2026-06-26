# 🎮 ATM10 Discord Manager

> Un bot Discord moderne permettant de gérer un serveur **Minecraft All the Mods 10: To the Sky** hébergé avec **Docker**.

![Version](https://img.shields.io/badge/version-v0.3.0-blue)
![Python](https://img.shields.io/badge/Python-3.13-yellow)
![Discord.py](https://img.shields.io/badge/discord.py-2.6-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Status](https://img.shields.io/badge/Status-En%20développement-orange)

---

# ✨ Présentation

ATM10 Discord Manager est un projet personnel permettant de piloter un serveur Minecraft directement depuis Discord.

L'objectif est de remplacer l'utilisation de Portainer pour les tâches courantes grâce à une interface moderne utilisant les commandes Slash, des embeds et des boutons interactifs.

---

# 🚀 Fonctionnalités

## ✅ Actuellement disponibles

- Bot Discord
- Architecture modulaire (Cogs)
- Chargement automatique des extensions
- Logger personnalisé
- Configuration via `.env`
- Commandes Slash
- `/ping`
- `/status`
- Architecture prête pour Docker

---

# 🚧 En développement

- Intégration Docker
- Contrôle du serveur Minecraft
- Dashboard Discord
- RCON
- Sauvegardes automatiques
- Détection des joueurs
- Détection des morts
- Surveillance des logs
- Alertes de crash

---

# 📁 Structure du projet

```text
atm10-discord-manager/
│
├── bot/
│   ├── cogs/
│   │   ├── docker.py
│   │   ├── ping.py
│   │   └── status.py
│   │
│   ├── embeds/
│   ├── services/
│   │   └── docker_service.py
│   │
│   ├── tasks/
│   ├── utils/
│   ├── views/
│   │
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
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🛠️ Technologies

- Python 3.13
- discord.py
- Docker SDK
- python-dotenv
- Git
- GitHub

---

# 🐳 Docker

Le projet est conçu pour fonctionner sur un serveur Debian.

Le bot communiquera directement avec Docker grâce au socket :

```text
/var/run/docker.sock
```

Exemple de montage :

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Cette méthode permet au bot de contrôler directement le conteneur Minecraft sans exposer l'API Docker sur le réseau.

---

# 📌 Roadmap

## ✅ v0.1.0

- Création du bot
- Première commande Slash

---

## ✅ v0.2.0

- Architecture professionnelle
- Chargement automatique des Cogs
- Logger
- Configuration centralisée
- `/ping`
- `/status`

---

## ✅ v0.3.0

- Intégration du Docker SDK
- Création de `DockerService`
- Préparation de la communication avec Docker
- Structure des services
- Base du contrôle du serveur

---

## 🔄 v0.4.0

- `/server status`
- `/server start`
- `/server stop`
- `/server restart`

---

## 📡 v0.5.0

- Connexion RCON
- Liste des joueurs
- Envoi de messages Minecraft
- Sauvegarde du monde

---

## 📊 v0.6.0

- Dashboard Discord
- Mise à jour automatique
- Boutons interactifs
- Statut du serveur en temps réel

---

## 📜 v0.7.0

- Lecture des logs
- Détection des connexions
- Détection des déconnexions
- Détection des morts
- Détection des crashs

---

## 💾 v0.8.0

- Sauvegardes automatiques
- Notifications Discord
- Rotation des sauvegardes

---

## 🏆 v1.0.0

Première version stable.

Fonctionnalités prévues :

- Gestion complète du serveur Minecraft
- Dashboard interactif
- Docker
- RCON
- Sauvegardes
- Détection des événements
- Système de permissions
- Déploiement complet avec Docker Compose

---

# 🎯 Objectif

Pouvoir gérer entièrement un serveur Minecraft ATM10 To the Sky sans ouvrir Portainer.

À terme, le bot permettra notamment :

- 🚀 Démarrer le serveur
- ⏹ Arrêter le serveur
- 🔄 Redémarrer le serveur
- 👥 Voir les joueurs connectés
- 💬 Envoyer des messages dans le chat Minecraft
- 📊 Consulter les performances
- 💀 Recevoir les notifications de morts
- 📦 Effectuer des sauvegardes
- 🔔 Être alerté en cas de crash

---

# 👨‍💻 Auteur

Développé par **Johann Glotin**.

Projet réalisé dans le cadre d'un serveur privé **All the Mods 10: To the Sky**.