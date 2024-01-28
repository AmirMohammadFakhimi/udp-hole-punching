# udp-hole-punching
It was our homework at Computer Networks course in fall 2023 at Sharif University of Technology.

**Server:** Just run it, it will listen on port 12345. It shows a message when a client sends a packet to it. And when a
connection is established between two clients, it shows their IP addresses and ports.  
The clients' first packet to the server should be in the format of `itsID DestinationID` where `itsID` is the ID of the
client who sends the packet and `DestinationID` is the ID of the client who the first client wants to connect to. The IDs
are arbitrary but should be unique and without any space.

**Client:** It gives some arguments, respectively:  
- Message: The message that the client wants to send to the other client.
- Port: The port that the client wants to listen to.
- Its ID: The ID of the client who sends the packet.
- Destination ID: The ID of the client who the first client wants to connect to.

After running the client, it will send a packet to the server and server sends the client's public IP address.
Then it waits for the server to send the other client's IP address and port. Then the direct connection will be
established between the two clients.
