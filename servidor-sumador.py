#!/usr/bin/python

"""
Simple HTTP Server version 2: reuses the port, so it can be
restarted right after it has been killed. Accepts connects from
the outside world, by binding to the primary interface of the host.

Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
#mySocket.bind((socket.gethostname(), 1234))
mySocket.bind(("localhost", 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

is_primer = True
primer = 0

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

try:
    while True:

        print 'Waiting for connections'
        (recvSocket, address) = mySocket.accept()
        print 'Request received:'
        request = recvSocket.recv(2048)
        print request
        number = request.split(" ",2)[1][1:]
        print "The number is: " + number

        if not number.isdigit() or number=="":

            htmlAnswer = "Not a number"
            returnCode = "404 Not Found"

        else:

            if is_primer:
                primer = int(number)
                is_primer = False
                htmlAnswer = "Dame otro numero"
                returnCode = "200 OK"
            else:
                result = int(number) + primer
                is_primer = True
                htmlAnswer = "El resultado de tu suma es: " + str(result)
                returnCode = "200 OK"

        print 'Answering back...'
        reply = "HTTP/1.1 " + returnCode + " \r\n\r\n" + htmlAnswer + "\r\n"
        recvSocket.send(reply)
        recvSocket.close()

except KeyboardInterrupt:
    print "Closing binded socket"
    mySocket.close()
