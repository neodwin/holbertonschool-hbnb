#!/bin/bash

# Ce script exporte les diagrammes Mermaid en images PNG
# Nécessite Node.js et @mermaid-js/mermaid-cli

# Vérifier si mmdc est installé
if ! command -v mmdc &> /dev/null; then
    echo "mmdc n'est pas installé. Installation en cours..."
    npm install -g @mermaid-js/mermaid-cli
fi

# Créer le répertoire pour les images
mkdir -p images

# Fonction pour extraire et exporter les diagrammes Mermaid d'un fichier Markdown
extract_and_export() {
    local file=$1
    local basename=$(basename "$file" .md)
    local count=1
    
    # Extraire les blocs Mermaid
    grep -n "^```mermaid" "$file" | while read -r line; do
        start_line=$(echo "$line" | cut -d: -f1)
        end_line=$(tail -n +$start_line "$file" | grep -n "^```" | head -n 1 | cut -d: -f1)
        end_line=$((start_line + end_line - 1))
        
        # Extraire le contenu du bloc Mermaid
        mermaid_content=$(sed -n "$((start_line+1)),$((end_line-1))p" "$file")
        
        # Créer un fichier temporaire pour le contenu Mermaid
        temp_file=$(mktemp)
        echo "$mermaid_content" > "$temp_file"
        
        # Exporter en PNG
        output_file="images/${basename}_${count}.png"
        echo "Exportation de $file (diagramme $count) vers $output_file..."
        mmdc -i "$temp_file" -o "$output_file" -t dark
        
        # Supprimer le fichier temporaire
        rm "$temp_file"
        
        count=$((count+1))
    done
}

# Exporter tous les diagrammes
for file in *.md; do
    if [ "$file" != "README.md" ]; then
        extract_and_export "$file"
    fi
done

echo "Exportation terminée. Les images sont dans le répertoire 'images'." 