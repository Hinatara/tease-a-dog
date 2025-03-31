import pycurl
import threading
from io import BytesIO
import socks
import socket
import time

# Function to set up Tor proxy
def setup_tor_proxy(curl):
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket
    curl.setopt(pycurl.PROXY, "localhost")
    curl.setopt(pycurl.PROXYPORT, 9050)
    curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)

# Function to perform the request and check IP
def perform_request(url, delay):
    curl = pycurl.Curl()
    setup_tor_proxy(curl)
    buffer = BytesIO()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, buffer)
    
    try:
        curl.perform()
        body = buffer.getvalue().decode('utf-8')
        print(f"Request to {url} completed. Response length: {len(body)}")
    except pycurl.error as e:
        print(f"Error occurred: {e}")
    finally:
        curl.close()
    
    time.sleep(delay)

# Function to check Tor IP
def check_tor_ip():
    curl = pycurl.Curl()
    setup_tor_proxy(curl)
    buffer = BytesIO()
    curl.setopt(pycurl.URL, "http://check.torproject.org")
    curl.setopt(pycurl.WRITEDATA, buffer)
    
    try:
        curl.perform()
        body = buffer.getvalue().decode('utf-8')
        if "Congratulations. This browser is configured to use Tor." in body:
            print("Tor is configured correctly.")
        else:
            print("Tor is not configured correctly.")
    except pycurl.error as e:
        print(f"Error occurred: {e}")
    finally:
        curl.close()

# Function to start multiple threads
def start_threads(url, num_threads, delay):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=perform_request, args=(url, delay))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    url = input("Enter the target URL: ")
    num_threads = int(input("Enter the number of threads: "))
    delay = float(input("Enter the delay between requests (in seconds): "))
    
    check_tor_ip()
    start_threads(url, num_threads, delay)