from socket import *
import datetime

# an arbitrary message
message = input('Enter message: ')
message = f'{datetime.datetime.now()}: {message}'

# getting a port and id from the user and also the destination id
host = ''
port = int(input('Enter port: '))
my_id = input('Enter your id: ')
destination_id = input('Enter destination id: ')

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((host, port))
print(f'client running on port {port}...')

# sending a message to the server in the format of 'my_id destination_id'
stun_server_address = ('141.11.45.90', 12345)
server_socket.sendto(f'{my_id} {destination_id}'.encode(), stun_server_address)

# receiving the public address (IP) of the client from the server
my_public_address, _ = server_socket.recvfrom(1024)
my_public_address = my_public_address.decode()
print(f'My public address: {my_public_address}')

# receiving the public address (IP and port) of the destination client from the server
destination_public_address, _ = server_socket.recvfrom(1024)
destination_public_address = destination_public_address.decode()
destination_public_address = destination_public_address.split(':')
destination_public_address = destination_public_address[0], int(destination_public_address[1])
print(f'Destination public address: {destination_public_address}')

print(f'{my_public_address}:{port}:{my_id} -> '
      f'{destination_public_address[0]}:{destination_public_address[1]}:{destination_id}')

# sending the message to the destination client
# After that the connection will be open and the two clients can communicate with each other
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
