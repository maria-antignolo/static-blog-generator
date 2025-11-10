"""
UTILIDADES COMPARTIDAS
======================
Funciones auxiliares usadas por todos los módulos.
"""

import os
import json
import re
import unicodedata
from config import POSTS_INDEX_FILE, POSTS_FOLDER, VALIDATE_IMAGES, ALLOW_MISSING_IMAGES


# ============================================================================
# MANEJO DE JSON
# ============================================================================

def load_json(file_path):
    """
    Carga un archivo JSON.
    Retorna dict si éxito, None si error.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print_error(f"Error al parsear JSON {file_path}: {e}")
        return None
    except Exception as e:
        print_error(f"Error al leer JSON {file_path}: {e}")
        return None


def save_json(data, file_path):
    """
    Guarda datos en un archivo JSON con formato bonito.
    Retorna True si éxito, False si error.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print_error(f"Error al guardar JSON {file_path}: {e}")
        return False


def load_posts_index():
    """
    Carga posts.json (índice maestro).
    Si no existe, lo crea vacío.
    Retorna dict con estructura {"posts": []}
    """
    if not os.path.exists(POSTS_INDEX_FILE):
        # Crear índice vacío
        empty_index = {"posts": []}
        save_json(empty_index, POSTS_INDEX_FILE)
        print_info(f"Creado índice vacío: {POSTS_INDEX_FILE}")
        return empty_index
    
    posts_index = load_json(POSTS_INDEX_FILE)
    
    if posts_index is None:
        print_error(f"Error al cargar {POSTS_INDEX_FILE}")
        return {"posts": []}
    
    return posts_index


# ============================================================================
# MANEJO DE POSTS
# ============================================================================

def get_next_post_number():
    """
    Obtiene el siguiente número de post disponible.
    Lee posts.json y retorna max(number) + 1.
    """
    posts_index = load_posts_index()
    posts = posts_index.get("posts", [])
    
    if not posts:
        return 1
    
    max_number = max(post["number"] for post in posts)
    return max_number + 1


def add_post_to_index(post_data):
    """
    Añade un post al índice maestro posts.json.
    
    Args:
        post_data: Diccionario con datos del post
    
    Returns:
        True si éxito, False si error
    """
    posts_index = load_posts_index()
    
    # Crear entrada simplificada para el índice
    index_entry = {
        "number": post_data["number"],
        "slug": post_data["slug"],
        "title": post_data["title"],
        "excerpt": post_data["excerpt"],
        "tags": post_data["tags"],
        "read_time": post_data["read_time"],
        "thumbnail": post_data.get("thumbnail"),
        "featured_image": post_data.get("featured_image")
    }
    
    # Verificar si ya existe
    existing = next(
        (p for p in posts_index["posts"] if p["number"] == post_data["number"]),
        None
    )
    
    if existing:
        # Actualizar existente
        posts_index["posts"] = [
            index_entry if p["number"] == post_data["number"] else p
            for p in posts_index["posts"]
        ]
        print_info(f"Post #{post_data['number']} actualizado en índice")
    else:
        # Añadir nuevo
        posts_index["posts"].append(index_entry)
        print_info(f"Post #{post_data['number']} añadido al índice")
    
    # Ordenar por número
    posts_index["posts"].sort(key=lambda x: x["number"])
    
    return save_json(posts_index, POSTS_INDEX_FILE)


# ============================================================================
# GENERACIÓN DE SLUGS
# ============================================================================

def slugify(text):
    """
    Convierte texto a slug URL-friendly.
    
    Args:
        text: Texto a convertir
    
    Returns:
        Slug en minúsculas con guiones
    
    Ejemplos:
        "Artificial Intelligence" -> "artificial-intelligence"
        "¿Cómo está?" -> "como-esta"
    """
    # Normalizar unicode (eliminar acentos)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Convertir a minúsculas
    text = text.lower()
    
    # Reemplazar espacios y caracteres especiales por guiones
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    # Eliminar guiones al inicio/final
    text = text.strip('-')
    
    return text


# ============================================================================
# TAGS
# ============================================================================

def get_all_tags():
    """
    Obtiene todos los tags únicos del blog con su contador.
    
    Returns:
        Dict {tag_name: count}
    """
    posts_index = load_posts_index()
    posts = posts_index.get("posts", [])
    
    tags_count = {}
    
    for post in posts:
        post_tags = post.get("tags", [])
        
        for tag in post_tags:
            tag_normalized = tag.strip()
            
            # Buscar tag existente que coincida
            matched_tag = find_matching_tag(tag_normalized, list(tags_count.keys()))
            
            if matched_tag:
                tags_count[matched_tag] += 1
            else:
                tags_count[tag_normalized] = 1
    
    return tags_count


def find_matching_tag(new_tag, existing_tags):
    """
    Busca un tag existente que coincida con el nuevo tag.
    Matching: case-insensitive, si comparten al menos una palabra.
    
    Args:
        new_tag: Tag nuevo a buscar
        existing_tags: Lista de tags existentes
    
    Returns:
        Tag existente que coincide, o None si no hay coincidencia
    
    Ejemplos:
        new_tag="Intelligence", existing=["Artificial Intelligence"] -> "Artificial Intelligence"
        new_tag="AI Tech", existing=["AI"] -> "AI"
        new_tag="Machine Learning", existing=["AI"] -> None
    """
    new_words = set(new_tag.lower().split())
    
    for existing_tag in existing_tags:
        existing_words = set(existing_tag.lower().split())
        
        # Si comparten al menos una palabra
        if new_words & existing_words:
            return existing_tag
    
    return None


# ============================================================================
# FORMATEO HTML
# ============================================================================

def format_tags_html(tags, relative_path=""):
    """
    Formatea una lista de tags como HTML para posts individuales.
    
    Args:
        tags: Lista de strings con los tags
        relative_path: Path relativo para enlaces (ej: "../" desde posts/)
    
    Returns:
        String HTML con spans de tags enlazados
    """
    if not tags:
        return ""
    
    tags_html = []
    
    for tag in tags:
        tag_slug = slugify(tag)
        tag_url = f"{relative_path}tags/{tag_slug}.html"
        tags_html.append(f'<span class="tag"><a href="{tag_url}">{tag}</a></span>')
    
    return "\n                ".join(tags_html)


def format_tags_small_html(tags, relative_path=""):
    """
    Formatea tags para tarjetas pequeñas (index, tag-indexes).
    
    Args:
        tags: Lista de strings con los tags
        relative_path: Path relativo para enlaces
    
    Returns:
        String HTML con enlaces de tags
    """
    if not tags:
        return ""
    
    tags_html = []
    
    for tag in tags:
        tag_slug = slugify(tag)
        tag_url = f"{relative_path}tags/{tag_slug}.html"
        tags_html.append(f'<a href="{tag_url}" class="tag-link">{tag}</a>')
    
    return " ".join(tags_html)


# ============================================================================
# VALIDACIÓN
# ============================================================================

def validate_post_data(post_data):
    """
    Valida que los datos del post sean correctos.
    
    Args:
        post_data: Diccionario con datos del post
    
    Returns:
        (is_valid: bool, error_msg: str)
    """
    required_fields = ["title", "excerpt", "tags", "read_time", "content"]
    
    for field in required_fields:
        if field not in post_data or not post_data[field]:
            return False, f"Campo obligatorio faltante: {field}"
    
    if not isinstance(post_data["tags"], list) or len(post_data["tags"]) == 0:
        return False, "El campo 'tags' debe ser una lista con al menos un tag"
    
    return True, ""


def validate_image(image_path, image_type="Imagen"):
    """
    Valida que una imagen exista.
    Si VALIDATE_IMAGES=False, no hace nada.
    Si ALLOW_MISSING_IMAGES=True, solo advierte.
    Si ALLOW_MISSING_IMAGES=False, detiene el programa.
    
    Args:
        image_path: Path a la imagen
        image_type: Tipo de imagen (para mensaje)
    """
    if not VALIDATE_IMAGES:
        return
    
    if not os.path.exists(image_path):
        msg = f"{image_type} no encontrada: {image_path}"
        
        if ALLOW_MISSING_IMAGES:
            print_warning(msg)
        else:
            print_error(msg)
            raise FileNotFoundError(msg)


# ============================================================================
# MENSAJES FORMATEADOS
# ============================================================================

def print_section(title):
    """Imprime un título de sección"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_success(message):
    """Imprime mensaje de éxito (verde)"""
    print(f"✅ {message}")


def print_error(message):
    """Imprime mensaje de error (rojo)"""
    print(f"❌ {message}")


def print_warning(message):
    """Imprime mensaje de advertencia (amarillo)"""
    print(f"⚠️  {message}")


def print_info(message):
    """Imprime mensaje informativo (azul)"""
    print(f"ℹ️  {message}")
