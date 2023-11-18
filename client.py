from sys import *
from helpers import LOCAL_HOST, LOCAL_DNS_SERVER_PORT, BUFFER_SIZE
import re
import socket
import helpers

'''
Repeatedly takes user input (a domain name) and sends a DNS query to the local DNS server.
Handles user input validation and prints the result received from the local DNS server.
'''

'''
DNS lookups, or Domain Name System lookups, are the process of translating human-readable domain names into IP addresses that computers use to identify each other on a network. DNS is a hierarchical and distributed system that helps map easily memorizable domain names (like www.example.com) to their corresponding IP addresses.
'''

'''
DNS Query Flow:
The client initiates a DNS query by sending a request to the local DNS server.

The local DNS server, if it doesn't have the information in its cache, queries the root server for information about the TLD server.

The local DNS server then queries the TLD server for information about the authoritative DNS server for the requested domain.

Finally, the local DNS server queries the authoritative DNS server for the IP address associated with the requested domain.

At each level, the DNS server (root, TLD, authoritative) responds with the necessary information, and the local DNS server caches intermediate results
'''




def connectClientToLocalDnsServer(message):
    originalClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    '''
    A new UDP socket is created using socket.socket(socket.AF_INET, socket.SOCK_DGRAM). This sets up a socket for UDP communication.

    socket.AF_INET:

This specifies the address (or protocol) family for the socket, and it stands for Address Family - Internet.
AF_INET is used for IPv4 addresses. It indicates that the socket will be used for communication over an IPv4 network.
socket.SOCK_DGRAM:

This specifies the type of socket, and it stands for Socket Type - Datagram.
SOCK_DGRAM indicates that the socket will be used for datagram-oriented communication, which is connectionless and operates with UDP (User Datagram Protocol).
In the context of UDP, datagram sockets are appropriate because UDP is a connectionless protocol, and each packet is treated as an independent unit (datagram).
    '''
    originalClientMessage = message.encode()
    '''
    The provided DNS query message is encoded into bytes using the encode() method. This is necessary for sending the message over the network.
    '''
    connectingAddress = (LOCAL_HOST, LOCAL_DNS_SERVER_PORT)
    '''
    The connecting address is specified as a tuple containing the IP address (localhost) and the port number of the local DNS server.
    '''
    originalClientSocket.sendto(originalClientMessage, connectingAddress)
    '''
    The encoded DNS query message is sent to the local DNS server using the sendto() method. The destination address is the local DNS server's address and port.
        '''
    serverMessage, serverAddress = originalClientSocket.recvfrom(BUFFER_SIZE)
    '''
    The client waits to receive a response from the local DNS server using recvfrom(BUFFER_SIZE). The received message and the server's address are stored.
    '''
    serverMessage = serverMessage.decode()
    '''
    The received server message is decoded from bytes to a string, and both the server's address and the message are printed.
    '''
    print(f"Talking to the localDnsServer at the Address: {serverAddress}")
    print(f"Message from {serverAddress}:")
    print(f"{serverMessage}")
    result, _ = originalClientSocket.recvfrom(BUFFER_SIZE)
    '''
    This line receives a response from the server using the recvfrom method of the originalClientSocket socket. The received data is stored in the result variable, and the second variable (_) is used to discard the server address information.
    '''
    result = result.decode()

    '''
    This line decodes the received data (result) from bytes to a string. Since network communication deals with binary data, decoding is necessary to interpret the message in a human-readable form.
    '''

    print(f"Resultant IP Address received from the localDnsServer: {result}")
    '''
    The client waits for and receives the resultant IP address from the local DNS server. The received IP address is decoded and printed.
    '''
    originalClientSocket.close()
    '''
    Finally, the socket is closed using close().
    '''


def isValid(userInput):
    regex = r"([a-z]+\.[a-z]+)+"
    result = re.findall(regex, userInput)
    if len(result) > 0:
        return True
    else:
        return False


while True:
    print()
    print("Please Enter the domain name or \"break\" to exit: ")
    example = "subdomain.domain.com or domain.com"
    print(f"Example : {example}")
    try:
        userInput = input()
        userInput = userInput.lower()
        if userInput == "break":
            print("\n...Exiting Program")
            break
        result = isValid(userInput)
        if result:
            connectClientToLocalDnsServer(userInput)
        else:
            print()
            print(
                f"Please enter a domain name as shown in the example : {example}")
            print()
    except KeyboardInterrupt:
        print("\n...Exiting Program")
        exit()
