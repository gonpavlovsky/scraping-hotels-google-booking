import requests
import pandas as pd
import time

API_KEY = 'TU_API_KEY_ACÁ'  # Reemplaza con tu clave de Google API

def get_places(location, radius, keyword):
    all_places = []
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={keyword}&key={API_KEY}"
    while url:
        try:
            response = requests.get(url, timeout=10)  # Agregar timeout
            if response.status_code == 200:
                data = response.json()
                places = data.get('results', [])
                all_places.extend(places)

                next_page_token = data.get('next_page_token')
                if next_page_token:
                    time.sleep(5)  # Esperar 5 segundos entre páginas
                    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={API_KEY}"
                else:
                    break
            else:
                print(f"Error: {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener lugares: {e}")
            time.sleep(5)  # Esperar antes de reintentar
    return all_places

def get_place_details(place_id):
    detail_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}"
    for _ in range(3):  # Reintentar hasta 3 veces
        try:
            response = requests.get(detail_url, timeout=10)  # Agregar timeout
            if response.status_code == 200:
                details = response.json().get('result', {})
                return {
                    'name': details.get('name'),
                    'address': details.get('formatted_address'),
                    'phone': details.get('formatted_phone_number'),
                    'website': details.get('website')
                }
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener detalles para {place_id}: {e}")
            time.sleep(5)  # Esperar antes de reintentar
    return None

def exclude_irrelevant_places(results):
    # Palabras clave que indican que un lugar es irrelevante
    exclude_keywords = ['surf', 'school', 'lessons', 'shop', 'gym', 'restaurant', 'café', 'bar', 'studio']
    filtered_results = []
    for result in results:
        name = result.get('name', '').lower()
        if not any(keyword in name for keyword in exclude_keywords):
            filtered_results.append(result)
    return filtered_results

# Lista de ubicaciones con coordenadas, radios y nombres
locations = [
    {"name": "Potrero", "location": "10.463132840989182,-85.7536355545857", "radius": 3000},
    {"name": "Playa Flamingo", "location": "10.431925,-85.785741", "radius": 2000},
    {"name": "Playa Flamingo", "location": "10.423708,-85.771704", "radius": 2000},
    {"name": "Manuel Antonio", "location": "9.406758,-84.157474", "radius": 4000},
    {"name": "Monteverde", "location": "10.307646609563927,-84.80869694520943", "radius": 8000},
    {"name": "Sayulita", "location": "20.869241859332696,-105.44075609020376", "radius": 2500},
    {"name": "San Francisco", "location": "20.908256,-105.407013", "radius": 2600},
    {"name": "Puerto Vallarta", "location": "20.648164,-105.192640", "radius": 10000}
]

# Palabras clave para buscar negocios
keywords = ['hotel', 'hostel', 'vacation rental', 'property management']
data = []

# Realizar búsquedas para cada ubicación
for loc in locations:
    for keyword in keywords:
        print(f"Buscando {keyword} en {loc['name']}...")
        places = get_places(loc['location'], loc['radius'], keyword)
        places = exclude_irrelevant_places(places)  # Filtrar negocios irrelevantes
        for place in places:
            place_id = place.get('place_id')
            time.sleep(2)  # Esperar entre solicitudes
            details = get_place_details(place_id)
            if details:
                details['city'] = loc['name']  # Etiquetar con el nombre de la ciudad
                details['type'] = keyword.capitalize()
                data.append(details)

# Guardar resultados en un único archivo Excel
df = pd.DataFrame(data)
df['Email 1'] = None  # Agregar columnas vacías para correos electrónicos
df['Email 2'] = None
df['Email 3'] = None
df.to_excel('hotels_hostels_property_management_filtered.xlsx', index=False)
print("Datos guardados exitosamente en 'hotels_hostels_property_management_filtered.xlsx'")
