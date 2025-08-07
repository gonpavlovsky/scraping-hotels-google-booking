from playwright.sync_api import sync_playwright
import pandas as pd
import re
import time

# Leer el archivo Excel generado en el Paso 1
excel_file = 'hotels_hostels_property_management_filtered.xlsx'  # Ajusta al nombre de tu archivo
df = pd.read_excel(excel_file)

# Función para validar correos electrónicos
def is_valid_email(email):
    # Excluir correos irrelevantes según patrones
    invalid_patterns = ['@sentry-next.wixpress.com', '@example.com', 'no-reply', 'noreply']
    return not any(pattern in email for pattern in invalid_patterns)

# Función para encontrar correos electrónicos en una página web
def find_emails_in_website(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)  # Timeout de 60 segundos para sitios lentos
            time.sleep(5)  # Esperar para que cargue el contenido
            page_content = page.content()
            
            # Buscar correos electrónicos con regex
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_content)
            
            # Filtrar correos inválidos
            emails = [email for email in emails if is_valid_email(email)]
            
            browser.close()
            return list(set(emails))  # Eliminar duplicados
    except Exception as e:
        print(f"Error al procesar {url}: {e}")
        return []

# Agregar columnas para los correos electrónicos
df['Email 1'] = None
df['Email 2'] = None
df['Email 3'] = None

# Iterar sobre cada fila del DataFrame y buscar correos en los sitios web
for index, row in df.iterrows():
    website = row.get('website')
    if pd.notna(website):  # Verificar que el sitio web no esté vacío
        print(f"Buscando correos en {website}...")
        emails = find_emails_in_website(website)
        for i, email in enumerate(emails):
            if i < 3:  # Solo los primeros tres correos
                df.at[index, f'Email {i + 1}'] = email

# Guardar los resultados en un nuevo archivo Excel
df.to_excel('hotels_hostels_emails_filtered.xlsx', index=False)
print("Correos electrónicos guardados en 'hotels_hostels_emails_filtered.xlsx'")
