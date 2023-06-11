from os import system
from colorama import Fore, Back, Style
import time, requests, random, math, re

system("title Proxy Scraper and Checker [HTTP/SOCKS4/SOCKS5] - github.com/nertigel/proxy_tool")

total_scrapped = 0
total_duplicates = 0
enable_logging = False
# scraper shit
proxy_limit = 100000
remove_duplicates = True
shuffle_output = False
clear_previous_results = True
# checker shit
get_response_from = "https://www.google.com"
response_timeout = 10

proxy_sources = {
    "http": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt",
        "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all",
        "https://api.openproxylist.xyz/http.txt",
    ],
    "socks4": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
        "https://api.openproxylist.xyz/socks4.txt",
    ],
    "socks5": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&country=all",
        "https://api.openproxylist.xyz/socks5.txt",
    ]
}

def log_print(garbage_but_ok):
    if enable_logging:
        print(garbage_but_ok)
        with open(f"logs-{time.strftime('%d-%m-%y')}.txt", "a") as file:
            to_write = re.sub(r'\033\[(\d|;)+?m', '', garbage_but_ok)
            file.write(f"[{time.strftime('%d/%m/%y %H:%M')}] " + to_write + "\n")
            file.flush()

def scrape(type):
    system("cls")
    if clear_previous_results:
        with open(f'output-{type}.txt', 'a') as file:
            file.truncate(0)
            log_print(Fore.LIGHTRED_EX + "[!] " + Fore.WHITE + f"output-{type}.txt has been cleared!")
            time.sleep(1)
    
    log_print(Fore.LIGHTRED_EX + "[!] " + Fore.WHITE + f"Started scrape for {type} proxy:")
    with open(f'output-{type}.txt', 'a') as file:
        collected_proxies = []
        idx = 1
        total_sources = len(proxy_sources[type])
        for key, url in enumerate(proxy_sources[type]):
            if idx >= proxy_limit:
                break
            log_print(Fore.LIGHTGREEN_EX + f"Scraping from target ({key+1}/{total_sources})")
            time.sleep(1)
            response = requests.get(url)
            if response.status_code >= 200 and response.status_code < 300:
                for key, value in enumerate(response.iter_lines()):
                    if idx >= proxy_limit:
                        break
                    
                    collected_proxies.insert(idx, value)
                    idx += 1

        global remove_duplicates
        if remove_duplicates:
            old_length = len(collected_proxies)
            collected_proxies = list(dict.fromkeys(collected_proxies))
            duplicates = old_length-len(collected_proxies)
            log_print(Fore.LIGHTRED_EX + "[!] " + Fore.WHITE + f"Removed {duplicates} duplicates")
            global total_duplicates
            total_duplicates += duplicates

        global shuffle_output
        if shuffle_output:
            random.shuffle(collected_proxies)
        
        for key, value in enumerate(collected_proxies):
            file.write(value.decode() + "\n")

        file.flush() # Flush the file buffer to ensure immediate write (thanks chatgpt)
        global total_scrapped
        total_scrapped += idx
        log_print(Fore.LIGHTRED_EX + "[!] " + Fore.WHITE + f"{idx}x {type} proxies have been scraped!")
        log_print(Fore.LIGHTRED_EX + "[!] " + Fore.WHITE + f"Scraped proxies were saved to output-{type}.txt!")
        time.sleep(4)
        return handle_main()
    
def checker(type):
    global get_response_from, response_timeout
    system("cls")
    log_print(Fore.LIGHTRED_EX + "[!] " + Fore.WHITE + f"Starting proxy check on output-{type}.txt:")
    collected_proxies = []
    good_proxies = []
    bad_proxies = []
    try:
        with open(f'output-{type}.txt', 'r') as file:
            collected_proxies = file.read().splitlines()
            total_proxies = len(collected_proxies)+1
            for key, proxy in enumerate(collected_proxies):
                start_time = time.time()
                response = requests.get(get_response_from, proxies={type: proxy}, timeout=response_timeout, headers = {'User-Agent': 'Mozilla/5.0'})
                end_time = time.time()
                response_time = math.floor((end_time - start_time) * 1000)
                if response.status_code == 200:
                    log_print(Fore.LIGHTGREEN_EX + f"{proxy} - Good! [{response_time}ms] ({key+1}/{total_proxies})")
                    good_proxies.insert(key, proxy)
                else:
                    log_print(Fore.LIGHTRED_EX + f"{proxy} - Bad! [{response_time}ms] ({key+1}/{total_proxies})")
                    bad_proxies.insert(key, proxy)
                
    except requests.exceptions.RequestException:
        log_print(Fore.RED + f"{proxy} - Bad (ERROR)! ({key})")
        bad_proxies.insert(key, proxy)

    if len(good_proxies) >= 1:
        with open(f'output-{type}-good.txt', 'a') as file:
            for key, value in enumerate(good_proxies):
                file.write(value + "\n")

            file.flush()
        
    if len(bad_proxies) >= 1:
        with open(f'output-{type}-bad.txt', 'a') as file:
            for key, value in enumerate(bad_proxies):
                file.write(value + "\n")

            file.flush()
    
    time.sleep(4)
    return handle_main()

def display_info():
    
    print(Fore.YELLOW + "██████████████████████████████████████████████████████")
    print(Fore.YELLOW + "█▄─▄▄─█▄─▄▄▀█─▄▄─█▄─▀─▄█▄─█─▄███─▄─▄─█─▄▄─█─▄▄─█▄─▄███")
    print(Fore.YELLOW + "██─▄▄▄██─▄─▄█─██─██▀─▀███▄─▄██████─███─██─█─██─██─██▀█")
    print(Fore.YELLOW + "▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▀▄▄█▄▄▀▀▄▄▄▀▀▀▀▀▄▄▄▀▀▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀")
    print(Fore.WHITE + "All proxies are taken from public sources available on the internet.")
    print(Fore.LIGHTBLUE_EX + "Made by Nertigel\ngithub.com/nertigel")

    global total_scrapped
    print(Fore.LIGHTGREEN_EX + f"Scraped: {total_scrapped} " + Fore.WHITE + "|" + Fore.RED + f" Duplicates: {total_duplicates}")

    print(Fore.RESET)
    return

def display_options():
    system("cls")
    display_info()

    print(Fore.LIGHTRED_EX + "[-] " + Fore.WHITE + "Please enter your choice:")
    print(Fore.LIGHTRED_EX + "[1] " + Fore.WHITE + "Scrape HTTP")
    print(Fore.LIGHTRED_EX + "[2] " + Fore.WHITE + "Scrape SOCKS4")
    print(Fore.LIGHTRED_EX + "[3] " + Fore.WHITE + "Scrape SOCKS5")
    print(Fore.LIGHTRED_EX + "[4] " + Fore.WHITE + "Check HTTP")
    print(Fore.LIGHTRED_EX + "[5] " + Fore.WHITE + "Check SOCKS4")
    print(Fore.LIGHTRED_EX + "[6] " + Fore.WHITE + "Check SOCKS5")
    print(Fore.LIGHTRED_EX + "[7] " + Fore.WHITE + "Settings")
    print(Fore.LIGHTRED_EX + "[8] " + Fore.WHITE + "Exit")

    return

def display_settings():
    system("cls")
    display_info()

    print(Fore.LIGHTRED_EX + "[0] " + Fore.WHITE + "Enable logging: " + str(enable_logging))
    print(Fore.LIGHTRED_EX + "[-] " + Fore.WHITE + "Scrape settings")
    print(Fore.LIGHTRED_EX + "[1] " + Fore.WHITE + "Remove duplicate ips: " + str(remove_duplicates))
    print(Fore.LIGHTRED_EX + "[2] " + Fore.WHITE + "Shuffle list output: " + str(shuffle_output))
    print(Fore.LIGHTRED_EX + "[3] " + Fore.WHITE + "Clear previous results from files: " + str(clear_previous_results))
    print(Fore.LIGHTRED_EX + "[4] " + Fore.WHITE + "Limit proxies: " + str(proxy_limit))
    print(Fore.LIGHTRED_EX + "[-] " + Fore.WHITE + "Checker settings")
    print(Fore.LIGHTRED_EX + "[5] " + Fore.WHITE + "Get response from: " + str(get_response_from))
    print(Fore.LIGHTRED_EX + "[6] " + Fore.WHITE + "Timeout: " + str(response_timeout))
    print(Fore.LIGHTRED_EX + "[7] " + Fore.WHITE + "Back")

    return

def handle_main(skip=None):
    try:
        display_options()

        option = skip or int(input())
        if option == 1:
            return scrape('http')
        elif option == 2:
            return scrape('socks4')
        elif option == 3:
            return scrape('socks5')
        elif option == 4:
            return checker('http')
        elif option == 5:
            return checker('socks4')
        elif option == 6:
            return checker('socks5')
        elif option == 7:
            return handle_settings()
        elif option == 8:
            return exit()
        else:
            return handle_main()
    except ValueError:
        return exit()

def handle_settings():
    display_settings()
    setting_option = int(input())
    if setting_option == 0:
        global enable_logging
        enable_logging = not enable_logging
    elif setting_option == 1:
        global remove_duplicates
        remove_duplicates = not remove_duplicates
    elif setting_option == 2:
        global shuffle_output
        shuffle_output = not shuffle_output
    elif setting_option == 3:
        global clear_previous_results
        clear_previous_results = not clear_previous_results
    elif setting_option == 4:
        update_proxy_limit()
    elif setting_option == 5:
        update_response_url()
    elif setting_option == 6:
        update_response_timeout()
    else:
        return handle_main()
    
    handle_main(7)

def update_proxy_limit():
    try:
        print(Fore.LIGHTRED_EX + "Enter an amount for proxy scrape limit (int):")
        setting = int(input())
        global proxy_limit
        proxy_limit = setting
    except ValueError:
        handle_main(7)

def update_response_url():
    try:
        print(Fore.LIGHTRED_EX + "Enter a url to get response from (example: https://www.google.com):")
        setting = str(input())
        global get_response_from
        get_response_from = setting
    except ValueError:
        handle_main(7)

def update_response_timeout():
    try:
        print(Fore.LIGHTRED_EX + "Enter a url to get response from (example: https://www.google.com):")
        setting = int(input())
        global response_timeout
        response_timeout = setting
    except ValueError:
        handle_main(7)

if __name__ == "__main__":
    handle_main()