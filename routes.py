from app import app
from flask import render_template, request, flash, redirect, url_for
from app.metadata import extract_metadata
import os

# Chemin pour enregistrer temporairement les fichiers
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('upload.html')  # Affiche le formulaire de téléchargement

@app.route('/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        file = request.files.get('file')  # Récupérer le fichier
        
        # Vérifier si un fichier a été sélectionné
        if not file or file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(url_for('home'))

        # Vérifier le type de fichier
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.mp4', '.avi', '.mov')):
            flash('Type de fichier non supporté', 'error')
            return redirect(url_for('home'))

        # Sauvegarder le fichier temporairement
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Extraire les métadonnées
        metadata = extract_metadata(file_path)
        
        if not metadata:
            flash('Aucune métadonnée trouvée pour ce fichier.', 'error')
            return redirect(request.url)

        # Supprimer le fichier après traitement (optionnel)
        os.remove(file_path)

        return render_template('result.html', metadata=metadata)  # Afficher les métadonnées
