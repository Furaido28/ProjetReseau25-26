from netaddr import IPNetwork

# Exemple de réseau
net = IPNetwork("192.168.1.10/24")

print("Adresse réseau :", net.network)
print("Broadcast     :", net.broadcast)
print("Masque        :", net.netmask)
print("Préfixe       :", net.prefixlen)
print("Nombre IPs    :", net.size)

for subnet in net.subnet(24):
    print(subnet)