import socket
import dns.resolver
import json
import sys
import random

NS = 0
HOST = 1
REC = 2

resolver = dns.resolver.Resolver()

remote_providers = [
	('resolver1.opendns.com', 'myip.opendns.com', 'A'),
	('ns1-1.akamaitech.net', 'whoami.akamai.net', 'A'),
	('ns1.google.com', 'o-o.myaddr.l.google.com', 'TXT'),
]

random.shuffle(remote_providers)

for provider in remote_providers:
	try:
		resolver.nameservers=[socket.gethostbyname(provider[NS])]
		ip_address = resolver.resolve(provider[HOST], provider[REC])[0].to_text().replace('"', '')
		break
	except:
		pass
		
if ip_address:
	print(json.dumps({
		'public_ip': ip_address,
		'hostname': socket.gethostname()
	}))
	sys.exit(0)
else:
	sys.exit(1)
