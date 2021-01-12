import socket
import dns.resolver
import json
import sys
import random
import logging
import logging.handlers

logger = logging.getLogger('autonslog')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)

DEBUG = 'debug'
ERROR = 'error'
FATAL = 'fatal'
NOTICE = 'notice'

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

def log(message, level=DEBUG):
	prefix = 'keen autons:'
	message = f"{prefix} {message}"
	logfn = getattr(logger, level)
	logfn(message)

log('checking public ip', NOTICE)

for provider in remote_providers:
	try:
		log(f"resolving {provider[HOST]}/{provider[REC]}")
		resolver.nameservers=[socket.gethostbyname(provider[NS])]
		ip_address = resolver.resolve(provider[HOST], provider[REC])[0].to_text().replace('"', '')
		break
	except:
		log(f"couldn't resolve provider {provider} {sys.exc_info()[0]}", ERROR)
		pass
		
if ip_address:
	print(json.dumps({
		'public_ip': ip_address,
		'hostname': f"{socket.gethostname()}.knoc"
	}))
	sys.exit(0)
else:
	log(f"couldn't contact any providers {sys.exc_info()[0]}", FATAL)
	sys.exit(1)
