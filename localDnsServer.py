import socket
import dns
import dns.resolver
from helpers import LOCAL_HOST, LOCAL_DNS_SERVER_PORT, BUFFER_SIZE
from helpers import ROOT_SERVER_PORT
from helpers import TLD_SERVER_PORT
from helpers import AUTHORITATIVE_SERVER_PORT
from helpers import splitInput
from helpers import actAsTemporaryClient
from helpers import displayMessages
from helpers import getInputForNextServer
from helpers import customPrint
from helpers import getInput

cache = {}


def fetchFromCache(searchKey):
    ipAddress = cache.get(searchKey)
    print(f"\"{searchKey}\" found in cache")
    print(f"IP Address of \"{searchKey}\" is \"{ipAddress}\"")
    return ipAddress


def generalServerHandler(userInput, nameServer, connectedPort, message):
    result = actAsTemporaryClient(userInput, connectedPort, nameServer)
    '''
    The actAsTemporaryClient function is called to simulate a DNS query to the specified nameServer at the given connectedPort. The result is stored in the result variable.
    '''
    print(message + ":")

    '''
    A message indicating the type of server (e.g., Root, TLD, Authoritative) is printed, and the displayMessages function is used to print the details of the DNS query result.
    '''

    displayMessages(result)
    ipAddress = getInputForNextServer(result)

    '''
    The getInputForNextServer function is called to extract the IP address for the next server from the result. This IP address is typically used in the next step of the DNS resolution process.
    '''

    '''
    In the context of the getInputForNextServer function, it is responsible for extracting the IP address of the server to which the next DNS query should be directed.
    '''

    print("Returned IP Address :", ipAddress)
    return ipAddress


def localDnsServer():
    '''
    Binds and listens on a UDP socket for the local DNS server.
Handles incoming client requests, performs root, TLD, and authoritative server lookups.
Maintains a cache to store intermediate results.
Sends the final IP address back to the client.
    '''
    localDnsServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # try:
    localDnsServerSocket.bind((LOCAL_HOST, LOCAL_DNS_SERVER_PORT))
    print(
        f"localDNS is up and running and I am listening at Port:{LOCAL_DNS_SERVER_PORT}")
    while True:
        clientMessage, clientAddress = localDnsServerSocket.recvfrom(
            BUFFER_SIZE)
        userInput = clientMessage.decode()
        print(f"Talking to the Client at the Address:{clientAddress}")
        print(f"Client Message:{userInput}")
        message = f"Hang in there client, I will get the IP Address of the \"{userInput}\""
        message = message.encode()
        '''
        
The line message = message.encode() is encoding the string variable message into bytes. In Python, strings are Unicode by default, and encoding is the process of converting a Unicode string into a sequence of bytes using a specific encoding scheme.


In network communication, data is transmitted between devices as a sequence of bytes. Textual data, such as strings, needs to be converted into a format that can be transmitted over the network, and this conversion is done through encoding

        '''
        localDnsServerSocket.sendto(message, clientAddress)
        '''     
The line localDnsServerSocket.sendto(message, clientAddress) is sending a message (in the form of bytes) from the local DNS server to the client address using a UDP (User Datagram Protocol) socket.
        '''
        defaultResolver = dns.resolver.get_default_resolver()
        '''  
The line defaultResolver = dns.resolver.get_default_resolver() is creating an instance of the default DNS resolver provided by the dnspython library. In DNS (Domain Name System), a resolver is responsible for making DNS queries and resolving domain names to their corresponding IP addresses.

dns.resolver: This is a module in the dnspython library that provides functionality for making DNS queries.

dns.resolver.get_default_resolver(): This is a function that returns the default DNS resolver configured on the system. The default resolver is typically used to handle DNS queries unless a specific resolver is specified.

defaultResolver: This variable is assigned the instance of the default DNS resolver. It can be used to make DNS queries and resolve domain names.


In the provided code, defaultResolver is a variable that holds an instance of the default DNS resolver provided by the dnspython library

        '''


        

        rootNameServer = defaultResolver.nameservers[0]

        '''

        In the context of the Domain Name System (DNS), nameservers are specialized servers on the internet that store DNS information and help in the process of translating human-readable domain names (like www.example.com) into numerical IP addresses (like 192.168.1.1).

        There are different types of nameservers, including:

        Root Nameservers: These are the highest-level nameservers in the DNS hierarchy. They provide information about the Top-Level Domain (TLD) nameservers.

        Top-Level Domain (TLD) Nameservers: These nameservers handle the next level of the hierarchy, representing domain extensions like .com, .org, .net, etc.

        Authoritative Nameservers: These are nameservers designated to store and provide authoritative information about specific domains. Each domain has its set of authoritative nameservers.

        Recursive Nameservers: These nameservers perform the task of resolving queries on behalf of clients by recursively querying other nameservers in the DNS hierarchy until the final IP address is obtained.


        defaultResolver: This variable holds an instance of the default DNS resolver provided by the dnspython library. A DNS resolver is responsible for making DNS queries to resolve domain names to their corresponding IP addresses.

        defaultResolver.nameservers: This attribute of the resolver contains a list of IP addresses representing the nameservers that the resolver is configured to use. Nameservers are servers that hold DNS information, and the resolver queries them to obtain the necessary information.

        [0]: The [0] indexing is used to access the first item in the list of nameservers. In DNS resolution, the root DNS server is typically the initial point of contact in the hierarchy.

        rootNameServer: This variable is assigned the IP address of the root DNS server. The root DNS server is a crucial part of the DNS infrastructure, and it provides information about the Top-Level Domain (TLD) servers.
        '''


        splitResult = splitInput(userInput)

        '''
        Original User Input: subdomain.example.com
        Split Subdomains: ['subdomain', 'example', 'com']
        '''


        splitResult.reverse()
        rootInput, tldInput, *_ = splitResult
        tldInput = tldInput + "." + rootInput

        '''
        rootInput: com
        tldInput: example.subdomain
        _ (ignored): []
        '''

        authoritativeInput = getInput(userInput, len(splitResult))
        authoritativeInput = authoritativeInput[:-1]
        '''
        The user input "subdomain.example.com" is split into subdomains, resulting in splitResult as ['subdomain', 'example', 'com'].

        The getInput function generates the authoritativeInput by concatenating the subdomains in reverse order with dots between them. The resulting string is 'com.example.subdomain'.

        The last character ('n') is then removed from authoritativeInput using slicing ([:-1]), resulting in the final authoritativeInput string: 'com.example.subdomain'
        '''
        customPrint("rootInput", rootInput)
        customPrint("tldInput", tldInput)
        customPrint("_", _) # _ (ignored): []
        customPrint("authoritativeInput", authoritativeInput)
        if bool(cache) and rootInput in cache:

            # pass the root input which is com in this case as key and returns IP address 

            tldNameServer = fetchFromCache(rootInput)
        else:



            '''
            Let’s take a look at a simple example. Suppose the host cse.nyu.edu desires 
the IP address of gaia.cs.umass.edu. Also suppose that NYU’s local DNS 
server for cse.nyu.edu is called dns.nyu.edu and that an authoritative DNS 
server for gaia.cs.umass.edu is called dns.umass.edu. As shown in 
Figure 2.19, the host cse.nyu.edu first sends a DNS query message to its local 
DNS server, dns.nyu.edu. The query message contains the hostname to be transalated, namely, gaia.cs.umass.edu. The local DNS server forwards the query 
message to a root DNS server. The root DNS server takes note of the edu suffix and 
returns to the local DNS server a list of IP addresses for TLD servers responsible 
for edu. The local DNS server then resends the query message to one of these TLD 
servers. The TLD server takes note of the umass.edu suffix and responds with 
the IP address of the authoritative DNS server for the University of Massachusetts, 
namely, dns.umass.edu. Finally, the local DNS server resends the query messsage directly to dns.umass.edu, which responds with the IP address of gaia 
.cs.umass.edu
            '''



            rootMessage = "Root Result"
            tldNameServer = generalServerHandler(
                userInput, rootNameServer, ROOT_SERVER_PORT, rootMessage) # PERFORM A DNS QUERY TO ROOT SERVER
            '''
            If the root input is not found in the cache, the generalServerHandler function is called to perform a DNS query to the root server. The result (tldNameServer) is then stored in the cache

            generalServerHandler calls  actAsTemporaryClient which sends the DNS query to the root server
            '''
        cache[rootInput] = tldNameServer
        tldMessage = "TLD Result"
        authoritativeServer = generalServerHandler( # PERFORM A DNS QUERY TO TLD SERVER
            userInput, tldNameServer, TLD_SERVER_PORT, tldMessage)
        
        '''
        The generalServerHandler function is called to perform the DNS resolution process for the TLD server. It simulates a DNS query to the TLD server, retrieves the result, and returns the IP address of the authoritative DNS server for the specific domain. The obtained IP address is stored in the authoritativeServer variable.
        '''

        cache[tldInput] = authoritativeServer
        authoritativeMessage = "Authoritative Result"
        finalIpAddress = generalServerHandler( # PERFORM A DNS QUERY TO AUTHORITATIVE SERVER
            userInput, authoritativeServer, AUTHORITATIVE_SERVER_PORT, authoritativeMessage)
        
        '''
        The generalServerHandler function is called again, this time to perform the DNS resolution process for the authoritative DNS server. It simulates a DNS query to the authoritative server, retrieves the result, and returns the final IP address associated with the user's input. The obtained IP address is stored in the finalIpAddress variable.
        '''


        cache[authoritativeInput] = finalIpAddress
        customPrint("cache", cache)
        print()
        print(f"Final IP Address : {finalIpAddress}")
        print()
        serverMessage = finalIpAddress.encode()
        localDnsServerSocket.sendto(serverMessage, clientAddress) # is responsible for sending the final IP address obtained from the authoritative DNS server back to the client.

        '''
        localDnsServerSocket: This is a UDP socket created by the local DNS server to handle incoming DNS queries and send responses.

        sendto(serverMessage, clientAddress): This method sends the serverMessage (which contains the final IP address) to the address specified by clientAddress. In the context of DNS, this is the client's address to which the DNS response is directed.
        '''

    # except KeyboardInterrupt:
    #     print("\nStopping the server")
    #     print("........")
    #     print("........")
    #     print("You Stopped the server")
    #     exit()
    # except:
    #     print("Something went wrong")
    #     exit()


localDnsServer()
