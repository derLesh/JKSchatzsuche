# %% [markdown]
# # Google Maps URL Generator
#
# Mit diesem Notebook werden mögliche Koordinaten für die Schatzsuche generiert.
# Der Rahmen liegt bei ganz Deutschland.

# %%
# Installieren der zusätzlichen benötigten Bibliotheken für Geopandas, Matplotlib und Contextily
!pip install geopandas matplotlib contextily

# %%
# Importieren der notwendigen Bibliotheken
import itertools
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point, Polygon

# %%
# Funktion zur Erzeugung von Google Maps URLs und zur Kartenvisualisierung mit Convex Hull
def generate_google_maps_urls_and_convex_hull(breitengrad_pattern, laengengrad_pattern, breiten_range, laengen_range):
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
        formatted_breitengrad = breitengrad_pattern.format(*breiten_digit).replace(" ", "")
        breitengrad = float(formatted_breitengrad)
        if breiten_range[0] <= breitengrad <= breiten_range[1]:
            for laengen_digit in laengen_digits:
                formatted_laengengrad = laengengrad_pattern.format(*laengen_digit).replace(" ", "")
                laengengrad = float(formatted_laengengrad)
                if laengen_range[0] <= laengengrad <= laengen_range[1]:
                    urls.append(f"https://www.google.com/maps?q={breitengrad},{laengengrad}")
                    points.append(Point(laengengrad, breitengrad))

    # Erstellen eines GeoDataFrame mit den Punkten
    gdf_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")
    
    # Berechnen der Convex Hull
    convex_hull = gdf_points.unary_union.convex_hull
    
    # Umwandeln der Convex Hull in ein GeoDataFrame
    gdf_hull = gpd.GeoDataFrame(geometry=[convex_hull], crs="EPSG:4326")
    
    # Erstellen der Karte
    fig, ax = plt.subplots(figsize=(10, 10))  # Hier können Sie die Größe anpassen, um das Verhältnis zu optimieren
    gdf_hull.plot(ax=ax, alpha=0.5, edgecolor='k', color='none')
    gdf_points.plot(ax=ax, markersize=10, color='blue')

    # Hintergrundkarte hinzufügen
    ctx.add_basemap(ax, crs=gdf_points.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    # Begrenzen der Ansicht auf Deutschland
    ax.set_xlim(5.866342, 15.041896)  # Grenzen für Deutschland
    ax.set_ylim(47.270111, 55.058347)

    # Achsen ausschalten
    ax.axis('off')
    
    # Speichern der Karte als Bild
    plt.savefig('coordinates_map.png', dpi=300, bbox_inches='tight')
    
    return urls

# %%
# Eingabeaufforderung für den Benutzer
breitengrad_pattern = input("Bitte geben Sie das Muster für den Breitengrad ein (z.B. '50._7_6_'): ")
laengengrad_pattern = input("Bitte geben Sie das Muster für den Längengrad ein (z.B. '12.4_2__'): ")

# %%
# Definieren des Bereichs für Koordinaten in Deutschland
breiten_range = (47.00000, 55.99999)
laengen_range = (6.00000, 15.99999)

# %%
# Generierung und Ausgabe der URLs und Karte als Bild
urls = generate_google_maps_urls_and_convex_hull(breitengrad_pattern, laengengrad_pattern, breiten_range, laengen_range)
print(f"\nEs wurden {len(urls)} URLs generiert:\n")
for url in urls:
    print(url)
