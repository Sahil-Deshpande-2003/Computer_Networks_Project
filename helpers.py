import socket

LOCAL_HOST = "localhost"
LOCAL_DNS_SERVER_PORT = 53
ROOT_SERVER_PORT = 9001
TLD_SERVER_PORT = 9002
AUTHORITATIVE_SERVER_PORT = 9003
BUFFER_SIZE = 65535
# Note:
# We could add the buffer size variable, one for sending and one for receiving,
# I have only used one to keep it simple. And its size is based on the max size
# of the receiving buffer.

'''
The helpers.py file contains various utility functions and constants shared among server and client scripts, such as printing messages, input validation, and socket configuration.
'''



def customPrint(name, value):
    '''
    Purpose: This function is a utility for printing messages with a specific format.
Parameters:
name: A string representing the name of the variable or information being printed.
value: The value to be printed.
Actions: Prints the provided name, value, and the type of the value.
    '''
    print()
    print(name + ":")
    print(value)
    print(type(value))
    print()


def getInputForNextServer(listOfMessages):
    '''
    Purpose: Extracts the IP address of the next server from a list of messages.
Parameters:
listOfMessages: A list of messages received from a server.
Actions:
Cleans up each message in the list by removing leading/trailing spaces and single quotes.
Reverses the list and extracts the first element as the IP address of the next server.
Returns the extracted IP address.
    '''
    cleanList = []
    for message in listOfMessages:
        message = message.strip()
        message = message.replace("'", "")
        cleanList.append(message)
    ipAddressOfTld = str
    cleanList.reverse()
    ipAddressOfTld = cleanList[0]
    return ipAddressOfTld


def displayMessages(listOfMessages):

    '''
    Purpose: Prints a list of messages, cleaning up formatting.
Parameters:
listOfMessages: A list of messages to be printed.
Actions:
Cleans up each message in the list by removing leading/trailing spaces and single quotes.
Prints each message.
    '''
    for message in listOfMessages:
        message = message.strip()
        message = message.replace("'", "")
        print(message)
    print()


def actAsTemporaryClient(message, connectingPort, nameServer):

    '''
    Purpose: Simulates a temporary client by sending a DNS query to a specified DNS server.
Parameters:
message: The DNS query message to be sent.
connectingPort: The port to connect to on the DNS server.
nameServer: The DNS server's address.
Actions:
Creates a UDP socket, encodes the DNS server address and query message, and sends them to the specified address and port.
Receives and decodes the server's response, printing the message and returning a list of messages.
    '''
    tempClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    queryMessage = message.encode()
    nameServer = nameServer.encode()
    connectingAddress = (LOCAL_HOST, connectingPort)
    tempClientSocket.sendto(nameServer, connectingAddress)
    tempClientSocket.sendto(queryMessage, connectingAddress)
    serverMessage, serverAddress = tempClientSocket.recvfrom(BUFFER_SIZE)
    serverMessage = serverMessage.decode()
    print()
    print(f"Message from {serverAddress}:")
    listOfMessages = serverMessage.strip('[]').split(',')
    tempClientSocket.close()
    return listOfMessages


def getInput(givenInput, numberOfWords):

    '''
    Purpose: Constructs a partial domain name based on the given input and the number of words.
Parameters:
givenInput: The user input (domain name).
numberOfWords: The number of words to include in the constructed domain name.
Actions:
Splits the input into words, reverses the list, and constructs a partial domain name by concatenating the specified number of words.
Returns the constructed domain name
    '''
    result = splitInput(givenInput)
    result.reverse()
    returningString = ""
    for i in range(numberOfWords):
        returningString = result[i] + "." + returningString
    return returningString


def splitInput(userInput):

    '''
    Purpose: Splits a user input (domain name) into a list of its components (subdomains).
Parameters:
userInput: The user input (domain name).
Actions:
Splits the input string using the dot ('.') as a delimiter.
Returns a list of subdomains.
    '''
    splitDomainName = userInput.split('.')
    return splitDomainName
