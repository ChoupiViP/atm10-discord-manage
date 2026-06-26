# 🎮 ATM10 Discord Manager

> **Gestionnaire Discord moderne pour serveur Minecraft All the Mods 10: To the Sky**

ATM10 Discord Manager est un bot Discord développé en Python permettant de gérer un serveur Minecraft hébergé sous Docker directement depuis Discord grâce aux commandes Slash, des embeds modernes et, prochainement, des boutons interactifs.

---

# 🚀 Fonctionnalités

## ✅ Version v0.4.0

* Bot Discord entièrement fonctionnel
* Architecture modulaire avec Cogs
* Chargement automatique des extensions
* Logger personnalisé
* Configuration via `.env`
* Commandes Slash

  * `/ping`
  * `/status`
  * `/server status`
* Architecture en couches
* Services dédiés
* Préparation à Docker
* Préparation à RCON

---

# 📁 Architecture

```
atm10-discord-manager/
│
├── bot/
│
├── cogs/
│   ├── ping.py
│   ├── status.py
│   └── server.py
│
├── services/
│   ├── docker_service.py
│   └── minecraft_service.py
│
├── embeds/
├── tasks/
├── utils/
├── views/
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
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🏗️ Architecture logicielle

```
Discord
      │
      ▼
Server Cog
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

Cette architecture permet de séparer :

* l'interface Discord
* la logique métier
* la communication avec Docker

Le projet est ainsi plus simple à maintenir et à faire évoluer.

---

# 🐳 Docker

Le projet est prévu pour fonctionner sur un serveur Debian.

La communication avec Docker utilisera directement le socket :

```
/var/run/docker.sock
```

Montage Docker prévu :

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Cette méthode permet de piloter le serveur Minecraft sans exposer l'API Docker sur le réseau.

---

# 🛠️ Technologies

* Python 3.13
* discord.py 2.x
* Docker SDK for Python
* python-dotenv
* Git
* GitHub
* Docker
* Portainer

---

# 📅 Roadmap

## ✅ v0.1.0

* Création du bot
* Première commande Slash

---

## ✅ v0.2.0

* Architecture des Cogs
* Logger
* Configuration
* `/ping`
* `/status`

---

## ✅ v0.3.0

* Intégration du Docker SDK
* DockerService
* Base de communication avec Docker

---

## ✅ v0.4.0

* Création de MinecraftService
* Architecture en couches
* Groupe de commandes `/server`
* Première commande `/server status`
* Préparation des futures commandes serveur

---

## 🔄 v0.5.0

* `/server start`
* `/server stop`
* `/server restart`
* Gestion des permissions

---

## 📡 v0.6.0

* Connexion RCON
* `/server players`
* `/server say`
* `/server save`

---

## 📊 v0.7.0

* Dashboard Discord
* Boutons interactifs
* Mise à jour automatique
* Informations serveur en temps réel

---

## 📜 v0.8.0

* Lecture des logs Minecraft
* Détection des connexions
* Détection des déconnexions
* Détection des morts
* Détection des crashs

---

## 💾 v0.9.0

* Sauvegardes automatiques
* Notifications Discord
* Rotation des sauvegardes

---

## 🏆 v1.0.0

Première version stable.

Fonctionnalités prévues :

* Contrôle complet du serveur Minecraft
* Dashboard interactif
* Docker
* RCON
* Sauvegardes
* Détection des événements
* Gestion des permissions
* Déploiement complet via Docker Compose

---

# 🎯 Objectif

Créer un gestionnaire Discord moderne permettant de piloter entièrement un serveur **Minecraft All the Mods 10: To the Sky** sans ouvrir Portainer.

À terme, le bot permettra notamment :

* 🚀 Démarrer le serveur
* ⏹️ Arrêter le serveur
* 🔄 Redémarrer le serveur
* 👥 Voir les joueurs connectés
* 💬 Envoyer des messages dans le chat Minecraft
* 📊 Consulter l'état du serveur
* 💀 Recevoir les notifications de morts
* 📦 Effectuer des sauvegardes
* 🔔 Être alerté en cas de crash

---

# 📌 État du projet

> 🚧 Projet actuellement en développement actif.

Chaque nouvelle version apporte une fonctionnalité majeure en suivant une architecture évolutive et professionnelle.

---

# 👨‍💻 Auteur

Développé par **Choupivip**

Projet personnel réalisé autour d'un serveur privé **All the Mods 10: To the Sky**.
