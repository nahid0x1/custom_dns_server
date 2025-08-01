from dnslib import *
from dnslib.server import DNSServer, BaseResolver, DNSLogger
import socket

TARGETS = {
    "nahid.com": "127.0.0.1", #replace with your localhost ip
    "google.com": "127.0.0.1", #replace with your localhost ip
    "hacker.com": "127.0.0.1" #replace with your localhost ip
}

WILDCARD_DOMAINS = {
    "google.com": "127.0.0.1" #replace with your localhost ip
}

UPSTREAM_DNS = ("8.8.8.8", 53)

class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname).strip('.')
        qtype = QTYPE[request.q.qtype]

        reply = request.reply()

        # Direct match
        if qtype == 'A' and qname in TARGETS:
            target_ip = TARGETS[qname]
            print(f"[*] Custom response for '{qname}' -> {target_ip}")
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(target_ip), ttl=300))
            return reply
        
        # Wildcard match
        for domain, ip in WILDCARD_DOMAINS.items():
            if qname.endswith("." + domain):
                print(f"[*] Wildcard response for '{qname}' -> {ip}")
                reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip), ttl=300))
                return reply

        # Fallback to upstream
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_sock.settimeout(3.0)
            proxy_sock.sendto(request.pack(), UPSTREAM_DNS)
            data, _ = proxy_sock.recvfrom(512)
            proxy_sock.close()
            return DNSRecord.parse(data)
        except Exception as e:
            print(f"[!] Failed to forward request for '{qname}': {e}")
            reply.header.rcode = RCODE.SERVFAIL
            return reply

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 53
    print(f"[*] Starting DNS server on {HOST}:{PORT}")
    print("[*] Custom domains:")
    for domain, ip in TARGETS.items():
        print(f"    - {domain} -> {ip}")
    for domain, ip in WILDCARD_DOMAINS.items():
        print(f"    - *.{domain} -> {ip}")
    print("[*] All other requests will be forwarded to 8.8.8.8")

    logger = DNSLogger(prefix=False)

    try:
        server = DNSServer(CustomResolver(), port=PORT, address=HOST, logger=logger)
        server.start()
    except PermissionError:
        print("[!] Permission denied. Use 'sudo'")
    except KeyboardInterrupt:
        print("[*] Stopping DNS server.")
    except Exception as e:
        print(f"[!] Error: {e}")
