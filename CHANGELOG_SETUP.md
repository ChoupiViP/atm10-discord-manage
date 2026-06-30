# 📝 Changements - Commande /setup

## 🎯 Objectif
Ajouter une commande `/setup` pour configurer le container Docker de manière persistante, sans redémarrage du bot.

## ✅ Changements effectués

### 📁 Fichiers créés

#### 1. **`bot/config_manager.py`** - Nouveau gestionnaire de configuration
- Gère la persistance des configurations en JSON
- Crée automatiquement le dossier `data/` et le fichier `config.json`
- Méthodes principales:
  - `get_docker_container()` - Récupère le container configuré
  - `set_docker_container(name)` - Définit le container
  - `get_guild_config()` / `set_guild_config()` - Pour des configurations par serveur (extensible)

#### 2. **`bot/cogs/setup.py`** - Nouvelle commande Discord
- Commande `/setup` avec 2 modes:
  - Mode interactif: liste tous les containers Docker avec menu déroulant
  - Mode direct: `/setup container:nom-du-container`
- Classe `SetupView`: gère l'interface de sélection
- Vérification des permissions (Admin)
- Gestion des erreurs Docker

#### 3. **`data/.gitkeep`** - Dossier de données
- Assure que le dossier `data/` est versionné
- Stocke `config.json` (créé automatiquement)

#### 4. **`SETUP.md`** - Documentation
- Guide complet d'utilisation de `/setup`
- Exemples d'utilisation
- Dépannage

#### 5. **`validate_setup.py`** - Script de validation
- Vérifie que tout est installé correctement
- Teste les imports et la structure
- Usage: `python validate_setup.py`

### 🔧 Fichiers modifiés

#### 1. **`bot/config.py`**
```python
# AVANT
DOCKER_CONTAINER = os.getenv("DOCKER_CONTAINER")

# APRÈS
@classmethod
def get_docker_container(cls):
    env_container = os.getenv("DOCKER_CONTAINER")
    if env_container:
        return env_container
    persisted_container = ConfigManager.get_docker_container()
    if persisted_container:
        return persisted_container
    raise ValueError("...")
```

**Impact**: Permet de récupérer le container de `.env` ou de la configuration persistante.

#### 2. **`bot/services/docker_service.py`**
```python
# AVANT
container_name = Config.DOCKER_CONTAINER

# APRÈS
container_name = Config.get_docker_container()
```

**Impact**: Utilise la méthode dynamique au lieu de la propriété statique.

#### 3. **`README.md`**
- Ajout de la commande `/setup` dans la liste
- Ajout du badge "Configuration persistante"
- Lien vers `SETUP.md`

## 🔄 Flux de configuration

```
┌─────────────────────────┐
│  Utilisateur utilise    │
│     /setup              │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  SetupView affiche      │
│  les containers         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  ConfigManager.         │
│  set_docker_container() │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Sauvegarde dans        │
│  data/config.json       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Au prochain appel:     │
│  Config.get_docker...() │
│  Lit depuis config.json │
└─────────────────────────┘
```

## 💾 Structure de `data/config.json`

```json
{
  "docker_container": "mon-serveur-minecraft",
  "guilds": {
    "12345": {
      "some_setting": "value"
    }
  }
}
```

## 🔐 Priorités de configuration

1. **`.env` (`DOCKER_CONTAINER=...`)**
   - Priorité maximale
   - À utiliser pour les déploiements en production
   
2. **`data/config.json` (via `/setup`)**
   - Utilisée si `.env` n'est pas défini
   - À utiliser pour une flexibilité maximale
   
3. **Erreur**
   - Si aucune des deux n'existe

## 🚀 Utilisation

### Installation

```bash
# Le code est prêt à utiliser, pas de dépendances supplémentaires
```

### Validation

```bash
python validate_setup.py
```

### Utilisation

```
/setup                           # Mode interactif
/setup container:mon-container   # Mode direct
```

## 🔗 Intégrations

- ✅ **Bot loading**: Le cog se charge automatiquement (aucune modification nécessaire)
- ✅ **Permissions**: Utilise le système existant (`Permissions.has_permission()`)
- ✅ **Logger**: Intégration avec le logger personnalisé
- ✅ **Docker Service**: Automatiquement compatible

## 📚 Exemple d'utilisation complet

```
1. Utilisateur: /setup
2. Bot affiche:
   🔧 Configuration du container Docker
   
   Sélectionnez le container Docker à utiliser par défaut.
   
   1. atm10-minecraft - Status: running
   2. autres-container - Status: exited
   3. test-container - Status: running

3. Utilisateur sélectionne "atm10-minecraft"
4. Bot répond:
   ✅ Container configuré
   Le container atm10-minecraft a été défini par défaut.

5. Fichier data/config.json créé:
   {
     "docker_container": "atm10-minecraft"
   }

6. Les commandes suivantes utilisent ce container:
   /status
   /server status
   /server start
   /server stop
   /server restart
```

## ⚠️ Notes importantes

- **Pas de redémarrage nécessaire** - La configuration change immédiatement
- **Persistance** - La configuration survit au redémarrage du bot
- **Multi-serveur ready** - La structure permet des configurations par serveur (future extension)
- **Extensibilité** - Le système peut être étendu pour d'autres configurations

## 🐛 Dépannage

### Le cog ne charge pas?
- Vérifiez que `bot/cogs/setup.py` existe
- Vérifiez les logs du bot

### `/setup` dit "Aucun container trouvé"
- Vérifiez que Docker est actif
- Vérifiez que le socket Docker est correctement monté

### Import Error?
- Exécutez `python validate_setup.py`
- Vérifiez les chemins des fichiers

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| Fichiers créés | 5 |
| Fichiers modifiés | 3 |
| Lignes de code | ~350 |
| Nouvelles commandes | 1 |
| Nouvelles dépendances | 0 |

## 🎉 Résumé

✅ Configuration persistante du container Docker  
✅ Commande `/setup` interactive et directe  
✅ Pas de redémarrage nécessaire  
✅ Interface utilisateur moderne avec embeds et menus  
✅ Gestion d'erreurs complète  
✅ Documentation complète  
✅ Validation de l'installation  
✅ Extensible pour les configurations futures
