import socket
import struct
import time
#this magic packet and request was written by ai cause i'm too dumb for this o_o
MAGIC = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"

def ping_rust(ip, port, timeout=3.0):
    timestamp = struct.pack(">Q", int(time.time() * 1000))
    guid = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    packet = b"\x01" + timestamp + MAGIC + guid

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    try:
        start = time.time()
        sock.sendto(packet, (ip, port))
        data, _ = sock.recvfrom(2048)
        ms = round((time.time() - start) * 1000)
        return True, ms
    except Exception:
        return False, 0
    finally:
        sock.close()

def get_us_delay():
    return ping_rust("103.67.202.165", 28015)
def get_eu_delay():
    return ping_rust("131.153.158.236", 28015)
def get_au_delay():
    return ping_rust("51.161.205.193", 28015)
