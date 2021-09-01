# Multi-Thread-Client-Server
b.py is the server
c.py is the client

Client asks for Username to initiate the thread (use unique)

In the Server:-

class memory -> is the shared memory for one match or two people

boards[]-> is an array of type 'memory'

initially all memory objects are set to unallocated

users is the shared dictionary maintained to handle:-

1. Communicating that an opponent is found.
2. Communicating that a memory is found.
