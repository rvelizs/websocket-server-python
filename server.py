# Implementación de websockets de servidor
# Autor: Rodrigo Véliz

import asyncio
from websockets.server import serve
from datetime import datetime

# puerto
PORT = 8000
# Lista para almacenar todas las conexiones de los clientes
clientes = []

# función que se ejecuta cuando se conecta un cliente
async def echo(websocket):
    # Añade el websocket del cliente a la lista de clientes
    clientes.append(websocket)
    client_id = clientes.index(websocket) + 1
    print(datetime.now(), f"Cliente {client_id} conectado")
    try:
        async for message in websocket:
            # Muestra por consola la hora actual y el mensaje recibido
            print(datetime.now(), f"Cliente {client_id} dice: ", message)
            # Envía el mensaje recibido a todos los clientes conectados
            for client in clientes:
                if client != websocket:  # No envía el mensaje al cliente que lo envió
                    await client.send(message)
    finally:
        # Elimina el websocket del cliente de la lista de clientes
        print(datetime.now(), f"Cliente {client_id} desconectado")
        clientes.remove(websocket)

async def main():
    print(datetime.now(), "Servidor iniciado en el puerto", PORT)
    print(datetime.now(), "Esperando conexiones...")
    async with serve(echo, "localhost", PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Servidor cerrado\n")
