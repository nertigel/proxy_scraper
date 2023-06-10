from asyncio.windows_events import NULL
from os import system
from time import sleep
from colorama import Fore, Back, Style
import requests, random

total_scrapped = 0
proxy_limit = 10000
remove_duplicates = True
shuffle_output = False

proxy_sources = {
    "http": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all",
        "https://api.openproxylist.xyz/http.txt",
    ],
    "socks4": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
        "https://api.openproxylist.xyz/socks4.txt",
    ],
    "socks5": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&country=all",
        "https://api.openproxylist.xyz/socks5.txt",
    ]
}

def scrape(type):
    with open(f'output-{type}.txt', 'a') as file:
        collected_proxies = []
        idx = 1
        for key, url in enumerate(proxy_sources[type]):
            if idx >= proxy_limit:
                break
            print(Fore.LIGHTGREEN_EX + f"Scraping from {url}")
            sleep(1)
            response = requests.get(url)
            for key, value in enumerate(response.iter_lines()):
                if idx >= proxy_limit:
                    break
                
                collected_proxies.insert(idx, value)
                idx += 1

        global remove_duplicates
        if remove_duplicates:
            collected_proxies = list(dict.fromkeys(collected_proxies))

        global shuffle_output
        if shuffle_output:
            random.shuffle(collected_proxies)
        
        for key, value in enumerate(collected_proxies):
            file.write(value.decode() + "\n")

        global total_scrapped
        total_scrapped += idx
        print(f"Scraped {idx} {type} proxies!\nSaved to file!")
        sleep(2)
        main()
    return

def display_info():
    print(Fore.YELLOW + "███████████████████████████████████████████")
    print(Fore.YELLOW + "█─▄▄▄▄█─▄▄▄─█▄─▄▄▀██▀▄─██▄─▄▄─█▄─▄▄─█▄─▄▄▀█")
    print(Fore.YELLOW + "█▄▄▄▄─█─███▀██─▄─▄██─▀─███─▄▄▄██─▄█▀██─▄─▄█")
    print(Fore.YELLOW + "▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▀▀▀▄▄▄▄▄▀▄▄▀▄▄▀")
    print(Fore.WHITE + "All proxies are taken from public sources available on the internet.")
    print(Fore.LIGHTBLUE_EX + "Made by Nertigel\ngithub.com/nertigel")

    global total_scrapped
    print(Fore.LIGHTGREEN_EX + f"Scraped: {total_scrapped}")

    print(Fore.RESET)
    return

def display_options():
    system("cls")
    display_info()

    print(Fore.LIGHTRED_EX + "[1] " + Fore.WHITE + "Scrape HTTP")
    print(Fore.LIGHTRED_EX + "[2] " + Fore.WHITE + "Scrape Socks4")
    print(Fore.LIGHTRED_EX + "[3] " + Fore.WHITE + "Scrape Socks5")
    print(Fore.LIGHTRED_EX + "[4] " + Fore.WHITE + "Settings")
    print(Fore.LIGHTRED_EX + "[5] " + Fore.WHITE + "Exit")

    return

def display_settings():
    system("cls")
    display_info()

    print(Fore.LIGHTRED_EX + "[1] " + Fore.WHITE + "Remove duplicates: " + str(remove_duplicates))
    print(Fore.LIGHTRED_EX + "[2] " + Fore.WHITE + "Shuffle output: " + str(shuffle_output))
    print(Fore.LIGHTRED_EX + "[3] " + Fore.WHITE + "Limit: " + str(proxy_limit))
    print(Fore.LIGHTRED_EX + "[4] " + Fore.WHITE + "Back")

    return

def main(skip=NULL):
    display_options()

    option = skip or int(input())
    if option == 1:
        scrape('http')
    elif option == 2:
        scrape('socks4')
    elif option == 3:
        scrape('socks5')
    elif option == 4:
        display_settings()

        setting_option = int(input())
        if setting_option == 1:
            global remove_duplicates
            remove_duplicates = not remove_duplicates
            main(4)
        elif setting_option == 2:
            global shuffle_output
            shuffle_output = not shuffle_output
            main(4)
        elif setting_option == 3:
            try:
                print(Fore.LIGHTRED_EX + "Please enter amount for proxy limit (int):")
                setting = int(input())
                global proxy_limit
                proxy_limit = setting
                main(4)
            except:
                main(4)
        else:
            main()

    elif option == 5:
        exit()
    else:
        main()
    
    return

if __name__ == "__main__":
    main()