import subprocess
import os

# Lista de grupos
grupos = ['g02', 'g07', 'g10', 'g12', 'g17', 'g22', 'g24', 'g27', 'g42', 'g51']  # Agregá los grupos que necesites


# Base URL del repositorio
base_url = 'git@bitbucket.org:redes-famaf/redes24lab'

# Directorio base donde se van a clonar los repositorios
base_clone_dir = './repositorios'

# Crear el directorio base si no existe
if not os.path.exists(base_clone_dir):
    os.makedirs(base_clone_dir)

# Clonar los repositorios
for lab in range(1, 5):
    lab_dir = os.path.join(base_clone_dir, f'lab{lab}')
    
    # Crear el directorio para el laboratorio si no existe
    if not os.path.exists(lab_dir):
        os.makedirs(lab_dir)
    
    for grupo in grupos:
        repo_url = f'{base_url}{lab}{grupo}.git'
        clone_dir = os.path.join(lab_dir, f'{grupo}')
        
        try:
            # Ejecutar el comando de git clone
            subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)
            print(f'Repositorio {repo_url} clonado en {clone_dir}')
        except subprocess.CalledProcessError as e:
            print(f'Error al clonar el repositorio {repo_url}: {e}')

