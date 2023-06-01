import os
import time
import subprocess
import csv

# Número de repositorios
grupos = ["02", "07", "12", "22", "32"]
anno = 23

# Directorio de destino para clonar los repositorios
dest_dir = "repos"

# Ruta del archivo CSV
csv_file = "results.csv"

# Abrir el archivo CSV en modo de escritura
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Grupo", "Resultado server-test", "Resultado connection.py", "Resultado server.py",
                     "Resultado pylint connection.py", "Resultado pylint server.py"])

    # Clonar los repositorios
    for g in grupos:
        repo_url = f"git@bitbucket.org:redes-famaf/redes{anno}lab2g{g}.git"
        repo_dir = os.path.join(dest_dir, f"redes{anno}lab2g{g}")
        os.makedirs(repo_dir, exist_ok=True)
        os.system(f"git clone {repo_url} {repo_dir}")

        # Ejecutar server.py
        server_py = os.path.join(repo_dir, "server.py")
        server_process = subprocess.Popen(["python", server_py])

        # Esperar unos segundos para que el servidor se inicie correctamente
        time.sleep(3)

        # Ejecutar server-test.py y capturar la última línea impresa en stderr
        server_test_py = os.path.join(repo_dir, "server-test.py")
        server_test_process = subprocess.Popen(["python", server_test_py], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stderr_lines = server_test_process.stderr.readlines()
        last_stderr_line = stderr_lines[-1].decode().strip()

        # Cerrar server.py
        server_process.terminate()

        # Ejecutar radon cc connection.py -s -a y capturar la última línea de stdout
        connection_py = os.path.join(repo_dir, "connection.py")
        connection_result = subprocess.run(["radon", "cc", connection_py, "-s", "-a"], capture_output=True, text=True)
        connection_stdout = connection_result.stdout.strip().split("\n")[-1]

        # Ejecutar radon cc server.py -s -a y capturar la última línea de stdout
        server_result = subprocess.run(["radon", "cc", server_py, "-s", "-a"], capture_output=True, text=True)
        server_stdout = server_result.stdout.strip().split("\n")[-1]

        # Ejecutar pylint connection.py y capturar la última línea de stdout
        pylint_connection_result = subprocess.run(["pylint", connection_py], capture_output=True, text=True)
        pylint_connection_stdout = pylint_connection_result.stdout.strip().split("\n")[-1]

        # Ejecutar pylint server.py y capturar la última línea de stdout
        pylint_server_result = subprocess.run(["pylint", server_py], capture_output=True, text=True)
        pylint_server_stdout = pylint_server_result.stdout.strip().split("\n")[-1]

        # Guardar el número de grupo, las últimas líneas de stderr y stdout en el archivo CSV
        writer.writerow([g, last_stderr_line, connection_stdout, server_stdout,
                         pylint_connection_stdout, pylint_server_stdout])

        print(f"Resultado de los tests para el grupo {g}: {last_stderr_line}")
        print(f"Resultado de radon cc connection.py: {connection_stdout}")
        print(f"Resultado de radon cc server.py: {server_stdout}")
        print(f"Resultado de pylint connection.py: {pylint_connection_stdout}")
        print(f"Resultado de pylint server.py: {pylint_server_stdout}")
        
        time.sleep(60)