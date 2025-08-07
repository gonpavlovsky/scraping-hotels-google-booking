# 🏨 Scraping de Hostels y Propiedades Turísticas desde Google Maps y Booking

Este proyecto tiene como objetivo crear una base de datos de alojamientos (hoteles, hostels, vacation rentals, property managers) en zonas turísticas específicas, combinando múltiples fuentes:

- Google Maps (via Google Places API)
- Sitios web oficiales de los alojamientos
- Booking.com

Se extrajeron datos como nombre, dirección, web, teléfono y correos electrónicos disponibles.

---

## 🌎 Localidades cubiertas

- Potrero  
- Playa Flamingo  
- Manuel Antonio  
- Monteverde  
- Sayulita  
- San Francisco  
- Puerto Vallarta  
- Entre otras

---

## 📂 Estructura del proyecto

| Carpeta | Contenido |
|--------|-----------|
| `data/` | Archivos `.csv` y `.xlsx` con los alojamientos recopilados |
| `scripts/` | Código en Python para scraping desde Booking, Google Places y extracción de emails |
| `README.md` | Este archivo con descripción del proyecto |

---

## ⚙️ Scripts incluidos

- `scraping_places_multiple.py`: consulta Google Places API por ciudad + keyword
- `extraer_emails_multiple.py`: extrae correos de los sitios web encontrados
- `booking_multiple.py`: automatiza la búsqueda de alojamientos por ciudad en Booking

Todos los scripts están escritos en Python e incluyen manejo de errores y filtros de irrelevancia.

---

## 🧠 ¿Para qué sirve este proyecto?

- Crear bases de datos comerciales con contactos reales
- Analizar la oferta de hospedaje por región
- Enriquecer información para campañas de marketing directo
- Construir herramientas de lead generation

---

## 🛠 Herramientas utilizadas

- Python + Pandas
- Google Places API
- Playwright
- Booking.com
- Regex para detección de correos
- Google Sheets

---

## ⚠️ Notas

- Todas las fuentes de datos utilizadas son públicas.
- Los correos se extrajeron únicamente de sitios oficiales disponibles.
- Las claves API fueron eliminadas por seguridad.

---
👤 Realizado por Gonzalo Pavlovsky | Febrero 2025
