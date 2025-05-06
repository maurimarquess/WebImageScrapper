import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import sys
import instaloader
import re
import getpass

def get_domain_name(url):
    """Extrae el nombre del dominio de una URL"""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Eliminar www. si existe
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def extract_images_from_metadata(soup):
    """Extrae URLs de imágenes de los metadatos (og:image, twitter:image, etc.)"""
    image_urls = set()
    # Buscar metadatos comunes de imágenes
    for prop in ['og:image', 'twitter:image', 'og:image:url']:
        tag = soup.find('meta', property=prop) or soup.find('meta', attrs={'name': prop})
        if tag and tag.get('content'):
            image_urls.add(tag['content'])
    return list(image_urls)

def scrape_images(url, base_output_dir='images'):
    # Obtener el nombre del dominio
    domain = get_domain_name(url)
    
    # Crear la ruta completa del directorio de salida
    output_dir = os.path.join(base_output_dir, domain)
    
    # Crear directorios si no existen
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Obtener el contenido de la página
        response = requests.get(url)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar todas las etiquetas img
        img_tags = soup.find_all('img')
        
        # Contador de imágenes descargadas
        count = 0
        
        for img in img_tags:
            # Obtener la URL de la imagen
            img_url = img.get('src')
            if img_url:
                # Convertir URL relativa a absoluta si es necesario
                img_url = urljoin(url, img_url)
                
                try:
                    # Obtener la imagen
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()
                    
                    # Generar nombre de archivo
                    filename = os.path.join(output_dir, f'imagen_{count}.jpg')
                    
                    # Guardar la imagen
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
                    
                    print(f'Imagen guardada: {filename}')
                    count += 1
                    
                except Exception as e:
                    print(f'Error al descargar {img_url}: {str(e)}')
        
        print(f'\nTotal de imágenes descargadas: {count}')
        
    except Exception as e:
        print(f'Error: {str(e)}')

def download_images(url):
    if not os.path.exists('images'):
        os.makedirs('images')
    domain = urlparse(url).netloc.replace('www.', '')
    domain_folder = os.path.join('images', domain)
    if not os.path.exists(domain_folder):
        os.makedirs(domain_folder)
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        downloaded = 0
        for img in images:
            try:
                img_url = img.get('src')
                if not img_url:
                    continue
                if img_url.startswith('/'):
                    img_url = f"https://{domain}{img_url}"
                elif not img_url.startswith(('http://', 'https://')):
                    img_url = f"https://{domain}/{img_url}"
                if img_url.startswith('data:'):
                    continue
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    filename = os.path.basename(img_url)
                    if not filename:
                        filename = f"image_{downloaded + 1}.jpg"
                    filepath = os.path.join(domain_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Imagen descargada: {filename} ({len(img_response.content)} bytes)")
                    downloaded += 1
            except Exception as e:
                print(f"Error al descargar imagen: {str(e)}")
        print(f"\nTotal de imágenes descargadas: {downloaded}")
    except Exception as e:
        print(f"Error al descargar data: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python image_scraper.py <URL>')
        sys.exit(1)
    url = sys.argv[1]
    download_images(url) 