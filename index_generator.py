"""
GENERADOR DE ÍNDICE HTML
=========================
Genera el archivo index.html del blog desde posts.json.
"""

import os
from config import (
    INDEX_HTML_FILE, get_template_path, INDEX_TEMPLATE_FILE,
    get_thumbnail_path, AUTHOR_NAME, BLOG_NAME, AUTHOR_BIO, 
    BLOG_DESCRIPTION, PORTFOLIO_URL, MAX_POSTS_SINGLE_COLUMN,
    POSTS_FOLDER
)
from utils import (
    load_posts_index, format_tags_small_html,
    print_success, print_error, print_info, get_all_tags, slugify
)


def generate_index_html():
    """
    Genera el archivo index.html del blog.
    Lee posts.json y crea tarjetas para cada post.
    
    Returns:
        True si éxito, False si error
    """
    try:
        # Cargar plantilla
        template_path = get_template_path(INDEX_TEMPLATE_FILE)
        
        if not os.path.exists(template_path):
            print_error(f"Plantilla no encontrada: {template_path}")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Cargar posts desde índice
        posts_index = load_posts_index()
        posts = posts_index.get("posts", [])
        
        if not posts:
            print_info("No hay posts para generar el índice")
            return False
        
        # Generar HTML de tarjetas
        posts_cards_html = _generate_posts_cards(posts)
        
        # Determinar clase de grid según número de posts
        grid_class = _get_grid_class(len(posts))
        
        # Generar nube de tags
        tag_cloud_html = _generate_tag_cloud()
        
        # Preparar reemplazos
        replacements = {
            "{author}": AUTHOR_NAME,
            "{blog_name}": BLOG_NAME,
            "{blog_description}": BLOG_DESCRIPTION,
            "{portfolio_url}": PORTFOLIO_URL,
            "{author_bio}": AUTHOR_BIO,
            "{posts_cards}": posts_cards_html,
            "{grid_class}": grid_class,
            "{tag_cloud_html}": tag_cloud_html
        }
        
        # Reemplazar placeholders
        html_content = template
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, value)
        
        # Guardar index.html
        with open(INDEX_HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print_success(f"Índice actualizado: {INDEX_HTML_FILE}")
        return True
        
    except Exception as e:
        print_error(f"Error al generar índice: {e}")
        return False


def _generate_posts_cards(posts):
    """
    Genera el HTML de todas las tarjetas de posts.
    Posts sin thumbnail se muestran sin imagen.
    
    Args:
        posts: Lista de diccionarios de posts desde posts.json
    
    Returns:
        String HTML con todas las tarjetas
    """
    cards_html = ""
    
    # Invertir orden para mostrar los más recientes primero
    posts_reversed = list(reversed(posts))
    
    for post in posts_reversed:
        cards_html += _generate_single_card(post)
    
    return cards_html


def _generate_single_card(post):
    """
    Genera el HTML de una tarjeta individual de post.
    
    Args:
        post: Diccionario con datos del post
    
    Returns:
        String HTML de la tarjeta
    """
    post_url = f"{POSTS_FOLDER}/{post['number']}-{post['slug']}.html"
    
    # Generar HTML del thumbnail solo si existe
    thumbnail_html = ""
    if post.get("thumbnail"):
        thumbnail_path = get_thumbnail_path(post["thumbnail"])
        thumbnail_html = f'''    <a href="{post_url}">
        <img src="{thumbnail_path}" alt="{post['title']}" class="post-thumbnail">
    </a>
'''
    
    # Generar HTML de tags
    tags_html = format_tags_small_html(post.get("tags", []))
    
    # Plantilla de tarjeta
    card_html = f'''                
                <article class="post-card">
{thumbnail_html}                    <div class="post-card-content">
                        <h3 class="post-card-title">
                            <a href="{post_url}">{post['title']}</a>
                        </h3>
                        <p class="post-card-excerpt">
                            {post['excerpt']}
                        </p>
                        <div class="post-card-tags">
                            {tags_html}
                        </div>
                        <a href="{post_url}" class="read-more">Read More</a>
                    </div>
                </article>
'''
    
    return card_html


def _get_grid_class(num_posts):
    """
    Determina la clase CSS del grid según número de posts.
    
    Args:
        num_posts: Número total de posts
    
    Returns:
        String con clase CSS apropiada
    """
    if num_posts <= MAX_POSTS_SINGLE_COLUMN:
        return "single-post"
    else:
        return "small-cards"


def _generate_tag_cloud():
    """
    Genera la nube de tags HTML para el índice general.
    
    Returns:
        String HTML con la nube de tags
    """
    all_tags = get_all_tags()
    
    if not all_tags:
        return ""
    
    # Calcular tamaños relativos
    max_count = max(all_tags.values())
    min_count = min(all_tags.values())
    
    tag_cloud_items = []
    
    for tag_name, count in sorted(all_tags.items()):
        tag_slug = slugify(tag_name)
        
        # Calcular tamaño (1.0 - 2.0)
        if max_count > min_count:
            size = 1.0 + (count - min_count) / (max_count - min_count)
        else:
            size = 1.5
        
        tag_url = f"tags/{tag_slug}.html"
        
        tag_cloud_items.append(
            f'<a href="{tag_url}" style="font-size: {size}em;">{tag_name}</a>'
        )
    
    return " ".join(tag_cloud_items)


def update_index():
    """
    Función wrapper para actualizar el índice.
    Útil para llamar desde otros módulos.
    
    Returns:
        True si éxito, False si error
    """
    print_info(f"Generando índice con posts desde {POSTS_FOLDER}...")
    return generate_index_html()
