# ⚡ Guide de démarrage rapide - /setup

## 🎯 Résumé en 30 secondes

La nouvelle commande `/setup` te permet de **choisir et configurer ton container Docker sans redémarrer le bot**. La configuration est **sauvegardée automatiquement** et **persiste** même après un redémarrage.

## 📦 Changements apportés

✅ Nouvelle commande Discord: `/setup`  
✅ Configuration persistante (fichier `data/config.json`)  
✅ Pas de redémarrage nécessaire  
✅ Interface interactive avec menu déroulant  
✅ Support du paramètre direct: `/setup container:nom`  

## 🚀 Utilisation

### Première utilisation

```
1. Tape: /setup
2. Sélectionne ton container dans le menu déroulant
3. C'est prêt ! La configuration est sauvegardée.
```

### Changer de container

```
1. Tape: /setup
2. Sélectionne le nouveau container
3. Confirmé - pas besoin de redémarrer le bot !
```

### Utilisation directe (optionnelle)

```
/setup container:atm10-minecraft
```

## 📁 Fichiers importants

| Fichier | Rôle |
|---------|------|
| `bot/config_manager.py` | Gère la sauvegarde en JSON |
| `bot/cogs/setup.py` | Commande Discord /setup |
| `data/config.json` | Sauvegarde la configuration (auto-créé) |
| `SETUP.md` | Documentation complète |
| `validate_setup.py` | Valide l'installation |

## ✅ Vérifier l'installation

```bash
python validate_setup.py
```

Doit afficher:
```
✅ VALIDATION RÉUSSIE - Tout est prêt !
```

## 🔧 Configuration persistante

Avant:
```
❌ Dépendant de .env uniquement
❌ Redémarrage nécessaire si changement
❌ Difficile à changer au runtime
```

Maintenant:
```
✅ Configurable via Discord
✅ Pas de redémarrage
✅ Priorité: .env > config.json > Erreur
```

## 📚 Documentation complète

Pour plus de détails: lire [SETUP.md](SETUP.md)

## ⚠️ Important

- **Permissions**: Seuls les admins (rôle `Admin` par défaut) peuvent utiliser `/setup`
- **Docker**: Le bot doit avoir accès à Docker (montage du socket)
- **Persistance**: La configuration est stockée dans `data/config.json` et survit aux redémarrages

## 🎓 Exemple

```
Avant:
/status → Erreur "DOCKER_CONTAINER manquant"
or
Dépendant du .env qui ne peut pas être modifié facilement

Après:
1. /setup → Menu interactif
2. Sélectionner "atm10-minecraft"
3. /status → Affiche l'état du serveur
4. Bot redémarre...
5. /status → Continue de fonctionner avec le même container!
```

## 🆘 Besoin d'aide?

1. Exécute `python validate_setup.py`
2. Consulte [SETUP.md](SETUP.md)
3. Vérifiez les logs du bot
4. Assurez-vous que Docker est actif
