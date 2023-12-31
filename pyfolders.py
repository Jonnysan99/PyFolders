# PyFolders
organizza e gestisci i tuoi file con facilità! Questo progetto Python ti consente di creare cartelle personalizzate e spostare i file in modo efficiente.
#STEP 1

import os
import shutil
import csv

# Ottieni il percorso della directory corrente
current_dir = os.getcwd()

# Crea il percorso completo per la cartella "files"
files_folder = os.path.join(current_dir, "files")

#verifica se il file di recap esiste già
recap_file = os.path.join(files_folder, 'recap.csv')
recap_exists = os.path.isfile(recap_file)

# Lista dei tipi di file supportati e relative estensioni
supported_extensions = {
    'audio': ['.mp3'],
    'docs': ['.txt', '.odt'],
    'images': ['.png', '.jpg', '.jpeg']
}

# Spostamento nella cartella "files"
os.chdir(files_folder)

# Creazione delle cartelle di destinazione se non esistono
for folder in supported_extensions.keys():
    os.makedirs(folder, exist_ok=True)

# Elaborazione dei file nella cartella "files"
file_info = []  # Lista per tenere traccia delle informazioni dei file

for filename in sorted(os.listdir()):
    file_path = os.path.join(files_folder, filename)

    # Ignora le sottocartelle e i file nascosti
    if os.path.isdir(file_path) or filename.startswith('.'):
        continue

    # Informazioni sul file
    name, ext = os.path.splitext(filename)
    file_type = None
    file_size = os.path.getsize(file_path)

    # Trova il tipo di file
    for file_category, extensions in supported_extensions.items():
        if ext.lower() in extensions:
            file_type = file_category
            break

    # Stampa le informazioni del file
    print(f'{name} type:{file_type} size:{file_size}B')

    # Sposta il file nella cartella corretta
    if file_type:
        dest_folder = os.path.join(files_folder, file_type)
        shutil.move(file_path, os.path.join(dest_folder, filename))

    # Aggiungi le informazioni del file alla lista
    file_info.append([name, file_type, file_size])

# Spostamento nella cartella corrente
os.chdir(current_dir)

# Aggiornamento o creazione del file di recap
with open(recap_file, 'a', newline='') as file:
    writer = csv.writer(file)

    # Scrivi l'intestazione del file se non esiste
    if not recap_exists:
        writer.writerow(['name', 'type', 'size'])

    # Scrivi le informazioni dei file
    writer.writerows(file_info)

print('Operazione completata!')
# STEP 2 


# Percorso della cartella corrente
current_folder = os.getcwd()

# Percorso della cartella "images"
images_folder = os.path.join(current_folder, "files", "images")

# Lista per tenere traccia delle informazioni delle immagini
image_info = []

# Iterazione sui file nella cartella "images"
for filename in sorted(os.listdir(images_folder)):
    file_path = os.path.join(images_folder, filename)

    # Ignora le sottocartelle e i file nascosti
    if os.path.isdir(file_path) or filename.startswith('.'):
        continue

    # Carica l'immagine
    image = Image.open(file_path)

    # Ottieni le dimensioni dell'immagine
    width, height = image.size

    # Converte l'immagine in un array NumPy
    image_array = np.array(image)

    # Verifica il numero di canali dell'immagine
    num_channels = image_array.shape[2] if len(image_array.shape) == 3 else 1

    # Calcola le medie dei valori dei canali di colore
    if num_channels == 1:
        grayscale = np.mean(image_array)
        color_values = [0, 0, 0, 0]
    else:
        grayscale = 0
        color_values = [np.mean(image_array[:, :, i]) for i in range(num_channels)]

    # Aggiungi le informazioni dell'immagine alla lista
    image_info.append([filename, height, width, grayscale] + color_values)

# Creazione della tabella riassuntiva
table_headers = ["name", "height", "width", "grayscale"] + ["R", "G", "B", "ALPHA"]
