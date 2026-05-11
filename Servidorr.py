# -*- coding: latin-1 -*-
import socket
import threading

clientes = []

def manejar_cliente(cliente_socket, direccion):
    """Hilo para recibir mensajes de cada cliente."""
    clientes.append(cliente_socket)
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if not mensaje:
                break
            
            # El servidor muestra lo que recibió
            print(f"\n[CLIENTE {direccion}] dice: {mensaje}")
            
            # Reenvía a los demás clientes
            for c in clientes:
                if c != cliente_socket: # Opcional: no enviárselo al mismo que lo mandó
                    c.send(f"Mensaje de otro cliente: {mensaje}".encode('utf-8'))
        except:
            break
            
    clientes.remove(cliente_socket)
    cliente_socket.close()

def entrada_servidor():
    """Hilo para que el administrador del servidor pueda escribir mensajes."""
    while True:
        mensaje_admin = input("Servidor (Escribe un mensaje para todos): \n")
        # El servidor envía su mensaje a TODOS los clientes conectados
        for c in clientes:
            try:
                c.send(f"AVISO DEL SERVIDOR: {mensaje_admin}".encode('utf-8'))
            except:
                continue

def iniciar_servidor():
    host = 'localhost'
    puerto = 12345
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()
    
    print(f"Servidor iniciado. Puerto: {puerto}")
    
    # LANZAMOS EL HILO DE ESCRITURA DEL SERVIDOR
    # Esto permite que el servidor pida 'input()' sin detener la espera de clientes
    hilo_admin = threading.Thread(target=entrada_servidor, daemon=True)
    hilo_admin.start()

    while True:
        cliente_socket, direccion = servidor.accept()
        print(f"\n[SISTEMA] Conectado con {direccion}")
        hilo = threading.Thread(target=manejar_cliente, args=(cliente_socket, direccion))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
