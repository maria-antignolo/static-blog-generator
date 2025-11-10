"""
ACTUALIZADOR DE NAVEGACIÓN
===========================
Actualiza los enlaces prev/next en todos los posts.
"""

import os
from config import get_post_json_path
from utils import (
    load_posts_index, load_json, save_json,
    print_success, print_error, print_info, print_section
)
from post_generator import generate_post_html


def update_navigation():
    """
    Actualiza la navegación (prev/next) de todos los posts.
    Lee posts.json, actualiza cada JSON individual y regenera HTML.
    
    Returns:
        True si éxito, False si error
    """
    print_section("ACTUALIZANDO NAVEGACIÓN DE POSTS")
    
    # Cargar índice de posts
    posts_index = load_posts_index()
    posts = posts_index.get("posts", [])
    
    if not posts:
        print_info("No hay posts para actualizar navegación")
        return True
    
    print_info(f"Actualizando navegación de {len(posts)} post(s)...")
    
    # Ordenar posts por número
    posts.sort(key=lambda x: x["number"])
    
    updated_count = 0
    error_count = 0
    
    for i, post in enumerate(posts):
        # Determinar prev y next
        prev_post = None
        next_post = None
        
        if i > 0:
            prev_post = {
                "number": posts[i-1]["number"],
                "slug": posts[i-1]["slug"],
                "title": posts[i-1]["title"]
            }
        
        if i < len(posts) - 1:
            next_post = {
                "number": posts[i+1]["number"],
                "slug": posts[i+1]["slug"],
                "title": posts[i+1]["title"]
            }
        
        # Actualizar JSON individual
        if _update_post_navigation(post["number"], post["slug"], prev_post, next_post):
            updated_count += 1
            print(f"  ✓ Post {post['number']}-{post['slug']}")
        else:
            error_count += 1
            print(f"  ✗ Post {post['number']}-{post['slug']} (error)")
    
    print_success("Navegación actualizada correctamente")
    
    if error_count > 0:
        print_info(f"Posts actualizados: {updated_count}/{len(posts)}")
        return False
    
    return True


def _update_post_navigation(post_number, slug, prev_post, next_post):
    """
    Actualiza la navegación de un post específico.
    
    Args:
        post_number: Número del post
        slug: Slug del post
        prev_post: Diccionario con datos del post anterior (o None)
        next_post: Diccionario con datos del post siguiente (o None)
    
    Returns:
        True si éxito, False si error
    """
    json_path = get_post_json_path(post_number, slug)
    
    # Cargar JSON del post
    if not os.path.exists(json_path):
        print_error(f"No se encontró el JSON del post {post_number}-{slug}")
        return False
    
    post_data = load_json(json_path)
    
    if not post_data:
        print_error(f"Error al leer JSON del post {post_number}-{slug}")
        return False
    
    # Actualizar navegación
    post_data["prev_post"] = prev_post
    post_data["next_post"] = next_post
    
    # Guardar JSON actualizado
    if not save_json(post_data, json_path):
        return False
    
    # Regenerar HTML con nueva navegación
    if not generate_post_html(post_data):
        return False
    
    return True


def update_single_post_navigation(post_number, slug):
    """
    Actualiza la navegación de un solo post específico.
    Útil cuando se añade o elimina un post adyacente.
    
    Args:
        post_number: Número del post a actualizar
        slug: Slug del post
    
    Returns:
        True si éxito, False si error
    """
    posts_index = load_posts_index()
    posts = posts_index.get("posts", [])
    
    # Buscar el post
    post_index = None
    for i, post in enumerate(posts):
        if post["number"] == post_number:
            post_index = i
            break
    
    if post_index is None:
        print_error(f"Post {post_number} no encontrado en posts.json")
        return False
    
    # Determinar prev y next
    prev_post = None
    next_post = None
    
    if post_index > 0:
        prev_post = {
            "number": posts[post_index-1]["number"],
            "slug": posts[post_index-1]["slug"],
            "title": posts[post_index-1]["title"]
        }
    
    if post_index < len(posts) - 1:
        next_post = {
            "number": posts[post_index+1]["number"],
            "slug": posts[post_index+1]["slug"],
            "title": posts[post_index+1]["title"]
        }
    
    return _update_post_navigation(post_number, slug, prev_post, next_post)
