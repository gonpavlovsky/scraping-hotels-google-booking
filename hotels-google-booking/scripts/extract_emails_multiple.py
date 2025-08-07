from playwright.sync_api import sync_playwright
import pandas as pd
import re
import time

# Cargar el archivo con los sitios web obtenidos de Google Maps para múltiples ciudades
input_file = "google_maps_results_multiple_cities.xlsx"
df = pd.read_excel(input_file)

# Crear una nueva columna para los correos
df["Emails"] = None

# Expresión regular para buscar correos electrónicos
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def extract_emails_from_page(page):
    """Extrae correos electrónicos del contenido de la página."""
    emails = set()
    page_text = page.content()
    emails.update(email_pattern.findall(page_text))
    return list(emails)

def scrape_emails(url):
    """Visita el sitio web y extrae los correos electrónicos."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            time.sleep(5)  # Esperar a que se cargue el contenido
            
            emails = extract_emails_from_page(page)
            browser.close()
            return ", ".join(emails) if emails else None
    except Exception as e:
        print(f"Error en {url}: {e}")
        return None

# Iterar por cada sitio web y extraer los correos
for index, row in df.iterrows():
    website = row["Website"]  # Usar el nombre correcto de la columna en el Excel
    if pd.notna(website) and website.startswith("http"):
        print(f"🔍 Buscando emails en: {website}")
        df.at[index, "Emails"] = scrape_emails(website)

# Guardar los resultados en un nuevo archivo Excel
output_file = "google_maps_results_with_emails_multiple_cities.xlsx"
df.to_excel(output_file, index=False)
print(f"✅ Correos electrónicos guardados en '{output_file}'")