import os
import sys

def rename_spaces_to_underscores(directory):
    # topdown=False traite les sous-dossiers avant les dossiers parents
    for root, dirs, files in os.walk(directory, topdown=False):
        
        # 1. Renommer les fichiers
        for name in files:
            if ' ' in name:
                old_path = os.path.join(root, name)
                new_name = name.replace(' ', '_')
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Fichier renommé : '{name}' -> '{new_name}'")

        # 2. Renommer les dossiers
        for name in dirs:
            if ' ' in name:
                old_path = os.path.join(root, name)
                new_name = name.replace(' ', '_')
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Dossier renommé : '{name}' -> '{new_name}'")

if __name__ == "__main__":
    # Utilise le dossier passé en argument, sinon le dossier courant (".")
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Sécurité : vérifier que le chemin existe
    if os.path.exists(target_dir):
        print(f"Analyse du répertoire : {os.path.abspath(target_dir)}")
        rename_spaces_to_underscores(target_dir)
        print("Terminé !")
    else:
        print(f"Erreur : Le chemin '{target_dir}' n'existe pas.")