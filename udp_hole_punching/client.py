from socket import *
import datetime


message = input('Enter message: ')
message = f'{datetime.datetime.now()}: {message}'

host = ''
port = int(input('Enter port: '))
my_id = input('Enter your id: ')
destination_id = input('Enter destination id: ')

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((host, port))
print(f'client running on port {port}...')

stun_server_address = ('localhost', 12345)
server_socket.sendto(f'{my_id} {destination_id}'.encode(), stun_server_address)

my_public_address, _ = server_socket.recvfrom(1024)
my_public_address = my_public_address.decode()

destination_public_address, _ = server_socket.recvfrom(1024)
destination_public_address = destination_public_address.decode()
destination_public_address = destination_public_address.split(':')
destination_public_address = destination_public_address[0], int(destination_public_address[1])

print(f'{my_public_address}:{port}:{my_id} -> '
      f'{destination_public_address[0]}:{destination_public_address[1]}:{destination_id}')

while True:
    try:
        server_socket.sendto(message.encode(), destination_public_address)
        message, address = server_socket.recvfrom(1024)
        print(f'Received message from {address}: {message.decode()}')
        message = input('Enter message: ')
    except KeyboardInterrupt:
        print('\nShutting down client...')
        server_socket.close()
        break
