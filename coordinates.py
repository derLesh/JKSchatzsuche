# %%
# Installieren der benötigten Bibliotheken für folium
# !pip install folium branca

# %%
# Importieren der notwendigen Bibliotheken
import itertools
import folium
import branca
import os
# from shapely.geometry import Point
# from IPython.display import display

# %%
# Funktion zur Erzeugung von Google Maps URLs und zur Kartenvisualisierung mit folium
def generate_google_maps_urls_and_folium_map(breitengrad_pattern, laengengrad_pattern, breiten_range, laengen_range):
    urls = []
    points = []

    # Ersetze Unterstriche mit Platzhalter für Ziffern
    breitengrad_pattern = breitengrad_pattern.replace("_", "{}")
    laengengrad_pattern = laengengrad_pattern.replace("_", "{}")
    
    # Generiere alle möglichen Zahlen für die Platzhalter
    breiten_digits = itertools.product(range(10), repeat=breitengrad_pattern.count("{}"))
    laengen_digits = list(itertools.product(range(10), repeat=laengengrad_pattern.count("{}")))
    
    # Erstelle alle möglichen Koordinaten innerhalb des vorgegebenen Rahmens
    for breiten_digit in breiten_digits:
        for laengen_digit in laengen_digits:
            breitengrad = float(breitengrad_pattern.format(*breiten_digit))
            laengengrad = float(laengengrad_pattern.format(*laengen_digit))
            if breiten_range[0] <= breitengrad <= breiten_range[1] and laengen_range[0] <= laengengrad <= laengen_range[1]:
                urls.append(f"https://www.google.com/maps?q={breitengrad},{laengengrad}")
                points.append((breitengrad, laengengrad))

    # Erstellen der Folium-Karte
    mittlerer_breitengrad = sum(breiten_range) / 2
    mittlerer_laengengrad = sum(laengen_range) / 2
    m = folium.Map(location=[mittlerer_breitengrad, mittlerer_laengengrad], zoom_start=6)

    # Hinzufügen der Marker zur Karte
    for point in points:
        folium.Marker(point).add_to(m)

    # Karte anzeigen
    m.save("coordinates.html")

    return urls

# %%
# Eingabeaufforderung für den Benutzer
breitengrad_pattern = os.getenv('BREITENGRAD_PATTERN')
if not breitengrad_pattern:
    breitengrad_pattern = input("Bitte geben Sie das Muster für den Breitengrad ein (z.B. '50._7_6_'): ")

laengengrad_pattern = os.getenv('LAENGENGRAD_PATTERN')
if not laengengrad_pattern:
    laengengrad_pattern = input("Bitte geben Sie das Muster für den Längengrad ein (z.B. '12.4_2__'): ")

# %%
# Definieren des Bereichs für Koordinaten in Deutschland
breiten_range = (47.00000, 55.99999)
laengen_range = (6.00000, 15.99999)

# %%
# Generierung und Ausgabe der URLs und Anzeigen der Karte
urls = generate_google_maps_urls_and_folium_map(breitengrad_pattern, laengengrad_pattern, breiten_range, laengen_range)
print(f"\nEs wurden {len(urls)} URLs generiert:\n")
for url in urls:
    print(url)
