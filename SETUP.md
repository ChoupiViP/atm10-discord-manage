# 🔧 Configuration du Container Docker

## Vue d'ensemble

La nouvelle commande `/setup` permet de configurer facilement le container Docker utilisé par le bot, **sans avoir besoin de redémarrer le bot à chaque changement**.

La configuration est **persistante** : elle reste même après le redémarrage du bot.

---

## Utilisation

### Option 1 : Via le menu interactif

```
/setup
```

Le bot affichera une liste de tous les containers Docker disponibles. Sélectionnez le container désiré via le menu déroulant.

**Permissions requises :** Rôle `Admin` (configurable via `.env`)

### Option 2 : Via paramètre direct

```
/setup container:mon-serveur-minecraft
```

Remplacez `mon-serveur-minecraft` par le nom exact du container.

---

## Configuration initiale

### Via `.env` (méthode traditionnelle)

```env
DOCKER_CONTAINER=mon-serveur-minecraft
```

### Via `/setup` (méthode interactive - recommandée)

1. Utilisez `/setup` pour afficher la liste des containers
2. Sélectionnez le container désiré
3. La configuration est sauvegardée automatiquement

---

## Persistance des données

La configuration est sauvegardée dans `data/config.json` :

```json
{
  "docker_container": "mon-serveur-minecraft"
}
```

### Avantages :
- ✅ La configuration survit aux redémarrages du bot
- ✅ Pas besoin de modifier `.env`
- ✅ Facile à changer à tout moment
- ✅ Historique des configurations (extensible)

---

## Priorité de configuration

Le bot recherche le container dans cet ordre :

1. **Variable `.env`** (`DOCKER_CONTAINER=...`) - Priorité maximale
2. **Configuration persistante** (`data/config.json`) - Utilisée si `.env` n'est pas défini
3. **Erreur** - Si aucune des deux n'existe

**Conseil :** Laissez `.env` vide et utilisez `/setup` pour plus de flexibilité.

---

## Exemple complet

### Première utilisation

```
1. /setup
2. Sélectionnez "atm10-minecraft" dans le menu
3. Le bot confirme : "✅ Container configuré : atm10-minecraft"
```

### Changer de container

```
1. /setup
2. Sélectionnez "autre-serveur" dans le menu
3. Le bot confirme automatiquement
```

### Vérifier le container actuel

```
/status
```

Le container utilisé s'affiche dans la réponse.

---

## Dépannage

### "Aucun container Docker trouvé"
- Vérifiez que le socket Docker est correctement monté dans le container
- Vérifiez que Docker est actif sur le serveur
- Consultez les logs du bot

### "Container non trouvé"
- Assurez-vous du nom exact du container
- Utilisez `/setup` sans paramètre pour voir la liste exacte des noms

### "Vous n'avez pas la permission"
- Seuls les utilisateurs avec le rôle `Admin` (ou celui configuré en `.env`) peuvent utiliser `/setup`

---

## Commandes liées

```
/setup                    # Configure le container (menu interactif)
/setup container:nom      # Configure le container (direct)
/status                   # Affiche l'état du container configuré
/server status            # Alias de /status
```

---

## Fichiers modifiés

- `bot/config_manager.py` - Nouveau : gestionnaire de configuration persistante
- `bot/config.py` - Modification : support de la configuration dynamique
- `bot/services/docker_service.py` - Modification : utilise la config dynamique
- `bot/cogs/setup.py` - Nouveau : commande `/setup`
- `data/config.json` - Nouveau : fichier de configuration persistante (auto-généré)
