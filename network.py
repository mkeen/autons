#!/usr/bin/env python3

import socket
import dns.resolver
import json
import sys
import random
import logging
import logging.handlers
import netifaces

logger = logging.getLogger('autonslog')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logger.addHandler(handler)

interface = 'em0'

def local_ip(interface_name='eth0'):
	netifaces.ifaddresses(interface_name)
	return netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0].get('addr', None)

private_ip = local_ip(interface)

if not private_ip:
	sys.exit(log(f"couldn't get private ip address on {interface}", 'critical'))

def log(message, level='info'):
	getattr(logger, level)(f"keen-autons: {message}")
	return message

def clean(input):
	return input.replace('"', '')

def text(input):
	return clean(input.to_text())

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

log('checking public ip')

ip_address = None

for provider in remote_providers:
	try:
		log(f"resolving {provider[HOST]}/{provider[REC]}")
		resolver.nameservers=[socket.gethostbyname(provider[NS])]
		ip_address = text(resolver.resolve(provider[HOST], provider[REC])[0])
		break
	except:
		log(f"couldn't resolve provider {provider} {sys.exc_info()[0]}", 'error')
		pass
		
if ip_address:
	print(json.dumps({
		'public_ip': ip_address,
		'private_ip': private_ip,
		'hostname': f"{socket.gethostname()}.knoc"
	}))
	sys.exit(0)
else:
	sys.exit(log('couldn\'t contact any providers', 'critical'))
