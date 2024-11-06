import requests
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Couleurs
RESET = "\033[0m"
VIOLET = "\033[38;5;93m"
WHITE = "\033[97m"
LIGHT_BLUE = "\033[38;5;123m"

def current_time_hour():
    """Retourne l'heure actuelle formatée en HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")

def Slow(text):
    """Affiche le texte avec une légère pause entre chaque caractère."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.01)
    print()

def Censored(text):
    """Affiche une version censurée du texte (par exemple, pour masquer certains caractères)."""
    censored_text = text[:2] + '*' * (len(text) - 4) + text[-2:]
    print(f"{VIOLET}[CENSORED]{RESET} {censored_text}")

def Continue():
    """Demande à l'utilisateur de continuer en appuyant sur une touche."""
    input(f"{VIOLET}[INFO]{RESET} Press Enter to continue...")

def Reset():
    """Réinitialise l'affichage des couleurs (si nécessaire)."""
    print(RESET, end='')

def Title(title):
    """Affiche un titre formaté."""
    print(f"\n{VIOLET}{'=' * len(title)}\n{title}\n{'=' * len(title)}{RESET}\n")

def Error(e):
    """Affiche les erreurs capturées."""
    print(f"{VIOLET}[ERROR]{RESET} {str(e)}")

def ErrorModule(e):
    """Gestion d'erreur pour les modules spécifiques."""
    Error(f"Module Error: {e}")

def osint_banner():
    """Retourne une bannière pour l'OSINT (illustratif)."""
    return f"{LIGHT_BLUE}OsintMx - Username Tracker{RESET}"

Title("Username Tracker")

try:
    sites = {
        "Roblox Trade": "https://rblx.trade/p/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Instagram": "https://www.instagram.com/{}",
        "Paypal": "https://www.paypal.com/paypalme/{}",
        "GitHub": "https://github.com/{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Snapchat": "https://www.snapchat.com/add/{}",
        "Telegram": "https://t.me/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "DeviantArt": "https://www.deviantart.com/{}",
        "LinkedIn": "https://www.linkedin.com/in/{}",
    }

    def site_exception(username, site, page_content):
        """Traite les exceptions spécifiques aux sites."""
        if site == "Paypal":
            page_content = page_content.replace(f'slug_name={username}', '').replace(f'"slug":"{username}"', '').replace(f'2F{username}&amp', '')
        elif site == "TikTok":
            page_content = page_content.replace(f'\\u002f@{username}"', '')
        return page_content

    number_site = 0
    number_found = 0
    sites_and_urls_found = []

    Slow(osint_banner())
    username = input(f"\n{VIOLET + current_time_hour() + RESET} {LIGHT_BLUE}Username -> {RESET}")
    Censored(username)

    username = username.lower()

    print(f"{VIOLET + current_time_hour() + RESET} {LIGHT_BLUE}Scanning...{RESET}")

    for site, url_template in sites.items():
        try:
            number_site += 1
            url = url_template.format(username)
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    page_content = re.sub(r'<[^>]*>', '', response.text.lower().replace(url, "").replace(f"/{username}", ""))
                    page_content = site_exception(username, site, page_content)
                    page_text = BeautifulSoup(response.text, 'html.parser').get_text().lower().replace(url, "")
                    page_title = BeautifulSoup(response.content, 'html.parser').title.string.lower()

                    found = username in page_title or username in page_content or username in page_text
                    if found:
                        number_found += 1
                        sites_and_urls_found.append(f"{site}: {WHITE + url}")
                        print(f"{VIOLET + current_time_hour() + RESET} {LIGHT_BLUE}[FOUND] {site}: {WHITE + url}")
                    else:
                        print(f"{VIOLET + current_time_hour() + RESET} [NOT FOUND] {site}:{RESET} Not Found")
                else:
                    print(f"{VIOLET + current_time_hour() + RESET} [ERROR] {site}:{RESET} Status code {response.status_code}")
            except Exception as e:
                print(f"{VIOLET + current_time_hour() + RESET} [ERROR] {site}:{RESET} {str(e)}")
        except:
            pass

    print(f"\n{VIOLET + current_time_hour() + RESET} {LIGHT_BLUE}Total Found:{RESET}")
    for site_and_url_found in sites_and_urls_found:
        time.sleep(0.5)
        print(f"{VIOLET + current_time_hour() + RESET} {LIGHT_BLUE}{site_and_url_found}{RESET}")

    print(f"\n{VIOLET + current_time_hour() + RESET} {LIGHT_BLUE}Total Websites: {WHITE}{number_site}{LIGHT_BLUE} Total Found: {WHITE}{number_found}{RESET}")
    Continue()
    Reset()
except Exception as e:
    Error(e)
