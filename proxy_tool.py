from os import system
from colorama import Fore
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
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all",
        "https://api.openproxylist.xyz/http.txt",
        "https://www.proxyscan.io/download?type=http",
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
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
        "https://api.openproxylist.xyz/socks4.txt",
        "https://www.proxyscan.io/download?type=socks4",
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
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&country=all",
        "https://api.openproxylist.xyz/socks5.txt",
        "https://www.proxyscan.io/download?type=socks5",
    ]
}
import array

colors = [
    Fore.WHITE,
    Fore.LIGHTRED_EX,
    Fore.LIGHTGREEN_EX,
    Fore.RED,
    Fore.YELLOW,
    Fore.LIGHTBLUE_EX,
    Fore.RESET
]

def log_print(garbage_but_ok):
    if enable_logging:
        with open(f"logs-{time.strftime('%d-%m-%y')}.txt", "a") as file:
            to_write = re.sub(r"\033\[(\d|;)+?m", "", garbage_but_ok)
            file.write(f"[{time.strftime('%d/%m/%y %H:%M')}] " + to_write + "\n")
            file.flush()
    
    return print(garbage_but_ok)

def scrape(type):
    global remove_duplicates, total_duplicates, shuffle_output, total_scrapped
    system("cls")
    if clear_previous_results:
        with open(f"output-{type}.txt", "a") as file:
            file.truncate(0)
            log_print(colors[1] + "[!] " + colors[0] + f"output-{type}.txt has been cleared")
            time.sleep(1)
    
    collected_proxies = []
    try:
        print(colors[1] + "[!] " + colors[0] + f"Press CTRL+C to stop action")
        log_print(colors[1] + "[!] " + colors[0] + f"Started scrape for {type} proxies:")
        with open(f"output-{type}.txt", "a") as file:
            idx = 1
            total_sources = len(proxy_sources[type])
            for key, url in enumerate(proxy_sources[type]):
                if idx >= proxy_limit:
                    break
                log_print(colors[2] + f"Scraping from target ({key+1}/{total_sources})")
                time.sleep(1)
                response = requests.get(url)
                if response.status_code >= 200 and response.status_code < 300:
                    for key, value in enumerate(response.iter_lines()):
                        if idx >= proxy_limit:
                            break
                        
                        collected_proxies.insert(idx, value)
                        idx += 1

            if remove_duplicates:
                old_length = len(collected_proxies)
                collected_proxies = list(dict.fromkeys(collected_proxies))
                duplicates = old_length-len(collected_proxies)
                log_print(colors[1] + "[!] " + colors[0] + f"Removed {duplicates} duplicates")
                total_duplicates += duplicates

            if shuffle_output:
                random.shuffle(collected_proxies)
            
            for key, value in enumerate(collected_proxies):
                file.write(value.decode() + "\n")

            file.flush() # Flush the file buffer to ensure immediate write (thanks chatgpt)
            total_scrapped += idx
            log_print(colors[1] + "[!] " + colors[0] + f"{idx}x {type} proxies have been scraped")
            log_print(colors[1] + "[!] " + colors[0] + f"Scraped proxies were saved to output-{type}.txt")
            time.sleep(4)
            return handle_main()
    except KeyboardInterrupt:
        collected_proxies_len = len(collected_proxies)
        if collected_proxies_len > 0:
            with open(f"output-{type}.txt", "a") as file:
                for key, value in enumerate(collected_proxies):
                    file.write(value.decode() + "\n")
                file.flush()
                
        total_scrapped += collected_proxies_len
        
        return handle_main()
    
def checker(type):
    global get_response_from, response_timeout
    system("cls")
    print(colors[1] + "[!] " + colors[0] + f"Press CTRL+C to stop action")
    log_print(colors[1] + "[!] " + colors[0] + f"Starting proxy check on output-{type}.txt:")
    collected_proxies = []
    good_proxies = []
    bad_proxies = []
    try:
        with open(f"output-{type}.txt", "r") as file:
            collected_proxies = file.read().splitlines()
            total_proxies = len(collected_proxies)+1
            for key, proxy in enumerate(collected_proxies):
                start_time = time.time()
                response = requests.get(get_response_from, proxies={type: proxy}, timeout=response_timeout, headers = {"User-Agent": "Mozilla/5.0"})
                end_time = time.time()
                response_time = math.floor((end_time - start_time) * 1000)
                if response.status_code == 200:
                    log_print(colors[2] + f"{proxy} - Good! [{response_time}ms] ({key+1}/{total_proxies})")
                    good_proxies.insert(key, proxy)
                else:
                    log_print(colors[1] + f"{proxy} - Bad! [{response_time}ms] ({key+1}/{total_proxies})")
                    bad_proxies.insert(key, proxy)
                
    except requests.exceptions.RequestException:
        log_print(colors[3] + f"{proxy} - Bad (ERROR)! ({key})")
        bad_proxies.insert(key, proxy)
    except KeyboardInterrupt:
        return handle_main()

    if len(good_proxies) >= 1:
        with open(f"output-{type}-good.txt", "a") as file:
            for key, value in enumerate(good_proxies):
                file.write(value + "\n")

            file.flush()
        
    if len(bad_proxies) >= 1:
        with open(f"output-{type}-bad.txt", "a") as file:
            for key, value in enumerate(bad_proxies):
                file.write(value + "\n")

            file.flush()
    
    time.sleep(4)
    return handle_main()

def display_info():
    global total_scrapped
    print(colors[4] + "██████████████████████████████████████████████████████")
    print(colors[4] + "█▄─▄▄─█▄─▄▄▀█─▄▄─█▄─▀─▄█▄─█─▄███─▄─▄─█─▄▄─█─▄▄─█▄─▄███")
    print(colors[4] + "██─▄▄▄██─▄─▄█─██─██▀─▀███▄─▄██████─███─██─█─██─██─██▀█")
    print(colors[4] + "▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▀▄▄█▄▄▀▀▄▄▄▀▀▀▀▀▄▄▄▀▀▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀")
    print(colors[0] + "All proxies are taken from public sources available on the internet.")
    print(colors[5] + "Made by Nertigel\ngithub.com/nertigel")

    print(colors[2] + f"Scraped: {total_scrapped} " + colors[0] + "|" + colors[3] + f" Duplicates: {total_duplicates}")

    print(colors[6])
    return

def display_options():
    system("cls")
    display_info()

    print(colors[1] + "[-] " + colors[0] + "Please enter your choice:")
    print(colors[1] + "[1] " + colors[0] + "Scrape HTTP")
    print(colors[1] + "[2] " + colors[0] + "Scrape SOCKS4")
    print(colors[1] + "[3] " + colors[0] + "Scrape SOCKS5")
    print(colors[1] + "[4] " + colors[0] + "Check HTTP")
    print(colors[1] + "[5] " + colors[0] + "Check SOCKS4")
    print(colors[1] + "[6] " + colors[0] + "Check SOCKS5")
    print(colors[1] + "[7] " + colors[0] + "Settings")
    print(colors[1] + "[8] " + colors[0] + "Exit")

    return

def display_settings():
    system("cls")
    display_info()

    print(colors[1] + "[0] " + colors[0] + "Enable logging: " + str(enable_logging))
    print(colors[1] + "[-] " + colors[0] + "Scrape settings")
    print(colors[1] + "[1] " + colors[0] + "Remove duplicate ips: " + str(remove_duplicates))
    print(colors[1] + "[2] " + colors[0] + "Shuffle list output: " + str(shuffle_output))
    print(colors[1] + "[3] " + colors[0] + "Clear previous results from files: " + str(clear_previous_results))
    print(colors[1] + "[4] " + colors[0] + "Limit proxies: " + str(proxy_limit))
    print(colors[1] + "[-] " + colors[0] + "Checker settings")
    print(colors[1] + "[5] " + colors[0] + "Get response from: " + str(get_response_from))
    print(colors[1] + "[6] " + colors[0] + "Timeout: " + str(response_timeout))
    print(colors[1] + "[7] " + colors[0] + "Back")

    return

def handle_main(skip=None):
    try:
        display_options()

        option = skip or int(input())
        if option == 1:
            return scrape("http")
        elif option == 2:
            return scrape("socks4")
        elif option == 3:
            return scrape("socks5")
        elif option == 4:
            return checker("http")
        elif option == 5:
            return checker("socks4")
        elif option == 6:
            return checker("socks5")
        elif option == 7:
            return handle_settings()
        elif option == 8:
            return exit()
        else:
            return handle_main()
    except ValueError:
        return exit()

def handle_settings():
    global enable_logging, remove_duplicates, shuffle_output, clear_previous_results
    display_settings()
    setting_option = int(input())
    if setting_option == 0:
        enable_logging = not enable_logging
    elif setting_option == 1:
        remove_duplicates = not remove_duplicates
    elif setting_option == 2:
        shuffle_output = not shuffle_output
    elif setting_option == 3:
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
        global proxy_limit
        print(colors[1] + "Enter an amount for proxy scrape limit (int):")
        setting = int(input())
        proxy_limit = setting
    except ValueError:
        handle_main(7)

def update_response_url():
    try:
        global get_response_from
        print(colors[1] + "Enter a url to get response from (default: https://www.google.com):")
        setting = str(input())
        get_response_from = setting
    except ValueError:
        handle_main(7)

def update_response_timeout():
    try:
        global response_timeout
        print(colors[1] + "Enter an amount for response timeout (default: 10):")
        setting = int(input())
        response_timeout = setting
    except ValueError:
        handle_main(7)

if __name__ == "__main__":
    handle_main()