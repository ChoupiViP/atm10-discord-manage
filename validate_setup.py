#!/usr/bin/env python3
"""
Script de validation de l'installation de la fonctionnalité /setup
"""

import json
from pathlib import Path

def check_files():
    """Vérifie que tous les fichiers nécessaires existent"""
    
    files_to_check = [
        ("bot/config_manager.py", "Gestionnaire de configuration persistante"),
        ("bot/config.py", "Fichier de configuration modifié"),
        ("bot/cogs/setup.py", "Cog de la commande /setup"),
        ("bot/services/docker_service.py", "Service Docker modifié"),
        ("data/.gitkeep", "Dossier data"),
        ("SETUP.md", "Documentation /setup"),
    ]
    
    print("=" * 60)
    print("🔍 Vérification des fichiers...")
    print("=" * 60)
    
    all_good = True
    
    for file_path, description in files_to_check:
        full_path = Path(__file__).parent / file_path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        
        print(f"{status} {description:<40} {file_path}")
        
        if not exists:
            all_good = False
    
    return all_good

def check_imports():
    """Vérifie que les imports fonctionnent correctement"""
    
    print("\n" + "=" * 60)
    print("🔌 Vérification des imports...")
    print("=" * 60)
    
    try:
        from bot.config_manager import ConfigManager
        print("✅ ConfigManager importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur lors de l'import de ConfigManager: {e}")
        return False
    
    try:
        from bot.config import Config
        print("✅ Config importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur lors de l'import de Config: {e}")
        return False
    
    try:
        from bot.services.docker_service import DockerService
        print("✅ DockerService importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur lors de l'import de DockerService: {e}")
        return False
    
    return True

def check_config_structure():
    """Vérifie la structure du fichier de configuration"""
    
    print("\n" + "=" * 60)
    print("📋 Vérification de la structure...")
    print("=" * 60)
    
    try:
        from bot.config_manager import ConfigManager
        
        # Test de création du fichier de configuration
        config_file = Path(__file__).parent / "data" / "config.json"
        
        # S'assurer que le dossier existe
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Tester la sauvegarde
        ConfigManager.set_docker_container("test-container")
        print("✅ Configuration sauvegardée avec succès")
        
        # Vérifier le fichier
        if config_file.exists():
            with open(config_file, "r") as f:
                data = json.load(f)
            print(f"✅ Fichier config.json créé: {data}")
        else:
            print("❌ Le fichier config.json n'a pas été créé")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    print("\n")
    print(" 🚀 VALIDATION DU SETUP /setup ".center(60, "="))
    print()
    
    checks = [
        ("Fichiers", check_files()),
        ("Imports", check_imports()),
        ("Structure", check_config_structure()),
    ]
    
    print("\n" + "=" * 60)
    print("📊 Résumé")
    print("=" * 60)
    
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    all_passed = all(result for _, result in checks)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ VALIDATION RÉUSSIE - Tout est prêt !".center(60))
        print("=" * 60)
        print("\n📌 Prochaines étapes:")
        print("   1. Démarrez le bot: python -m bot.main")
        print("   2. Utilisez la commande: /setup")
        print("   3. Sélectionnez votre container Docker")
        print("\n📖 Pour plus de détails: voir SETUP.md\n")
    else:
        print("❌ VALIDATION ÉCHOUÉE - Vérifiez les erreurs ci-dessus".center(60))
        print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
