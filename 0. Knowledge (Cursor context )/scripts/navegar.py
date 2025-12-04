from camoufox.sync_api import Camoufox

with Camoufox() as browser:
    page = browser.new_page()
    page.goto("https://www.browserscan.net")

    # Wait for Network Idle
    page.wait_for_load_state('networkidle')

    # Wait more, just in case
    page.wait_for_timeout(10000)


#page.goto("https://...") # navegar a una URL
#page.fill("selector", "texto") # escribir en un input
#page.hover("selector") # mover el ratón
#page.click("selector") # hacer clic en un elemento