# Custom DNS Server

It's a lightweight DNS server that intercepts requests for domains you specify and points them to an IP of your choice. Any other DNS request is automatically forwarded to a public DNS server (like Google's 8.8.8.8), so your internet works as usual.

## How It Works

Think of this script as a custom phone book for your computer's internet queries.

1.  **Custom List**: You create a list of domains you want to control in the `TARGETS` dictionary.
2.  **Check the List**: When your computer asks for a domain's IP, the script first checks if that domain is on your custom list.
3.  **Custom Reply**: If it's on the list, the script replies with the IP address you specified. For example, it tells your computer that `hacker.com` is at `127.0.0.1`.
4.  **Forward Others**: If the domain is *not* on your list, the script forwards the request to Google's DNS server and passes the answer back to you.

## Features

*   **Redirect Specific Domains**: Point any domain to your local machine or any other IP.
*   **Wildcard Support**: Redirect all subdomains of a domain (e.g., `*.google.com`).
*   **Upstream Forwarding**: Forwards all other requests, so you don't lose internet connectivity.
*   **Lightweight & Simple**: Easy to understand and modify with minimal dependencies.

## Usage Guide

Follow these simple steps to get your custom DNS server running.

### 1. Prerequisites

First, you need to install the `dnslib` library. You can do this using pip:

```bash
pip3 install dnslib
```

### 2. Configuration

Open the script and edit the TARGETS dictionary:

```python
TARGETS = {
    "nahid.com": "your_ip", # replace with your localhost ip
    "*.google.com": "your_ip", # replace with your localhost ip
    "hacker.com": "your_ip" # replace with your localhost ip
}
```
Replace your_ip with the IP address you want the domains to point to. For testing on your own machine, 127.0.0.1 is a great choice.

### 3. Run the Server

Because this server needs to run on port 53 (the standard DNS port), you need administrator/root permissions.
Open your terminal, navigate to the script's directory, and run it with sudo:

```bash
sudo python3 dns_run.py
```
You should see a message indicating the server has started:

```python
[*] Starting DNS server on 0.0.0.0:53
[*] Custom domains:
    - nahid.com -> 127.0.0.1
    - *.google.com -> 127.0.0.1
    - hacker.com -> 127.0.0.1
[*] All other requests will be forwarded to 8.8.8.8
```

### 4. Test It

Open a new terminal window and run:

```bash
# Test a custom domain
dig nahid.com @127.0.0.1

# Test a regular domain (it should be forwarded)
dig example.com @127.0.0.1
```

# Author
- **GitHub**: [@nahid0x1](https://github.com/nahid0x1)
- **Twitter**: [@nahid0x1](https://x.com/nahid0x1)
- **Linkedin**: [@nahid0x1](https://www.linkedin.com/in/nahid0x1)
- **Email**: [nahid0x1.official@gmail.com](mailto:nahid0x1.official@gmail.com)
