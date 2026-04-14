# -*- coding: latin-1 -*-
import socket
import threading

def recibir_mensajes(cliente_socket):
    """Este hilo solo se encarga de escuchar lo que llega del servidor e imprimirlo."""
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(mensaje)
        except:
            print("Desconectado del servidor.")
            cliente_socket.close()
            break

def iniciar_cliente():
    host = 'localhost'
    puerto = 12345
    
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente_socket.connect((host, puerto))
        print("Conectado al chat. ¡Ya puedes escribir!")
        
        # Iniciamos un hilo en el fondo para RECIBIR mensajes simultáneamente
        hilo_lectura = threading.Thread(target=recibir_mensajes, args=(cliente_socket,))
        hilo_lectura.start()
        
        # El hilo principal se encarga de ENVIAR mensajes (leer tu teclado)
        while True:
            mensaje = input()
            cliente_socket.send(mensaje.encode('utf-8'))
            
    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")

if __name__ == "__main__":
    iniciar_cliente()
