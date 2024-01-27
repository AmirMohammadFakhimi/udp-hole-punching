from socket import *


def convert_address_to_string(address):
    return f'{address[0]}:{address[1]}'.encode()


host = ''
port = 12345
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((host, port))
print(f'STUN server running on port {port}...')

# id: (ip, port)
id_address = {}
# source_id: destination_id
pending_requests = {}

while True:
    try:
        message, address = server_socket.recvfrom(1024)
        decoded_message = message.decode()
        print(f'Received message from {address}: {decoded_message}')

        try:
            source_id, destination_id = decoded_message.split(' ', 1)
        except ValueError:
            print('Invalid message format')
            continue
        id_address[source_id] = address
        server_socket.sendto(address[0].encode(), address)

        if destination_id in pending_requests and pending_requests[destination_id] == source_id:
            print(id_address[source_id], id_address[destination_id])
            server_socket.sendto(convert_address_to_string(id_address[source_id]), id_address[destination_id])
            server_socket.sendto(convert_address_to_string(id_address[destination_id]), id_address[source_id])
            del pending_requests[destination_id]
        else:
            pending_requests[source_id] = destination_id

    except KeyboardInterrupt:
        print('\nShutting down STUN server...')
        server_socket.close()
        break
