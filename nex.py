                                                                                                                                                                                                                                                                                                                                                                                                                                                                        nex.py *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
import nmap
import requests
import os
import threading
import itertools
import time
import subprocess
def banner():
    print(r"""
 _   _ ______ __   __                      NEX v2.0
| \ | |  ____|\ \ / /          enum toolkit (port scan + directory busting)
|  \| | |__    \ V /           github.com/Xmyronn
| . ` |  __|    > <            
| |\  | |____  / . \           
|_| \_|______|/_/ \_\          
      N  E  X """)

#def spinner(message):
 #   done = False

  #  def animate():
   #     for c in itertools.cycle(['|', '/', '-', '\\']):
    #        if done:
     #           break
      #      print(f'\r{message} {c}', end='', flush=True)
       #     time.sleep(0.1)
       # print('\r' + ' ' * (len(message) + 2) + '\r', end='')

#    t = threading.Thread(target=animate)
 #   t.start()
  #  return lambda: setattr(threading.current_thread(), "done", True), 

def nex_scan(target, ports="1-10000"):
    print(f"[+] Starting Nex Scan on {target} (Ports: {ports})\n")
    scanner = nmap.PortScanner()
    
    print("[*] Scanning... Please wait.")
    start_time = time.time()
#    stop_spinner, spinner_thread = spinner("Scanning")

    try:
        scanner.scan(hosts=target, ports=ports, arguments="-sS -Pn -n -T4 --min-rate 500")
        end_time = time.time()
        print(f"[✓] Scan completed in {end_time - start_time:.2f} seconds.")
 #       stop_spinner()
  #      spinner_thread.join()
        print("[DEBUG] Scan completed. Processing results...")

        for host in scanner.all_hosts():
            print(f"\nHost: {host} ({scanner[host].hostname()})")
            print(f"State: {scanner[host].state()}")

            if 'osmatch' in scanner[host]:
                os_guesses = scanner[host]['osmatch']
                if os_guesses:
                    print(f"OS Guess: {os_guesses[0]['name']}")

            for proto in scanner[host].all_protocols():
                print(f"\nProtocol: {proto}")
                ports = scanner[host][proto].keys()
                for port in sorted(ports):
                    service = scanner[host][proto][port]
                    print(f"Port: {port}\tState: {service['state']}\tService: {service.get('name', 'n/a')}")

    except Exception as e:
   #     stop_spinner()
    #    spinner_thread.join()
        print(f"[-] Nex encountered an error: {e}")

def dir_buster():
    target_url = input("Enter target URL (e.g. http://example.com): ").strip()
    if not target_url.startswith("http"):
        target_url = "http://" + target_url

    print("\nPopular wordlists:")
    print("1. /usr/share/wordlists/dirb/common.txt")
    print("2. /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt")
    print("3. /usr/share/seclists/Discovery/Web-Content/common.txt")

    choice = input("Enter path to wordlist or press 1/2/3 to auto-select: ").strip()

    if choice == "1":
        wordlist = "/usr/share/wordlists/dirb/common.txt"
    elif choice == "2":
        wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
    elif choice == "3":
        wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"
    elif os.path.exists(choice):
        wordlist = choice
    else:
        print("[!] Invalid input or path. Exiting.")
        return

    print(f"\n[+] Starting Directory Buster on {target_url}")
    print(f"[+] Using wordlist: {wordlist}")
    print("-----------------------------------------")
    start_time = time.time()

   # stop_spinner, spinner_thread = spinner("Scanning")

    try:
        with open(wordlist, 'r') as file:
            for line in file:
                word = line.strip()
                url = f"{target_url.rstrip('/')}/{word}"
                try:
                    res = requests.get(url, timeout=3)
                    if res.status_code == 200:
                        print(f"[200 OK] {url}")
                    elif res.status_code == 403:
                        print(f"[403 Forbidden] {url}")
                except requests.RequestException:
                    pass
    except FileNotFoundError:
        print("[-] Wordlist file not found.")
    end_time = time.time()

   # stop_spinner()
   # spinner_thread.join()

    print("-----------------------------------------")
    print(f"[✓] Directory scan complete in {end_time - start_time:.2f} seconds.")

def galactico_scan():
    target = input("Enter target URL or IP for galactico scan: ").strip()
    print(f"\nRunning glactico scan on: {target}\n")
    start_time = time.time()

    try:
        result = subprocess.run(
            ["nuclei", "-u", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in result.stdout.splitlines():
            if "projectdiscovery" not in line and "____" not in line:
                print(line)
                end_time = time.time()
                print(f"[✓] Galactico scan complete in {end_time - start_time:.2f} seconds.")
    except subprocess.CalledProcessError:
        print("Error running glactico. Make sure it's installed and in your PATH.")


def main_menu():
    banner()
    while True:
        print("\n[1] Nex Port Scanner")
        print("[2] Directory Buster")
        print("[3] galactico Scanner")
        print("[4] Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            target = input("Enter the target IP or hostname: ")
            port_range = input("Enter the port range (default 1-10000): ") or "1-1000"
            nex_scan(target, port_range)

        elif choice == "2":
            dir_buster()

        elif choice == "3":
           galactico_scan()

        elif choice == "4":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()


