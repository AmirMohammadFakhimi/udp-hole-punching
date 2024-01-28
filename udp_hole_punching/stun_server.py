from socket import *


def convert_address_to_string(address):
    return f'{address[0]}:{address[1]}'.encode()


# running server on port 12345
host = ''
port = 12345
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((host, port))
print(f'STUN server running on port {port}...')

# id: (ip, port)
id_address = {}
# source_id: destination_id
pending_requests = {}

# running server
while True:
    try:
        # receiving a message from client
        message, address = server_socket.recvfrom(1024)
        decoded_message = message.decode()
        print(f'Received message from {address}: {decoded_message}')

        # each client just sends one message to the server
        # the message is in the format of 'source_id destination_id'
        # 'source_id' is the id of the client that sent the message
        # 'destination_id' is the id of the client that the source client wants to communicate with
        try:
            source_id, destination_id = decoded_message.split(' ', 1)
        except ValueError:
            print('Invalid message format')
            continue

        # saving the address of the client that sent the message
        id_address[source_id] = address
        # sending the public address of the client that sent the message to the server
        server_socket.sendto(address[0].encode(), address)

        if destination_id in pending_requests and pending_requests[destination_id] == source_id:
            # if the destination client already sent a message to the server
            # and the source client is the one that the destination client wants to communicate with
            # then send the public addresses of the two clients to each other
            print(id_address[source_id], id_address[destination_id])
            server_socket.sendto(convert_address_to_string(id_address[source_id]), id_address[destination_id])
            server_socket.sendto(convert_address_to_string(id_address[destination_id]), id_address[source_id])
            del pending_requests[destination_id]
        else:
            # if the destination client didn't send a message to the server
            # or the source client is not the one that the destination client wants to communicate with
            # then save the request in the pending requests dictionary
            pending_requests[source_id] = destination_id

    except KeyboardInterrupt:
        print('\nShutting down STUN server...')
        server_socket.close()
        break
