#!/usr/bin/env python3
import os
import json
import sys
import time
import signal
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError

# Package installation check
try:
    from dotenv import load_dotenv
    import playwright
except ImportError:
    import subprocess
    import sys
    
    packages = [
        'playwright',
        'python-dotenv'
    ]
    
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    from dotenv import load_dotenv
    import playwright

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Virtual environment check
if not hasattr(sys, 'real_prefix') and (sys.prefix == sys.base_prefix):
    print("\n⚠️  You are not in a virtual environment!")
    print("To create and activate a virtual environment:")
    print("1. python -m venv venv")
    print("2. " + ("venv\\Scripts\\activate" if os.name == 'nt' else "source venv/bin/activate"))
    sys.exit(1)

load_dotenv()

# Configuration
BRAVE_PATH = os.getenv('BRAVE_PATH', '/usr/bin/brave-browser')
USER_DATA_DIR = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default")
RATE_LIMIT_DELAY = 3  # Animation handling delay
POKEBALL_TIMEOUT = 5  # Increased timeout for elements

# Complete list of all 151 Pokémon names
POKEMON_NAMES = [
    "Bulbasaur Pokemon", "Ivysaur Pokemon", "Venusaur Pokemon", "Charmander Pokemon", "Charmeleon Pokemon", "Charizard Pokemon",
    "Squirtle Pokemon", "Wartortle Pokemon", "Blastoise Pokemon", "Caterpie Pokemon", "Metapod Pokemon", "Butterfree Pokemon",
    "Weedle Pokemon", "Kakuna Pokemon", "Beedrill Pokemon", "Pidgey Pokemon", "Pidgeotto Pokemon", "Pidgeot Pokemon", "Rattata Pokemon",
    "Raticate Pokemon", "Spearow Pokemon", "Fearow Pokemon", "Ekans Pokemon", "Arbok Pokemon", "Pikachu Pokemon", "Raichu Pokemon",
    "Sandshrew Pokemon", "Sandslash Pokemon", "Nidoran (F) Pokemon", "Nidorina Pokemon", "Nidoqueen Pokemon", "Nidoran (M) Pokemon",
    "Nidorino Pokemon", "Nidoking Pokemon", "Clefairy Pokemon", "Clefable Pokemon", "Vulpix Pokemon", "Ninetales Pokemon",
    "Jigglypuff Pokemon", "Wigglytuff Pokemon", "Zubat Pokemon", "Golbat Pokemon", "Oddish Pokemon", "Gloom Pokemon", "Vileplume Pokemon",
    "Paras Pokemon", "Parasect Pokemon", "Venonat Pokemon", "Venomoth Pokemon", "Diglett Pokemon", "Dugtrio Pokemon", "Meowth Pokemon",
    "Persian Pokemon", "Psyduck Pokemon", "Golduck Pokemon", "Mankey Pokemon", "Primeape Pokemon", "Growlithe Pokemon", "Arcanine Pokemon",
    "Poliwag Pokemon", "Poliwhirl Pokemon", "Poliwrath Pokemon", "Abra Pokemon", "Kadabra Pokemon", "Alakazam Pokemon", "Machop Pokemon",
    "Machoke Pokemon", "Machamp Pokemon", "Bellsprout Pokemon", "Weepinbell Pokemon", "Victreebel Pokemon", "Tentacool Pokemon",
    "Tentacruel Pokemon", "Geodude Pokemon", "Graveler Pokemon", "Golem Pokemon", "Ponyta Pokemon", "Rapidash Pokemon", "Slowpoke Pokemon",
    "Slowbro Pokemon", "Magnemite Pokemon", "Magneton Pokemon", "Farfetch'd Pokemon", "Doduo Pokemon", "Dodrio Pokemon", "Seel Pokemon",
    "Dewgong Pokemon", "Grimer Pokemon", "Muk Pokemon", "Shellder Pokemon", "Cloyster Pokemon", "Gastly Pokemon", "Haunter Pokemon", "Gengar Pokemon",
    "Onix Pokemon", "Drowzee Pokemon", "Hypno Pokemon", "Krabby Pokemon", "Kingler Pokemon", "Voltorb Pokemon", "Electrode Pokemon",
    "Exeggcute Pokemon", "Exeggutor Pokemon", "Cubone Pokemon", "Marowak Pokemon", "Hitmonlee Pokemon", "Hitmonchan Pokemon",
    "Lickitung Pokemon", "Koffing Pokemon", "Weezing Pokemon", "Rhyhorn Pokemon", "Rhydon Pokemon", "Chansey Pokemon", "Tangela Pokemon",
    "Kangaskhan Pokemon", "Horsea Pokemon", "Seadra Pokemon", "Goldeen Pokemon", "Seaking Pokemon", "Staryu Pokemon", "Starmie Pokemon",
    "Mr. Mime Pokemon", "Scyther Pokemon", "Jynx Pokemon", "Electabuzz Pokemon", "Magmar Pokemon", "Pinsir Pokemon", "Tauros Pokemon",
    "Magikarp Pokemon", "Gyarados Pokemon", "Lapras Pokemon", "Ditto Pokemon", "Eevee Pokemon", "Vaporeon Pokemon", "Jolteon Pokemon",
    "Flareon Pokemon", "Porygon Pokemon", "Omanyte Pokemon", "Omastar Pokemon", "Kabuto Pokemon", "Kabutops Pokemon", "Aerodactyl Pokemon",
    "Snorlax Pokemon", "Articuno Pokemon", "Zapdos Pokemon", "Moltres Pokemon", "Dratini Pokemon", "Dragonair Pokemon", "Dragonite Pokemon",
    "Mewtwo Pokemon", "Mew Pokemon"
]

class PokemonCatcher:
    def __init__(self):
        self.caught_pokemon = self.load_progress()
        self.current_pokemon = None
        self.device = {
            "user_agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
            "viewport": {"width": 360, "height": 740}
        }
        self.should_exit = False
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        clear_screen()
        print("\n🛑 Received interrupt signal. Saving progress...")
        self.should_exit = True
        self.save_progress()
        sys.exit(0)

    def load_progress(self):
        try:
            with open('progress.json', 'r') as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    def save_progress(self):
        with open('progress.json', 'w') as f:
            json.dump(list(self.caught_pokemon), f)

    def handle_animation_delay(self):
        time.sleep(RATE_LIMIT_DELAY)

    def run(self):
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                executable_path=BRAVE_PATH,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
                viewport=self.device["viewport"],
                user_agent=self.device["user_agent"],
                channel='chrome'
            )

            try:
                # Close all existing tabs except first
                for page in context.pages[1:]:
                    page.close()
                
                page = context.pages[0]

                for pokemon in POKEMON_NAMES:
                    if self.should_exit:
                        break
                    
                    if pokemon in self.caught_pokemon:
                        print(f"⏩ Skipping {pokemon} (already caught)")
                        continue

                    self.current_pokemon = pokemon
                    if self.catch_pokemon(page):
                        self.caught_pokemon.add(pokemon)
                        self.save_progress()

            except Exception as e:
                print(f"❌ Critical error: {e}")
            finally:
                context.close()

    def catch_pokemon(self, page):
        print(f"🎯 Attempting to catch {self.current_pokemon}")
        base_name = self.current_pokemon.replace(" Pokemon", "")
        attempts = [self.current_pokemon, base_name]
        
        for search_query in attempts:
            try:
                # Perform search and wait for game to load
                page.goto(f"https://www.google.com/search?q={search_query}", timeout=60000)
                
                # Wait for game container
                page.wait_for_selector('div[data-attrid="title"]', timeout=POKEBALL_TIMEOUT*1000)
                
                # Find and click the pokeball
                pokeball = page.wait_for_selector('g-ripple.aaU6gd', state="visible", timeout=POKEBALL_TIMEOUT*1000)
                pokeball.click(delay=100)
                self.handle_animation_delay()
                
                # Check for success message
                page.wait_for_selector('span[jsname="B4OA0d"]:has-text("Gotcha!")', timeout=15000)

                # Check and claim Master Ball
                try:
                    master_ball_btn = page.wait_for_selector('div.btku5b:has-text("Claim Master Ball")', timeout=5000)
                    master_ball_btn.click()
                    print("🎉 Claimed Master Ball!")
                    time.sleep(1)  # Allow claim animation
                except TimeoutError:
                    pass  # No Master Ball available
                
                # Wait before closing popup
                print("⏳ Waiting 1 seconds before closing popup...")
                time.sleep(1)
                
                # Close modal using X button
                close_btn = page.wait_for_selector('div.I4LJKd[aria-label="Close"]', state="visible", timeout=5000)
                close_btn.click()
                
                print(f"✅ Successfully caught {search_query}!")
                return True

            except TimeoutError:
                print(f"⚠️  Failed to catch {search_query}: Game elements not found")
                continue
            except Exception as e:
                print(f"⚠️  Error catching {search_query}: {str(e)}")
                continue
        
        print(f"⚠️  All attempts failed for {self.current_pokemon}")
        return False

if __name__ == "__main__":
    clear_screen()
    print("🚀 Starting Pokémon Auto-Catcher 🚀")
    print("🛠️  Script coded by Phr34kz")
    print("⚠️  Keep browser window focused and don't move mouse!")
    catcher = PokemonCatcher()
    try:
        catcher.run()
    finally:
        clear_screen()
        print(f"🎉 Completed! Caught {len(catcher.caught_pokemon)}/151 Pokémon!")
