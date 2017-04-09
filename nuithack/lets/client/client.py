import socket
import letsenchiffre_pb2 as letsenchiffre
from time import sleep

def forge_request():
    crtreq = letsenchiffre.CertificateRequest()
    crtreq.Locality = 'FR'
    crtreq.State = 'IDF'
    crtreq.City = 'Paris'
    crtreq.Company = 'Sysdream'
    crtreq.CommonName = 'www.sysdream.com'
    crtreq.CertificatePassword = 'changeme'
    return crtreq.SerializeToString()

def decode_certificate(certdata):
    crtreq = letsenchiffre.CertificateResponse()
    crtreq.ParseFromString(certdata)
    print("Certificate Password : \n\n%s\n" % crtreq.CertificatePassword)
    print("Certificate : \n\n%s" % crtreq.Certificate)
    print("PrivateKey : \n\n%s" % crtreq.PrivateKey)
    print("Thanks for using LetsEnchiffre!")

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9999))
    sock.send(forge_request())
    data = sock.recv(2048)
    decode_certificate(data)
    sleep(0.05)
    sock.close()
