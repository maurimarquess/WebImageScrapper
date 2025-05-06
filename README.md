# Image Web Scraper

Este script en Python permite descargar automáticamente todas las imágenes encontradas en una página web dada. Utiliza las librerías `requests` y `BeautifulSoup` para obtener y analizar el contenido HTML de la página.

## ¿Cómo funciona?

1. **Obtención del HTML**  
   El script realiza una petición HTTP a la URL proporcionada y obtiene el HTML de la página.

2. **Análisis del HTML**  
   Utiliza BeautifulSoup para buscar todas las etiquetas `<img>` en el HTML.

3. **Descarga de imágenes**  
   Para cada imagen encontrada:
   - Obtiene la URL de la imagen (atributo `src`).
   - Convierte la URL a absoluta si es necesario.
   - Descarga la imagen y la guarda en una carpeta local, organizada por dominio.

4. **Ejecución**  
   El script se ejecuta desde la línea de comandos así:
   ```
   python image_scraper.py <URL>
   ```
   Por ejemplo:
   ```
   python image_scraper.py https://ejemplo.com
   ```

## Estructura de carpetas

Las imágenes descargadas se guardan en una carpeta llamada `images`, dentro de una subcarpeta con el nombre del dominio de la web.

## Notas

- El script ignora imágenes embebidas en base64.
- Si la URL de la imagen es relativa, la convierte a absoluta.
- Si la imagen no tiene nombre, le asigna uno por defecto.
- El script solo descarga imágenes de páginas web generales, no de Instagram ni de YouTube.

--- 