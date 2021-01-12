#!/usr/bin/env python3

import socket
import dns.resolver
import json
import sys
import random
import logging
import logging.handlers

logger = logging.getLogger('autonslog')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logger.addHandler(handler)

def log(message, level='info'):
	getattr(logger, level)(f"keen autons: {message}")

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

log('checking public ip', 'info')

for provider in remote_providers:
	try:
		log(f"resolving {provider[HOST]}/{provider[REC]}", 'debug')
		resolver.nameservers=[socket.gethostbyname(provider[NS])]
		ip_address = resolver.resolve(provider[HOST], provider[REC])[0].to_text().replace('"', '')
		break
	except:
		log(f"couldn't resolve provider {provider} {sys.exc_info()[0]}", logging.WARNING)
		pass
		
if ip_address:
	print(json.dumps({
		'public_ip': ip_address,
		'hostname': f"{socket.gethostname()}.knoc"
	}))
	sys.exit(0)
else:
	log(f"couldn't contact any providers {sys.exc_info()[0]}", 'critical')
	sys.exit(1)
