from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_booking(city, checkin_date, checkout_date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Cambia a False para ver qué ocurre
        page = browser.new_page()
        
        # Construir URL de búsqueda
        search_url = f"https://www.booking.com/searchresults.html?ss={city}&checkin_year_month_monthday={checkin_date}&checkout_year_month_monthday={checkout_date}"
        print(f"Buscando en: {search_url}")
        page.goto(search_url, timeout=60000)

        # Esperar a que cargue la lista de alojamientos (esto evita errores)
        try:
            page.wait_for_selector('[data-testid="property-card"]', timeout=10000)
        except:
            print(f"No se encontraron alojamientos en {city} o la página no cargó correctamente.")
            browser.close()
            return []

        # Desplazarse hasta cargar todos los alojamientos
        previous_height = 0
        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break
            previous_height = current_height

        # Extraer nombres de alojamientos
        property_names = page.locator('[data-testid="title"]').all_text_contents()
        print(f"Nombres capturados en {city}: {len(property_names)} alojamientos encontrados")

        browser.close()
        return property_names

# Lista de ciudades para buscar
cities = ["Monteverde", "Playa Flamingo", "Puerto Vallarta", "Sayulita"]
checkin_date = "2025-03-20"
checkout_date = "2025-03-30"

# Almacenar resultados
all_data = []

for city in cities:
    print(f"Scraping para {city}...")
    properties = scrape_booking(city, checkin_date, checkout_date)
    for name in properties:
        all_data.append({"City": city, "Name": name})

# Guardar resultados en Excel
df = pd.DataFrame(all_data)
df.to_excel('booking_multiple_cities.xlsx', index=False)
print("Nombres de alojamientos guardados en 'booking_multiple_cities.xlsx'")
