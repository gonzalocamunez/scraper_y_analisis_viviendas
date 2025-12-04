import random
from camoufox.sync_api import Camoufox

def get_mac_fonts(seed=None, count=10):
    """Devuelve lista de fonts directamente para Camoufox"""
    if seed:
        random.seed(seed)
    
    custom_fonts = [
        # Microsoft Office
        "Calibri", "Cambria", "Consolas", "Constantia", "Corbel", "Candara",
        # Adobe
        "Myriad Pro", "Minion Pro", "Adobe Garamond Pro", "Adobe Caslon Pro",
        "Proxima Nova", "Brandon Grotesque", "Acumin Pro", "Adobe Arabic",
        # Google Fonts populares
        "Roboto", "Open Sans", "Lato", "Montserrat", "Poppins", "Inter",
        "Raleway", "Ubuntu", "Oswald", "Playfair Display", "Noto Sans",
        "Work Sans", "Nunito", "PT Sans", "Source Sans Pro", "Merriweather",
        # Desarrollo
        "Fira Code", "JetBrains Mono", "Source Code Pro", "Cascadia Code",
        "Hack", "Inconsolata", "Ubuntu Mono", "Droid Sans Mono", "Victor Mono",
        # Diseño/Apps
        "SF Pro Display", "Circular", "Graphik", "Apercu", "Gilroy",
        "Avenir Next Pro", "DIN", "Gotham", "Neue Haas Grotesk Display",
        "Atlas Grotesk", "Maison Neue", "Suisse Int'l", "Akkurat",
        # Misc apps populares
        "Slack-Lato", "WhatsApp Font", "Spotify Circular", "Netflix Sans",
        "YouTube Sans", "IBM Plex Sans", "Samsung Sans", "Google Sans"
    ]
    
    return random.sample(custom_fonts, min(count, len(custom_fonts)))

with Camoufox(
    headless=False,         # False para ver la página durante los tests.
    main_world_eval=False,
    persistent_context=True,
    enable_cache=False,     # False Aporta potencialmente un poco de stealth. Revisar notas por si cambiamos.
    block_webrtc=True,      # con proxy bueno (común y justificable). Revisar notas por si cambiamos.
    block_webgl=False,      # Solo bloquea WebGL si la privacidad es crítica y aceptas el riesgo de detección aumentado.
    block_images=True,      # Blocks all requests to images. This can help save your proxy usage.
    user_data_dir="./user_data", #Poner la ruta de la carpeta (!)
    os="macos",             # MacOS
    fonts=get_mac_fonts("session_123", 12),  # Devuelve lista directamente
    webgl_config=("Apple", "Apple M2, or similar"),
    geoip=True,             # Importante para evitar detección.
    proxy={
        'server': 'http://example.com:8080',
        'username': 'username',
        'password': 'password'
    }
) as browser:
    page = browser.new_page()
    page.goto("https://www._________.com/")
