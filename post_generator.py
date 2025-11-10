"""
GENERADOR DE POSTS HTML
========================
Genera archivos HTML de posts individuales desde datos JSON.
"""

import os
from config import (
    get_post_html_path, get_post_json_path, get_template_path,
    get_thumbnail_path, get_featured_image_path,
    POST_TEMPLATE_FILE, INDEX_HTML_FILE,
    AUTHOR_NAME, AUTHOR_BIO
)
from utils import (
    save_json, load_json, format_tags_html,
    validate_image, print_success, print_error, print_info
)


def generate_post_html(post_data):
    """
    Genera el archivo HTML de un post individual.
    
    Args:
        post_data: Diccionario con datos del post (debe incluir number, slug, etc.)
    
    Returns:
        True si éxito, False si error
    """
    try:
        # Cargar plantilla
        template_path = get_template_path(POST_TEMPLATE_FILE)
        
        if not os.path.exists(template_path):
            print_error(f"Plantilla no encontrada: {template_path}")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Validar imágenes si existen
        if post_data.get("thumbnail"):
            thumb_path = get_thumbnail_path(post_data["thumbnail"])
            validate_image(thumb_path, "Thumbnail")
        
        if post_data.get("featured_image"):
            featured_path = get_featured_image_path(post_data["featured_image"])
            validate_image(featured_path, "Imagen destacada")
        
        # Preparar datos para reemplazo
        replacements = {
            "{title}": post_data["title"],
            "{excerpt}": post_data["excerpt"],
            "{author}": AUTHOR_NAME,
            "{author_bio}": AUTHOR_BIO,
            "{content}": post_data["content"],
            "{read_time}": str(post_data["read_time"]),
            "{index_file}": INDEX_HTML_FILE,
            "{tags_html}": format_tags_html(post_data.get("tags", []), relative_path="../"),
            "{featured_image_html}": _generate_featured_image_html(post_data),
            "{navigation_html}": _generate_navigation_html(post_data)
        }
        
        # Reemplazar placeholders
        html_content = template
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, value)
        
        # Guardar HTML
        html_path = get_post_html_path(post_data["number"], post_data["slug"])
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print_success(f"Post HTML generado: {html_path}")
        return True
        
    except Exception as e:
        print_error(f"Error al generar HTML del post: {e}")
        return False


def _generate_featured_image_html(post_data):
    """
    Genera el HTML de la imagen destacada.
    Si no hay imagen, retorna string vacío.
    """
    featured_image = post_data.get("featured_image")
    
    if not featured_image:
        return ""
    
    image_path = get_featured_image_path(featured_image)
    # Path relativo desde posts/ hacia assets/
    relative_path = f"../{image_path}"
    
    return f'<img src="{relative_path}" alt="{post_data["title"]}" class="featured-image">'


def _generate_navigation_html(post_data):
    """
    Genera el HTML de navegación prev/next.
    Si no hay navegación, retorna string vacío.
    """
    prev_post = post_data.get("prev_post")
    next_post = post_data.get("next_post")
    
    if not prev_post and not next_post:
        return ""
    
    nav_html = '<div class="post-navigation">\n'
    
    # Enlace anterior
    if prev_post:
        nav_html += f'''                <a href="{prev_post['number']}-{prev_post['slug']}.html" class="nav-link prev-link">
                    <span class="nav-label">← Previous Post</span>
                    <span class="nav-title">{prev_post['title']}</span>
                </a>\n'''
    else:
        nav_html += '                <div></div>\n'
    
    # Enlace siguiente
    if next_post:
        nav_html += f'''                <a href="{next_post['number']}-{next_post['slug']}.html" class="nav-link next-link">
                    <span class="nav-label">Next Post →</span>
                    <span class="nav-title">{next_post['title']}</span>
                </a>\n'''
    
    nav_html += '            </div>\n            <!-- .post-navigation -->'
    
    return nav_html


def save_post_json(post_data):
    """
    Guarda el JSON individual del post en posts/.
    
    Args:
        post_data: Diccionario completo del post
    
    Returns:
        True si éxito, False si error
    """
    json_path = get_post_json_path(post_data["number"], post_data["slug"])
    
    if save_json(post_data, json_path):
        print_success(f"Post JSON guardado: {json_path}")
        return True
    else:
        print_error(f"Error al guardar JSON del post")
        return False


def create_post(post_input, auto_number=True, auto_slug=True):
    """
    Crea un nuevo post completo: JSON individual + HTML.
    
    Args:
        post_input: Diccionario con datos del post
        auto_number: Si True, asigna número automáticamente
        auto_slug: Si True, genera slug desde título si no existe
    
    Returns:
        post_data completo si éxito, None si error
    """
    from utils import get_next_post_number, slugify, validate_post_data, add_post_to_index
    
    # Validar datos básicos
    is_valid, error_msg = validate_post_data(post_input)
    if not is_valid:
        print_error(error_msg)
        return None
    
    # Asignar número si es automático
    if auto_number or "number" not in post_input:
        post_input["number"] = get_next_post_number()
    
    # Generar slug si es automático
    if auto_slug or "slug" not in post_input:
        post_input["slug"] = slugify(post_input["title"])
    
    # Estructura completa del post
    post_data = {
        "number": post_input["number"],
        "slug": post_input["slug"],
        "title": post_input["title"],
        "excerpt": post_input["excerpt"],
        "tags": post_input["tags"],
        "read_time": post_input["read_time"],
        "thumbnail": post_input.get("thumbnail"),
        "featured_image": post_input.get("featured_image"),
        "content": post_input["content"],
        "prev_post": None,  # Se actualizará después
        "next_post": None   # Se actualizará después
    }
    
    # Guardar JSON individual
    if not save_post_json(post_data):
        return None
    
    # Generar HTML
    if not generate_post_html(post_data):
        return None
    
    # Añadir al índice maestro
    if not add_post_to_index(post_data):
        print_error("Error al actualizar posts.json")
        return None
    
    print_success(f"Post #{post_data['number']} creado exitosamente")
    return post_data


def regenerate_post_from_json(post_number, slug):
    """
    Regenera el HTML de un post desde su JSON individual.
    Usado para actualizar el HTML cuando cambian las plantillas.
    
    Args:
        post_number: Número del post
        slug: Slug del post
    
    Returns:
        True si éxito, False si error
    """
    json_path = get_post_json_path(post_number, slug)
    
    if not os.path.exists(json_path):
        print_error(f"JSON no encontrado: {json_path}")
        return False
    
    post_data = load_json(json_path)
    
    if not post_data:
        print_error(f"Error al leer JSON: {json_path}")
        return False
    
    return generate_post_html(post_data)
