import socket
import dns
import dns.resolver
import dns.query
import dns.message
import dns.message
import warnings
from helpers import LOCAL_HOST, TLD_SERVER_PORT, BUFFER_SIZE
from helpers import splitInput
from helpers import getInput
from helpers import customPrint
from helpers import displayMessages


def findOutAuthoritative(userInput, nameServer):
    '''
    Takes user input and the TLD DNS server as arguments.
Performs a DNS query to the TLD DNS server for the authoritative server information.
Returns messages about the lookup process.
    '''
    returnMessage = []
    defaultResolver = dns.resolver.get_default_resolver()
    converToDomainName = dns.name.from_text(userInput)
    numberOfWords = 2
    tldInput = getInput(userInput, numberOfWords)
    customPrint("Customized tldInput", tldInput)
    if len(splitInput(userInput)) > 2:
        message = f"I dont know the address \"{userInput}\" but I know the address of \"{tldInput}\""
        returnMessage.append(message)
    returnMessage.append(f"Looking up \"{tldInput}\" on \"{nameServer}\"")
    query = dns.message.make_query(tldInput, dns.rdatatype.NS)
    response = dns.query.udp(query, nameServer)
    responseCode = response.rcode()
    if responseCode != dns.rcode.NOERROR:
        if responseCode == dns.rcode.NXDOMAIN:
            returnMessage.append(f"\"{tldInput}\" does not exist.")
            returnMessage.append("Please enter a legible domain")
            return returnMessage
        else:
            returnMessage.append("Please enter a legible domain.")
            return returnMessage
    resourceRecordSet = None
    if len(response.authority) > 0:
        resourceRecordSet = response.authority[0]
    else:
        resourceRecordSet = response.answer[0]
    resourceRecord = resourceRecordSet[0]
    if resourceRecord.rdtype == dns.rdatatype.SOA:
        returnMessage.append(
            f"Same server is authoritative for \"{tldInput}\"")
    else:
        authoritativeServerName = resourceRecord.target
        returnMessage.append(
            f"\"{authoritativeServerName}\" is authoritative for \"{tldInput}\"")
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        ipAddressofAuthoritative = defaultResolver.query(
            authoritativeServerName).rrset[0].to_text()
        returnMessage.append(
            f"Ip Address of \"{authoritativeServerName}\" is \"{ipAddressofAuthoritative}\"")
        returnMessage.append(str(authoritativeServerName))
        returnMessage.append(ipAddressofAuthoritative)
    return returnMessage


def tldDnsServer():
    '''
    Sets up a UDP socket for the TLD DNS server.
Listens for incoming requests from root DNS servers.
Calls findOutAuthoritative to perform authoritative server lookups.
Sends the result back to the root DNS server.
    '''
    tldDnsServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        tldDnsServerSocket.bind((LOCAL_HOST, TLD_SERVER_PORT))
        print(
            f"TLD Server is up and running at port:{TLD_SERVER_PORT}")
        while True:
            nameServer, _ = tldDnsServerSocket.recvfrom(BUFFER_SIZE)
            nameServer = nameServer.decode()
            clientMessage, clientAddress = tldDnsServerSocket.recvfrom(
                BUFFER_SIZE)
            userInput = clientMessage.decode()
            print(f"Talking to Client at Address:{clientAddress}")
            print(f"Client Message:{userInput}")
            result = findOutAuthoritative(userInput, nameServer)
            displayMessages(result)
            serverMessage = str(result).encode()
            tldDnsServerSocket.sendto(serverMessage, clientAddress)
    except KeyboardInterrupt:
        print("\nStopping the server")
        print("........")
        print("........")
        print("You Stopped the server")
        exit()
    except:
        print("Enter Eligible Domain Name")
        exit()


tldDnsServer()
