import psutil

def close_processes_by_port(port):
    for proc in psutil.process_iter():
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.status == 'LISTEN' and conn.laddr.port == port:
                    print(f"Closing process {proc.pid} - {proc.name()} on port {port}")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Definir el número de puerto que deseas cerrar
port_to_close = 19500

# Cerrar procesos en el puerto especificado
close_processes_by_port(port_to_close)