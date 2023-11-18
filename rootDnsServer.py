import socket
import dns
import dns.resolver
import dns.query
import dns.name
import dns.message
import warnings
from helpers import LOCAL_HOST, ROOT_SERVER_PORT, BUFFER_SIZE
from helpers import splitInput
from helpers import getInput
from helpers import customPrint
from helpers import displayMessages


def findOutTld(userInput, localNameServer):
    '''
    Takes user input and the local DNS server as arguments.
Performs a DNS query to the local DNS server for the TLD (Top-Level Domain) information.
Returns messages about the lookup process.
    '''

    '''
    The function findOutTld performs the DNS resolution process to find information about the Top-Level Domain (TLD) associated with a given user input. Here's a step-by-step explanation of the function:

    Initialization:

    returnMessage: A list to store messages about the DNS lookup process.
    defaultResolver: Retrieves the default DNS resolver.
    converToDomainName: Converts the user input into a DNS name.
    numberOfWords: Set to 1, indicating that only the root domain is considered initially.
    rootInput: Obtains the root domain from the user input using the getInput function.
    message: A message indicating that the function is aware of the root domain.
    DNS Query to Local DNS Server:

    Appends a message indicating the lookup of the root domain on the local DNS server.
    Creates a DNS query for the root domain (rootInput) with the query type NS (Name Server).
    Sends the query to the local DNS server using UDP and receives the response.
    Handling DNS Response:

    Checks the response code (rcode). If it's not NOERROR, handles specific cases:
    If the response code is NXDOMAIN (domain not found), appends an error message.
    If there's another error, appends a general error message.
    If the response is successful:
    Determines whether the authoritative information is in the authority section or the answer section.
    Retrieves the resource record (RR) from the appropriate section.
    Checks if the RR type is Start of Authority (SOA). If so, the same server is considered the TLD server.
    If it's not SOA, extracts the TLD server name and appends related messages.
    Retrieves the IP address of the TLD server using the default DNS resolver.
    Appends messages about the TLD server name and its IP address.
    Return:

    Returns the list of messages (returnMessage), providing insights into the DNS lookup process for the TLD.
    '''


    returnMessage = []
    defaultResolver = dns.resolver.get_default_resolver()
    converToDomainName = dns.name.from_text(userInput)
    numberOfWords = 1
    rootInput = getInput(userInput, numberOfWords)
    customPrint("Customized rootInput", rootInput)
    message = f"I dont know the address of \"{userInput}\" but I know the address of \"{rootInput}\""
    returnMessage.append(message)
    returnMessage.append(
        f"Looking up \"{rootInput}\" on \"{localNameServer}\"")
    query = dns.message.make_query(rootInput, dns.rdatatype.NS)
    response = dns.query.udp(query, localNameServer)
    responseCode = response.rcode()
    if responseCode != dns.rcode.NOERROR:
        if responseCode == dns.rcode.NXDOMAIN:
            returnMessage.append(f"\"{rootInput}\" does not exist.")
            returnMessage.append("Please enter a legible domain")
            return returnMessage
        else:
            returnMessage.append("Please enter a legible domain.")
            return returnMessage
    '''
    Initialize Variables:

resourceRecordSet: Initially set to None.
Check if there is information in the authority section (response.authority). If yes, assign the first resource record set from the authority section. If not, use the first resource record set from the answer section (response.answer).
Extract the first resource record (resourceRecord) from the chosen resource record set.
Check Resource Record Type:

Check if the resource record type (resourceRecord.rdtype) is Start of Authority (SOA).
If it is SOA, it means that the same server is considered the TLD server for the root domain (rootInput). Append a message indicating this.
Extract TLD Server Information:

If the resource record type is not SOA, it means there is a different TLD server.
Extract the target name of the resource record (tldServerName), which represents the TLD server.
Append messages indicating the TLD server for the root domain.
Retrieve TLD Server IP Address:

Use the default DNS resolver to query for the IP address of the TLD server (tldServerName).
Suppress deprecation warnings to avoid clutter in the output.
Extract the IP address from the response and append messages indicating the IP address of the TLD server.
Return Messages:

Return the list of messages (returnMessage) containing information about the TLD server, its name, and IP address.
    '''
    resourceRecordSet = None


    '''
    
In DNS (Domain Name System) responses, the authority and answer sections are two of the sections that can be present. These sections contain resource records with information about the domain being queried. Let's understand what each section represents:

Authority Section (response.authority):

The authority section of a DNS response contains information about authoritative DNS servers for the queried domain.
It provides information about which DNS servers are considered authoritative for the domain.
This section is particularly relevant when a DNS server needs to delegate authority for a subdomain to another DNS server.
Answer Section (response.answer):

The answer section of a DNS response contains the actual resource records that answer the DNS query.
These records include information such as IP addresses associated with the queried domain or other relevant data depending on the query type (A, AAAA, MX, etc.).
This section provides the data that the DNS client requested.
In the code snippet you provided earlier, the logic checks both the authority and answer sections to determine which section contains the relevant information. If the authority section is non-empty, it selects the first resource record set from the authority section. If the authority section is empty, it uses the first resource record set from the answer section.
    '''

    if len(response.authority) > 0:
        resourceRecordSet = response.authority[0]
    else:
        resourceRecordSet = response.answer[0]
    resourceRecord = resourceRecordSet[0]
    if resourceRecord.rdtype == dns.rdatatype.SOA:
        returnMessage.append(
            f"Same server is TLD Server for \"{rootInput}\"")
    else:
        tldServerName = resourceRecord.target
        returnMessage.append(
            f"\"{tldServerName}\" is TLD Server for \"{rootInput}\"")
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        ipAddressofTld = defaultResolver.query(
            tldServerName).rrset[0].to_text()
        returnMessage.append(
            f"IP Address of \"{tldServerName}\" is \"{ipAddressofTld}\"")
        returnMessage.append(str(tldServerName))
        returnMessage.append(ipAddressofTld)
    return returnMessage


def rootDnsServer():
    '''
    Sets up a UDP socket for the root DNS server.
Listens for incoming requests from local DNS servers.
Calls findOutTld to perform TLD lookups.
Sends the result back to the local DNS server.
    '''
    rootDnsServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # This line creates a UDP (User Datagram Protocol) socket for communication. AF_INET specifies the address family (IPv4), and SOCK_DGRAM specifies the socket type (UDP).
    try:
        '''
        The try block attempts to bind the socket to the root DNS server's address (LOCAL_HOST) and port (ROOT_SERVER_PORT). If successful, it prints a message indicating that the server is running.
        '''
        rootDnsServerSocket.bind((LOCAL_HOST, ROOT_SERVER_PORT))
        print(f"Root Server is up and running at port:{ROOT_SERVER_PORT}")
        while True:
            localNameServer, _ = rootDnsServerSocket.recvfrom(BUFFER_SIZE)
            localNameServer = localNameServer.decode()
            clientMessage, clientAddress = rootDnsServerSocket.recvfrom(
                BUFFER_SIZE)
            userInput = clientMessage.decode()
            # Receives the DNS query message and address from the client and decodes the message.
            print(f"Talking to Client at Address:{clientAddress}")
            print(f"Client Message:{userInput}")
            result = findOutTld(userInput, localNameServer)
            # Calls the findOutTld function to perform Top-Level Domain (TLD) lookups based on the user's input and the local DNS server's address.
            displayMessages(result)
            # Prints the messages obtained from the TLD lookup process.
            serverMessage = str(result).encode()
            # Encodes the result as a string, sends it back to the client using the UDP socket, and repeats the loop for the next request.
            rootDnsServerSocket.sendto(serverMessage, clientAddress)
    except KeyboardInterrupt:
        print("\nStopping the server")
        print("........")
        print("........")
        print("You Stopped the server")
        exit()
    except:
        print("Something went wrong")
        exit()


rootDnsServer()
