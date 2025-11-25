#!/usr/bin/env python3
"""
Script para generar todos los iconos necesarios para PWA desde ahorify_logo.png
"""

from PIL import Image
import os

# Rutas
SOURCE_LOGO = 'backend/static/ahorify_logo.png'
OUTPUT_DIR = 'frontend/public'

# Tamaños necesarios
ICON_SIZES = {
    # Favicon sizes
    'favicon-16x16.png': (16, 16),
    'favicon-32x32.png': (32, 32),
    'favicon-48x48.png': (48, 48),
    
    # Apple Touch Icon
    'apple-touch-icon.png': (180, 180),
    
    # PWA Icons
    'icon-192x192.png': (192, 192),
    'icon-512x512.png': (512, 512),
    
    # Maskable icon (512x512 con padding seguro para Android)
    'icon-maskable-512x512.png': (512, 512),
    
    # Windows Tile (opcional)
    'mstile-310x310.png': (310, 310),
}

def generate_icons():
    """Genera todos los iconos desde el logo original"""
    
    # Verificar que existe el logo original
    if not os.path.exists(SOURCE_LOGO):
        print(f"❌ Error: No se encuentra {SOURCE_LOGO}")
        return False
    
    # Crear directorio de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Abrir imagen original
    try:
        original = Image.open(SOURCE_LOGO)
        print(f"✅ Logo original cargado: {original.size[0]}x{original.size[1]}")
    except Exception as e:
        print(f"❌ Error abriendo logo: {e}")
        return False
    
    # Generar cada icono
    for filename, size in ICON_SIZES.items():
        try:
            # Para maskable icon, necesitamos agregar padding seguro (80% del tamaño)
            if 'maskable' in filename:
                # Crear imagen con padding: el icono ocupa 80% del espacio
                maskable_size = size[0]
                icon_size = int(maskable_size * 0.8)  # 80% del tamaño
                padding = (maskable_size - icon_size) // 2
                
                # Crear imagen en blanco
                maskable_img = Image.new('RGBA', (maskable_size, maskable_size), (0, 0, 0, 0))
                
                # Redimensionar logo
                resized = original.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                
                # Pegar en el centro
                maskable_img.paste(resized, (padding, padding), resized if resized.mode == 'RGBA' else None)
                
                output_path = os.path.join(OUTPUT_DIR, filename)
                maskable_img.save(output_path, 'PNG', optimize=True)
                print(f"✅ Generado: {filename} ({maskable_size}x{maskable_size} con padding)")
            else:
                # Redimensionar normalmente
                resized = original.resize(size, Image.Resampling.LANCZOS)
                output_path = os.path.join(OUTPUT_DIR, filename)
                resized.save(output_path, 'PNG', optimize=True)
                print(f"✅ Generado: {filename} ({size[0]}x{size[1]})")
                
        except Exception as e:
            print(f"❌ Error generando {filename}: {e}")
            return False
    
    # Generar favicon.ico (multi-resolución)
    try:
        # Crear lista de tamaños para favicon.ico
        favicon_sizes = [(16, 16), (32, 32), (48, 48)]
        favicon_images = []
        
        for size in favicon_sizes:
            resized = original.resize(size, Image.Resampling.LANCZOS)
            # Convertir a RGB si es necesario (ICO no soporta transparencia completa)
            if resized.mode == 'RGBA':
                # Crear fondo blanco
                rgb_img = Image.new('RGB', size, (255, 255, 255))
                rgb_img.paste(resized, mask=resized.split()[3])  # Usar canal alpha como mask
                favicon_images.append(rgb_img)
            else:
                favicon_images.append(resized.convert('RGB'))
        
        # Guardar como ICO (PIL puede guardar múltiples tamaños en un ICO)
        favicon_path = os.path.join(OUTPUT_DIR, 'favicon.ico')
        favicon_images[0].save(favicon_path, format='ICO', sizes=[(s[0], s[1]) for s in favicon_sizes])
        print(f"✅ Generado: favicon.ico (multi-resolución: {', '.join([f'{s[0]}x{s[1]}' for s in favicon_sizes])})")
        
    except Exception as e:
        print(f"⚠️  No se pudo generar favicon.ico: {e}")
        print("   (Se usarán los favicon PNG individuales)")
    
    print("\n✅ ¡Todos los iconos generados correctamente!")
    return True

if __name__ == "__main__":
    generate_icons()

