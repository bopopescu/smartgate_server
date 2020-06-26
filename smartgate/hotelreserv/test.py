import socket
import struct

def udp_connection(data):

    port = 11111
    ipaddr = find_my_ip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind( (ipaddr, port))

    print('start server')
    print("server ip: {:s} | port: {:d}".format( ipaddr, port))
    print('operation complete')

    sock.sendto(data, (ipaddr, port))

    sock.close()

def find_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',0)) # google dns 연결 해서 아이피 찾기
    ip = s.getsockname()[0]
    print(ip)
    return ip