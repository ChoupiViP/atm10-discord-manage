# Changelog

Toutes les modifications importantes du projet sont documentées dans ce fichier.

Le format suit les recommandations de Keep a Changelog.

---

## [0.9.0] - 2026-07-11

### Ajouté

- Commandes `/link`, `/unlink` et `/myprofile` pour lier Discord à un pseudo Minecraft.
- Validation du lien par code envoyé depuis le chat Minecraft.
- Stockage des associations `Discord ID ↔ pseudo Minecraft`.
- Chat Discord → Minecraft stylé avec `tellraw` pour supprimer le préfixe `[Rcon]`.
- Affichage du pseudo Discord associé dans les messages Minecraft relayés.

### Modifié

- Mise à jour du README pour documenter la liaison Discord/Minecraft et le chat stylé.
- Amélioration du relais Minecraft → Discord pour afficher le lien du joueur.

### Corrigé

- Stabilisation du pont chat Discord/Minecraft.
- Réduction du bruit d’affichage inutile via RCON.

---

## [0.8.0] - 2026-07-11

### Ajouté

- Synchronisation du chat Minecraft ↔ Discord via le salon Logs.
- Envoi automatique des messages de mort Minecraft dans le canal Logs.
- Passage des messages Discord postés dans le salon Logs vers le chat Minecraft.
- Filtrage des messages de retour pour éviter les boucles de chat.
- Ajout de `bot/tasks/minecraft_chat_task.py` pour suivre les logs Docker Minecraft.
- Ajout de `bot/cogs/minecraft_bridge.py` pour relayer Discord vers Minecraft.

### Modifié

- Extension de la configuration Logs pour servir de canal de logs et de chat.
- Mise à jour du README pour documenter la synchronisation de chat et les notifications de mort.

### Corrigé

- Amélioration de la robustesse du pont chat Discord/Minecraft.

---

## [0.6.0] - 2026-07-01

### Ajouté

- Commandes /dashboard create, /dashboard delete et /dashboard refresh.
- Dashboard Discord permanent basé sur un message unique.
- Sauvegarde de guild_id, channel_id et message_id dans data/dashboard.json.
- View persistante avec boutons Start, Stop, Restart et Refresh.
- custom_id stable pour chaque bouton du dashboard.
- Enregistrement de la View persistante au démarrage du bot avec add_view().
- Tâche d'actualisation automatique toutes les 15 secondes.
- DashboardService dédié à la persistance du dashboard.
- Embed dashboard enrichi avec serveur, Docker, conteneur, CPU, RAM, disque, uptime, joueurs, TPS et dernière mise à jour.
- Test de cycle de vie pour DashboardService.
- Dockerfile prêt pour l'image de production.
- docker-compose.yml prêt pour une stack Portainer.
- .dockerignore pour alléger le contexte de build.
- .env.example pour documenter les variables de déploiement.
- Workflow GitHub Actions pour publier automatiquement l'image sur GHCR.

### Modifié

- Refonte du Cog dashboard autour d'un groupe de commandes slash /dashboard.
- Renforcement de DockerService avec un statut normalisé pour le dashboard.
- Ajout de l'API MinecraftService.status() tout en conservant get_status() pour compatibilité.
- Déplacement des appels Docker synchrones hors de la boucle Discord avec asyncio.to_thread().
- Démarrage automatique de la tâche dashboard dans bot/main.py.
- Documentation README mise à jour pour la v0.6.0.

### Corrigé

- Suppression de l'ancien code mort du dashboard.
- Suppression du risque de création de plusieurs messages dashboard.
- Nettoyage automatique de dashboard.json si le message Discord enregistré n'existe plus.
- Gestion plus robuste des erreurs Docker dans l'embed et dans les boutons.

---

## [0.5.0] - 2026-06-30

### Ajouté

- Commandes /server.
- Démarrage du serveur.
- Arrêt du serveur.
- Redémarrage du serveur.
- Gestion des permissions.
- Dashboard Discord initial.
- Boutons de confirmation.
- Embeds personnalisés.

### Modifié

- Refonte de l'architecture.
- Séparation en services.
- Amélioration de DockerService.

### Corrigé

- Gestion des erreurs Docker.
- Amélioration de la stabilité.

---

## [0.4.0]

### Ajouté

- MinecraftService.
- Architecture en couches.
- Commande /server status.

---

## [0.3.0]

### Ajouté

- Docker SDK.
- DockerService.

---

## [0.2.0]

### Ajouté

- Logger.
- Configuration.
- Cogs.

---

## [0.1.0]

### Ajouté

- Première version.
- Commande /ping.
