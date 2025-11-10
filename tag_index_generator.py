"""
GENERADOR DE TAG-INDEXES
=========================
Genera páginas HTML individuales para cada tag del blog.
"""

import os
from config import (
    TAGS_FOLDER, get_tag_index_html_path, get_tag_index_json_path,
    get_template_path, TAG_INDEX_TEMPLATE_FILE, get_thumbnail_path,
    AUTHOR_NAME, BLOG_NAME, AUTHOR_BIO, BLOG_DESCRIPTION, 
    PORTFOLIO_URL, MAX_POSTS_SINGLE_COLUMN, INDEX_HTML_FILE
)
from utils import (
    load_posts_index, save_json, load_json, format_tags_small_html,
    print_success, print_error, print_info, slugify, get_all_tags,
    find_matching_tag
)


def generate_tag_index_html(tag_name, tag_slug, posts):
    """
    Genera el archivo HTML de un tag-index individual.
    
    Args:
        tag_name: Nombre del tag (ej: "Artificial Intelligence")
        tag_slug: Slug del tag (ej: "artificial-intelligence")
        posts: Lista de posts asociados a este tag
    
    Returns:
        True si éxito, False si error
    """
    try:
        # Cargar plantilla
        template_path = get_template_path(TAG_INDEX_TEMPLATE_FILE)
        
        if not os.path.exists(template_path):
            print_error(f"Plantilla no encontrada: {template_path}")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Generar HTML de tarjetas
        posts_cards_html = _generate_posts_cards(posts)
        
        # Determinar clase de grid según número de posts
        grid_class = _get_grid_class(len(posts))
        
        # Generar nube de tags
        tag_cloud_html = _generate_tag_cloud(tag_slug)
        
        # Preparar reemplazos
        replacements = {
            "{author}": AUTHOR_NAME,
            "{blog_name}": BLOG_NAME,
            "{blog_description}": BLOG_DESCRIPTION,
            "{portfolio_url}": PORTFOLIO_URL,
            "{author_bio}": AUTHOR_BIO,
            "{tag_name}": tag_name,
            "{posts_cards}": posts_cards_html,
            "{grid_class}": grid_class,
            "{tag_cloud_html}": tag_cloud_html,
            "{index_file}": f"../{INDEX_HTML_FILE}"
        }
        
        # Reemplazar placeholders
        html_content = template
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, value)
        
        # Guardar HTML
        html_path = get_tag_index_html_path(tag_slug)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print_success(f"Tag-index generado: {html_path}")
        return True
        
    except Exception as e:
        print_error(f"Error al generar tag-index: {e}")
        return False


def _generate_posts_cards(posts):
    """
    Genera el HTML de todas las tarjetas de posts.
    
    Args:
        posts: Lista de diccionarios de posts
    
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
    post_url = f"../posts/{post['number']}-{post['slug']}.html"
    
    # Generar HTML del thumbnail solo si existe
    thumbnail_html = ""
    if post.get("thumbnail"):
        thumbnail_path = f"../{get_thumbnail_path(post['thumbnail'])}"
        thumbnail_html = f'''    <a href="{post_url}">
        <img src="{thumbnail_path}" alt="{post['title']}" class="post-thumbnail">
    </a>
'''
    
    # Generar HTML de tags
    tags_html = format_tags_small_html(post.get("tags", []), relative_path="../")
    
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


def _generate_tag_cloud(current_tag_slug=None):
    """
    Genera la nube de tags HTML.
    
    Args:
        current_tag_slug: Slug del tag actual (se marca como activo)
    
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
        
        # Marcar tag actual
        active_class = ' class="active"' if tag_slug == current_tag_slug else ''
        
        # URL relativa
        tag_url = f"{tag_slug}.html" if current_tag_slug else f"tags/{tag_slug}.html"
        
        tag_cloud_items.append(
            f'<a href="{tag_url}" style="font-size: {size}em;"{active_class}>{tag_name}</a>'
        )
    
    return " ".join(tag_cloud_items)


def save_tag_json(tag_slug, posts):
    """
    Guarda el JSON individual de un tag.
    
    Args:
        tag_slug: Slug del tag
        posts: Lista de posts asociados
    
    Returns:
        True si éxito, False si error
    """
    tag_data = {
        "tag_slug": tag_slug,
        "posts": posts
    }
    
    json_path = get_tag_index_json_path(tag_slug)
    
    if save_json(tag_data, json_path):
        print_success(f"Tag JSON guardado: {json_path}")
        return True
    else:
        print_error(f"Error al guardar JSON del tag")
        return False


def update_tag_indexes():
    """
    Actualiza o crea todos los tag-indexes basándose en posts.json.
    
    Returns:
        True si éxito, False si error
    """
    print_info("Actualizando tag-indexes...")
    
    # Cargar índice de posts
    posts_index = load_posts_index()
    posts = posts_index.get("posts", [])
    
    if not posts:
        print_info("No hay posts para generar tag-indexes")
        return True
    
    # Agrupar posts por tag
    tags_dict = {}
    
    for post in posts:
        post_tags = post.get("tags", [])
        
        for tag in post_tags:
            # Normalizar tag (case-insensitive)
            tag_normalized = tag.strip()
            tag_slug = slugify(tag_normalized)
            
            # Buscar tag existente que coincida
            matched_tag = find_matching_tag(tag_normalized, list(tags_dict.keys()))
            
            if matched_tag:
                tag_key = matched_tag
            else:
                tag_key = tag_normalized
            
            if tag_key not in tags_dict:
                tags_dict[tag_key] = []
            
            tags_dict[tag_key].append(post)
    
    # Generar HTML y JSON para cada tag
    success_count = 0
    error_count = 0
    
    for tag_name, tag_posts in tags_dict.items():
        tag_slug = slugify(tag_name)
        
        # Guardar JSON
        if not save_tag_json(tag_slug, tag_posts):
            error_count += 1
            continue
        
        # Generar HTML
        if generate_tag_index_html(tag_name, tag_slug, tag_posts):
            success_count += 1
        else:
            error_count += 1
    
    print_success(f"Tag-indexes actualizados: {success_count} generados")
    
    if error_count > 0:
        print_error(f"{error_count} tag-indexes con errores")
    
    return error_count == 0


def regenerate_tag_indexes():
    """
    Regenera todos los tag-indexes desde los JSON existentes.
    
    Returns:
        True si éxito, False si error
    """
    print_info("Regenerando tag-indexes desde JSON...")
    
    if not os.path.exists(TAGS_FOLDER):
        print_info("No existe carpeta tags/")
        return update_tag_indexes()
    
    # Buscar todos los JSON de tags
    tag_jsons = [f for f in os.listdir(TAGS_FOLDER) if f.startswith("posts-") and f.endswith(".json")]
    
    if not tag_jsons:
        print_info("No hay tag JSONs para regenerar")
        return update_tag_indexes()
    
    success_count = 0
    error_count = 0
    
    for json_file in tag_jsons:
        json_path = os.path.join(TAGS_FOLDER, json_file)
        tag_data = load_json(json_path)
        
        if not tag_data:
            print_error(f"Error al leer JSON: {json_file}")
            error_count += 1
            continue
        
        tag_slug = tag_data.get("tag_slug")
        posts = tag_data.get("posts", [])
        
        # Inferir tag_name desde el primer post
        tag_name = tag_slug.replace("-", " ").title()
        if posts and posts[0].get("tags"):
            for tag in posts[0]["tags"]:
                if slugify(tag) == tag_slug:
                    tag_name = tag
                    break
        
        if generate_tag_index_html(tag_name, tag_slug, posts):
            success_count += 1
        else:
            error_count += 1
    
    print_success(f"Tag-indexes regenerados: {success_count}/{len(tag_jsons)}")
    
    if error_count > 0:
        print_error(f"{error_count} tag-indexes con errores")
    
    return error_count == 0
