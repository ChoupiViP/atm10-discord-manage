# 🎮 ATM10 Discord Manager

> Gestionnaire Discord moderne pour administrer un serveur **Minecraft All the Mods 10: To the Sky** directement depuis Discord.

ATM10 Discord Manager est un bot Discord développé en **Python** permettant de contrôler un serveur Minecraft hébergé sous **Docker**, grâce aux commandes Slash, à une architecture modulaire et à une configuration entièrement réalisable depuis Discord.

---

# 📌 Table des matières

- [✨ Fonctionnalités](#-fonctionnalit%C3%A9s)
- [📁 Architecture](#-architecture)
- [⚙️ Configuration](#-configuration)
- [🐳 Docker](#-docker)
- [📡 RCON](#-rcon)
- [🛠️ Technologies](#-technologies)
- [🚀 Installation](#-installation)
- [📅 Roadmap](#-roadmap)

---

# 🚀 Installation

## Prérequis

- Python 3.12+ ou 3.13
- Docker
- Docker Compose
- RCON activé sur votre serveur Minecraft
- Un token Discord valide

## Installation locale

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

## Configuration

1. Copier ou créer un fichier `.env` à la racine.
2. Ajouter votre token Discord et les variables nécessaires :

```env
DISCORD_TOKEN=VotreTokenDiscord
DOCKER_CONTAINER=Votre serveur Doker minecraft
AUTHORIZED_ROLE=role (ex : Admin)
TZ=votre zone de temps (ex : Europe/Paris)
```

La configuration RCON est maintenant gérée via `/setup` dans Discord.

## Démarrage

```bash
python bot/main.py
```

## Recommandation Docker Compose

Si vous utilisez Docker Compose, montez le socket Docker :

```yaml
services:
  bot:
    build: .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

---

# ✨ Fonctionnalités

## ✅ v0.8.0

### ⚙️ Nouvelles fonctionnalités

- Gestion dédiée du chat Minecraft vers Discord via un salon Discord spécifique
- Publication des morts Minecraft dans un canal Discord configuré
- Détection des messages de chat Minecraft dans les logs Docker
- Suppression du bruit lié aux logs RCON Listener / RCON Client
- Nettoyage des préfixes `>....` avant analyse des logs

### ⚙️ Configuration

- Configuration complète via `/setup`
- Sélection du conteneur Docker
- Configuration RCON
- Configuration du salon Dashboard
- Configuration du salon Logs pour les événements et erreurs
- Configuration du salon Chat Minecraft dédié
- Configuration du salon Mort Minecraft dédié
- Configuration du salon Notifications
- Réinitialisation de la configuration

### 🐳 Docker

- Communication avec Docker SDK
- Démarrage du serveur
- Arrêt du serveur
- Redémarrage du serveur
- Vérification de l'état du serveur

### 📡 RCON

- Connexion RCON
- Exécution de commandes
- Service dédié
- Préparation des futures commandes Minecraft

### 🏗️ Architecture

- Architecture modulaire
- Cogs Discord
- Services
- Views
- Modals
- Embeds
- Configuration persistante (JSON)

---

# 📁 Architecture

```text
atm10-discord-manager/
│
├── bot/
│
├── cogs/
│   ├── dashboard.py
│   ├── minecraft_bridge.py
│   ├── ping.py
│   ├── server.py
│   ├── setup.py
│   └── status.py
│
├── embeds/
│   ├── dashboard_embed.py
│   └── server_embed.py
│
├── modals/
│   └── rcon_modal.py
│
├── services/
│   ├── config_service.py
│   ├── dashboard_service.py
│   ├── docker_service.py
│   ├── minecraft_service.py
│   └── rcon_service.py
│
├── tasks/
│   └── minecraft_chat_task.py
│
├── utils/
│
├── views/
│   ├── channel_select_view.py
│   ├── dashboard_view.py
│   ├── docker_select_view.py
│   └── setup_view.py
│
├── config.py
├── logger.py
└── main.py
│
├── config/
├── data/
├── docker/
├── logs/
├── tests/
│
├── .env
├── README.md
├── CHANGELOG.md
├── LICENSE
└── requirements.txt
```

---

# 🏗️ Architecture logicielle

```text
                    Discord

                       │

               Slash Commands

                       │

                     Cogs

                       │

             MinecraftService

          ┌────────────┴────────────┐

          ▼                         ▼

  DockerService              RconService

          └────────────┬────────────┘

                       ▼

                ConfigService

                       │

                  config.json
```

Cette architecture permet de séparer :

- Interface Discord
- Logique métier
- Docker
- RCON
- Configuration

Le projet est ainsi plus simple à maintenir et à faire évoluer.

---

# ⚙️ Configuration

La configuration du bot se fait directement depuis Discord :

```text
/setup
```

Le menu permet de configurer :

- 🐳 Docker
- 📡 RCON
- 📊 Dashboard
- 📜 Logs (chat Minecraft / Discord)
- 🔔 Notifications

Toutes les informations sont sauvegardées automatiquement dans le fichier :

```text
config/config.json
```

---

# 🐳 Docker

Le bot communique directement avec Docker grâce au socket :

```text
/var/run/docker.sock
```

Exemple Docker Compose :

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Aucune API Docker n'est exposée sur Internet.

---

# 📡 RCON

Le bot utilise **mctools** pour communiquer avec Minecraft.

La configuration via `/setup` permet de définir plusieurs canaux :

- un salon Chat Discord dédié pour le chat Minecraft
- un salon Morts dédié aux notifications de décès
- un salon Logs pour les événements et les messages système

Fonctionnalités disponibles :

- Exécution de commandes
- Chat Minecraft
- Notifications de morts
- Liste des joueurs
- Arrêt propre du serveur

---

# 🛠️ Technologies

- Python 3.13
- discord.py 2.x
- Docker SDK
- MCTools
- python-dotenv
- Docker
- Portainer
- Git
- GitHub

---

# 📅 Roadmap

## ✅ v0.1.0

- Création du bot
- Première commande Slash

---

## ✅ v0.2.0

- Logger
- Configuration
- Architecture des Cogs

---

## ✅ v0.3.0

- Docker SDK
- DockerService

---

## ✅ v0.4.0

- MinecraftService
- Groupe `/server`

---

## ✅ v0.5.0

- Start
- Stop
- Restart
- Permissions

---

## ✅ v0.6.0

- Setup interactif
- Configuration Docker
- Configuration RCON
- Configuration Dashboard
- Configuration Logs
- Configuration Notifications
- ConfigService
- RconService
- Nouvelle architecture

---

## ✅ v0.7.0

Dashboard Discord interactif :

- Dashboard permanent
- Mise à jour automatique
- Boutons persistants
- Informations système
- Joueurs connectés
- Uptime
- CPU
- RAM

---

## ✅ v0.8.0

Événements Minecraft :

- Connexions
- Déconnexions
- Morts
- Crashs
- Logs Minecraft

---

## 🚧 v0.9.0

Sauvegardes :

- Sauvegardes automatiques
- Sauvegardes manuelles
- Rotation
- Compression

---

## 🏆 v1.0.0

Première version stable.

Fonctionnalités prévues :

- Dashboard complet
- Gestion complète du serveur
- Docker
- RCON
- Sauvegardes
- Logs
- Notifications
- Déploiement Docker
- Documentation complète

---

# 🎯 Objectif

Créer un gestionnaire Discord moderne permettant de piloter entièrement un serveur **Minecraft All the Mods 10: To the Sky** sans ouvrir Portainer.

Le bot permettra notamment :

- 🚀 Démarrer le serveur
- ⏹ Arrêter le serveur
- 🔄 Redémarrer le serveur
- 👥 Voir les joueurs connectés
- 💬 Envoyer des messages dans le chat Minecraft
- 📊 Consulter l'état du serveur
- 💀 Recevoir les notifications de morts
- 📦 Effectuer des sauvegardes
- 🔔 Être alerté en cas de crash

---

# 📌 État du projet

> 🚧 Projet actuellement en développement actif.

Version actuelle :

## **v0.8.0**

Le projet propose désormais une capture étendue du chat Minecraft, des notifications de morts et une gestion dédiée des canaux Discord via `/setup`.

---

# 👨‍💻 Auteur

**Johann Glotin**

Projet personnel développé autour d'un serveur privé **All the Mods 10: To the Sky**.

---

# 📄 Licence

Ce projet est distribué sous la licence **MIT**.

Consultez le fichier **LICENSE** pour plus d'informations.