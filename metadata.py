from PIL import Image
from PyPDF2 import PdfFileReader
import moviepy as mp
import io

def extract_metadata(file):
    metadata = {'name': file.filename, 'size': len(file.read())}
    file.seek(0)  # Remettre le curseur au début du fichier

    # Pour les images (avec Pillow)
    if file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        image = Image.open(file)
        metadata['image_format'] = image.format
        metadata['image_size'] = image.size
        metadata['image_mode'] = image.mode

    # Pour les vidéos (avec moviepy)
    elif file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        video = mp.VideoFileClip(file)
        metadata['video_duration'] = video.duration  # Durée de la vidéo en secondes
        metadata['video_fps'] = video.fps  # Fréquence d'images par seconde

    # Pour les fichiers PDF (avec PyPDF2)
    elif file.filename.lower().endswith('.pdf'):
        pdf = PdfFileReader(file)
        metadata['pdf_num_pages'] = pdf.getNumPages()
        metadata['pdf_author'] = pdf.getDocumentInfo().author

    return metadata
