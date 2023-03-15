import subprocess
import sys

#Toma un repositorio git como comando y devuelve la lista de los commits con sus autores y el tamaño del cambio

# Definir la ruta al repositorio
repo_path = sys.argv[1]

# Ejecutar el comando para obtener una lista de todos los commits con su descripción
output = subprocess.check_output(['git', '-C', repo_path, 'log', '--pretty=format:%H,%an,%s'])

# Dividir la salida en líneas y analizar cada línea para obtener el hash del commit, el autor y la descripción
commits = {}
for line in output.decode().split('\n'):
    if line.strip() != '':
        commit_hash, author, description = line.strip().split(',', 2)
        commits[commit_hash] = {'author': author, 'lines_changed': 0, 'description': description}

# Ejecutar el comando para obtener la cantidad de líneas modificadas en cada commit
for commit_hash in commits:
    output = subprocess.check_output(['git', '-C', repo_path, 'show', '--shortstat', commit_hash])
    lines_changed = 0
    for line in output.decode().split('\n'):
        if line.startswith(' ') and line.strip().endswith(')'):
            lines_changed += int(line.strip().split(' ')[-2])
    commits[commit_hash]['lines_changed'] = lines_changed

# Imprimir los resultados
for commit_hash, commit_data in commits.items():
    print('Commit:', commit_hash)
    print('Autor:', commit_data['author'])
    print('Descripcion:', commit_data['description'])
    print('Lineas de codigo modificadas:', commit_data['lines_changed'])
    print('------')