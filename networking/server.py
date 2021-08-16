from scapy.all import *

PORT = 88088


def filter_pckt(p):
    return DLT_BLUETOOTH_LE_LL in p


def recieve_pckt(p):
    print(p.summary())


def start_listen():
    sniff(lfilter=filter_pckt, prn=recieve_pckt)


def main():
    try:
        start_listen()
    except Exception:
        print("problem occurred")

if __name__ == '__main__':
    main()
