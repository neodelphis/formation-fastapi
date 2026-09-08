#!/bin/bash

# ### Procédure md vers pdf avec mermaid
# Procédure pour la transformation du document markdown en pdf qui affiche correctement les schémas mermaid:
#
# 1. copier le document mon_document.md dans mon_document.qmd
# 2. dans mon_document.qmd tranformer tous les ```mermaid en ```{mermaid}
# 3. lancer la commande:
# quarto render mon_document.qmd --to pdf
# 4. supprimer le document mon_document.qmdv
#
# ### Comment l'utiliser
# 1. **Rendez le script exécutable** (à faire une seule fois) en tapant cette commande dans votre terminal :
# ```bash
# chmod +x md2pdf.sh
# ```
# 2. **Lancez le script** en lui passant votre document en paramètre :
# ```bash
# ./md2pdf.sh mon_document.md
# ```

# Vérifie si un fichier a été fourni en argument
if [ -z "$1" ]; then
  echo "Utilisation: $0 nom_du_fichier.md"
  exit 1
fi

FICHIER_MD="$1"
# Extrait le nom du fichier sans l'extension .md
NOM_BASE=$(basename "$FICHIER_MD" .md)
FICHIER_QMD="${NOM_BASE}.qmd"

echo "⚙️  Génération du PDF pour $FICHIER_MD..."

# Étape 1 & 2 : Copie et remplace ```mermaid par ```{mermaid}
# La commande sed lit le fichier .md, modifie le texte et crée le .qmd
sed 's/^```mermaid/```{mermaid}/g' "$FICHIER_MD" > "$FICHIER_QMD"

# Étape 3 : Rendu avec Quarto
quarto render "$FICHIER_QMD" --to pdf

# Étape 4 : Nettoyage du fichier temporaire
rm "$FICHIER_QMD"

echo "✅ Terminé ! Le PDF est prêt."

