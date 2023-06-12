#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import html
import requests
import argparse
import time
import urllib.parse
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    print(        
         """

                ██╗░░██╗░██████╗░██████╗  ██╗░░██╗██╗██╗░░░░░██╗░░░░░███████╗██████╗░
                ╚██╗██╔╝██╔════╝██╔════╝  ██║░██╔╝██║██║░░░░░██║░░░░░██╔════╝██╔══██╗
                ░╚███╔╝░╚█████╗░╚█████╗░  █████═╝░██║██║░░░░░██║░░░░░█████╗░░██████╔╝
                ░██╔██╗░░╚═══██╗░╚═══██╗  ██╔═██╗░██║██║░░░░░██║░░░░░██╔══╝░░██╔══██╗
                ██╔╝╚██╗██████╔╝██████╔╝  ██║░╚██╗██║███████╗███████╗███████╗██║░░██║
                ╚═╝░░╚═╝╚═════╝░╚═════╝░  ╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝

                                                                           
                                                                       by AbelJM
        """)

def printError(msg): 
    print(f"{Fore.RED}[-] {msg}{Fore.RESET}")

def printSuccess(msg):
    print(f"{Fore.GREEN}[+] {msg}{Fore.RESET}")

def Send_req(url,payloads,file,verbose, proxy):
    for payload in payloads:
        payload_enc = urllib.parse.quote(payload)
        new_url = re.sub(r"=[^?\|&]*", "=" + payload_enc, url)

        payload_esc = html.escape(payload)

        try:
            if proxy:
                proxies = {
                    'http': proxy,
                    'https': proxy
                    }
                res = requests.get(new_url, timeout=5, verify=False, proxies=proxies)
            else:
                res = requests.get(new_url, timeout=5, verify=False)


            if payload in res.text:
                if "Content-Type" in res.headers and "text/html" in res.headers["Content-Type"]:
                    printSuccess(f"{new_url}")

                if file:
                    saveFile(file,new_url)
            else:
                if verbose:
                    printError(new_url)

        except requests.exceptions.HTTPError as e:
            pass

def Threads_req(list_url,list_payloads,workers,file,verbose,proxy):
    threads = []
    with ThreadPoolExecutor(max_workers=workers)  as executor:
        for url in list_url:
            url = url.strip()
            t = executor.submit(Send_req,url,list_payloads,file,verbose,proxy)
            threads.append(t)
        wait(threads)

def saveFile(name_file,data):
    path = os.getcwd()
    path_file = "%s/%s" %(path,name_file)
    with open(path_file, mode='a+', encoding='utf-8') as file:
        file.write('%s\n' %(data))
        file.close()


def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', help='Ocultar banner', action='store_true')
    parser.add_argument('-t', '--threads',help='Threads', type=int, default=3)
    parser.add_argument('-u', '--url', help='URL para escanear', metavar='')
    parser.add_argument('-l', '--list', help='Archivo con lista de urls', metavar='')
    parser.add_argument('-s', '--pipe', help='Recibir datos de stding/pipe', action='store_true')
    parser.add_argument('-p', '--payload', help='lista de payloads XSS', metavar='')
    parser.add_argument('--proxy', type=str, help='Especifica un proxy para utilizar con las peticiones')
    parser.add_argument('-d', help='duracion del escaneo', action='store_true')
    parser.add_argument('-o', '--output', help='Guardar output en archivo de texto', metavar='')
    parser.add_argument('-v', '--verbose', help='modo verbose', action='store_true')
    
    args = parser.parse_args()

    init_time = time.time()

    if not args.q:
        banner()

    if args.url and (args.list):
        print("No puede utilizar al mismo tiempo los argumentos -u --url, -l --list, -s --pipe")
        sys.exit(2)

    if args.payload:
        payloads = [line.strip() for line in open(args.payload,"r")]
    else:
        payloads = ["\"></script><script>alert('xss')</script>"]
    
    if args.url:
        url = args.url.split()        

    elif args.pipe:
        url = [line.strip() for line in sys.stdin]

    elif args.list:
        url = [line.strip() for line in open(args.list,"r")]

    else:
        print("Nesecariamente tiene que poner -u o -l")
        sys.exit(2)

    Threads_req(url,payloads,args.threads,args.output,args.verbose,args.proxy)

    if args.d:
        total_time = time.time() - init_time
        print(f'\nTotal time: {round(total_time, 2)} sec')   

if __name__ == "__main__":
    main()