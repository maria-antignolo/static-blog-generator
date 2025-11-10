#!/usr/bin/env python3
"""
BLOG MANAGER - SISTEMA DE GESTIÓN DE BLOG ESTÁTICO
===================================================
Sistema robusto y modular para gestionar un blog estático.

Uso:
    python blog_manager.py                    # Menú interactivo
    python blog_manager.py --new-post         # Crear post modo guiado
    python blog_manager.py --from-json FILE   # Crear post desde JSON
    python blog_manager.py --update-index     # Actualizar índice
    python blog_manager.py --update-nav       # Actualizar navegación
    python blog_manager.py --regenerate       # Regenerar todo el blog
    python blog_manager.py --regenerate-tags  # Regenerar tag-indexes
"""

import sys
import argparse
from config import validate_config, print_system_info
from utils import (
    load_json, print_section, print_success, print_error, 
    print_info, slugify, load_posts_index
)
from post_generator import create_post, regenerate_post_from_json
from index_generator import update_index
from navigation_updater import update_navigation
from tag_index_generator import update_tag_indexes, regenerate_tag_indexes


# ============================================================================
# CREACIÓN DE POSTS
# ============================================================================

def create_post_interactive():
    """
    Crea un post en modo guiado interactivo.
    Pide datos al usuario paso a paso.
    """
    print_section("CREAR NUEVO POST - MODO GUIADO")
    
    print("\nℹ️  Ingresa los datos del post. Los campos marcados con * son obligatorios.\n")
    
    try:
        # Recopilar datos
        title = input("Título del post *: ").strip()
        if not title:
            print_error("El título no puede estar vacío")
            return False
        
        # Sugerir slug
        suggested_slug = slugify(title)
        slug_input = input(f"Slug (URL) [{suggested_slug}]: ").strip()
        slug = slug_input if slug_input else suggested_slug
        
        excerpt = input("Extracto (resumen para índice) *: ").strip()
        if not excerpt:
            print_error("El extracto no puede estar vacío")
            return False
        
        tags_input = input("Tags (separados por comas) *: ").strip()
        if not tags_input:
            print_error("Debes ingresar al menos un tag")
            return False
        tags = [tag.strip() for tag in tags_input.split(",")]
        
        read_time = input("Tiempo de lectura (minutos) [5]: ").strip()
        read_time = read_time if read_time else "5"
        
        thumbnail = input("Nombre del thumbnail (o Enter si no hay): ").strip()
        thumbnail = thumbnail if thumbnail else None
        
        featured_image = input("Nombre de imagen destacada (o Enter si no hay): ").strip()
        featured_image = featured_image if featured_image else None
        
        print("\nℹ️  Ingresa el contenido HTML del post.")
        print("   Puedes pegar HTML multilínea.")
        print("   Escribe 'END' en una línea sola para terminar.\n")
        
        content_lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines).strip()
        
        if not content:
            print_error("El contenido no puede estar vacío")
            return False
        
        # Crear estructura del post
        post_input = {
            "title": title,
            "slug": slug,
            "excerpt": excerpt,
            "tags": tags,
            "read_time": read_time,
            "thumbnail": thumbnail,
            "featured_image": featured_image,
            "content": content
        }
        
        # Crear post
        post_data = create_post(post_input)
        
        if not post_data:
            return False
        
        # Actualizar índice
        print_section("ACTUALIZANDO ÍNDICE DEL BLOG")
        if not update_index():
            print_error("Error al actualizar índice")
            return False
        
        # Actualizar tag-indexes
        print_section("ACTUALIZANDO TAG-INDEXES")
        if not update_tag_indexes():
            print_error("Error al actualizar tag-indexes")
            return False
        
        # Actualizar navegación
        if not update_navigation():
            print_error("Error al actualizar navegación")
            return False
        
        print_section("POST CREADO EXITOSAMENTE")
        print(f"  Post #{post_data['number']}: {post_data['title']}")
        print(f"  URL: posts/{post_data['number']}-{post_data['slug']}.html")
        print()
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Creación cancelada por el usuario")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False


def create_post_from_json(json_file):
    """
    Crea un post desde un archivo JSON.
    
    Args:
        json_file: Path al archivo JSON con datos del post
    
    Returns:
        True si éxito, False si error
    """
    print_section("CREAR POST DESDE JSON")
    
    post_input = load_json(json_file)
    
    if not post_input:
        print_error(f"No se pudo leer el archivo JSON: {json_file}")
        return False
    
    # Crear post
    post_data = create_post(post_input)
    
    if not post_data:
        return False
    
    # Actualizar índice
    print_section("ACTUALIZANDO ÍNDICE DEL BLOG")
    if not update_index():
        print_error("Error al actualizar índice")
        return False
    
    # Actualizar tag-indexes
    print_section("ACTUALIZANDO TAG-INDEXES")
    if not update_tag_indexes():
        print_error("Error al actualizar tag-indexes")
        return False
    
    # Actualizar navegación
    if not update_navigation():
        print_error("Error al actualizar navegación")
        return False
    
    print_section("POST CREADO EXITOSAMENTE")
    print(f"  Post #{post_data['number']}: {post_data['title']}")
    print(f"  URL: posts/{post_data['number']}-{post_data['slug']}.html")
    print()
    
    return True


# ============================================================================
# REGENERACIÓN COMPLETA
# ============================================================================

def regenerate_blog():
    """
    Regenera todo el blog desde los JSON existentes.
    Útil cuando se cambian las plantillas HTML.
    """
    print_section("REGENERANDO TODO EL BLOG")
    
    # Cargar índice de posts
    posts_index = load_posts_index()
    posts = posts_index.get("posts", [])
    
    if not posts:
        print_info("No hay posts para regenerar")
        return True
    
    print_info("Regenerando posts...")
    
    updated_count = 0
    error_count = 0
    
    for post in posts:
        if regenerate_post_from_json(post["number"], post["slug"]):
            updated_count += 1
        else:
            error_count += 1
            print_error(f"No se encontró JSON para {post['number']}-{post['slug']}, omitiendo...")
    
    # Actualizar índice
    print_section("ACTUALIZANDO ÍNDICE DEL BLOG")
    print_info(f"Generando índice con {len(posts)} post(s)...")
    if not update_index():
        print_error("Error al actualizar índice")
        return False
    
    # Actualizar tag-indexes
    print_section("ACTUALIZANDO TAG-INDEXES")
    if not update_tag_indexes():
        print_error("Error al actualizar tag-indexes")
        return False
    
    # Actualizar navegación
    if not update_navigation():
        print_error("Error al actualizar navegación")
        return False
    
    print_section("REGENERACIÓN COMPLETADA")
    print(f"✅ Blog regenerado: {updated_count}/{len(posts)} posts actualizados")
    
    if error_count > 0:
        print_info(f"⚠️  {error_count} post(s) no pudieron regenerarse (JSON no encontrado)")
    
    print()
    
    return True


# ============================================================================
# MENÚ INTERACTIVO
# ============================================================================

def show_menu():
    """Muestra el menú principal"""
    print("\n" + "="*70)
    print("  MENÚ PRINCIPAL")
    print("="*70)
    print("\n1. Crear nuevo post (modo guiado)")
    print("2. Actualizar índice del blog")
    print("3. Actualizar navegación de posts")
    print("4. Regenerar todo el blog")
    print("5. Regenerar tag-indexes")
    print("6. Salir\n")


def interactive_menu():
    """Ejecuta el menú interactivo"""
    while True:
        show_menu()
        
        try:
            choice = input("Selecciona una opción [1-6]: ").strip()
            
            if choice == "1":
                create_post_interactive()
            elif choice == "2":
                print_section("ACTUALIZANDO ÍNDICE DEL BLOG")
                update_index()
            elif choice == "3":
                update_navigation()
            elif choice == "4":
                regenerate_blog()
            elif choice == "5":
                print_section("REGENERANDO TAG-INDEXES")
                regenerate_tag_indexes()
            elif choice == "6":
                print("\n👋 ¡Hasta pronto!\n")
                sys.exit(0)
            else:
                print_error("Opción inválida. Selecciona un número entre 1 y 6.")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto!\n")
            sys.exit(0)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal del programa"""
    
    # Mostrar info del sistema
    print_system_info()
    
    # Validar configuración
    if not validate_config():
        print_error("Error en la configuración. Revisa config.py")
        sys.exit(1)
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(
        description="Sistema de gestión de blog estático",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--new-post",
        action="store_true",
        help="Crear nuevo post en modo guiado"
    )
    
    parser.add_argument(
        "--from-json",
        metavar="FILE",
        help="Crear post desde archivo JSON"
    )
    
    parser.add_argument(
        "--update-index",
        action="store_true",
        help="Actualizar índice del blog"
    )
    
    parser.add_argument(
        "--update-nav",
        action="store_true",
        help="Actualizar navegación de posts"
    )
    
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Regenerar todo el blog desde JSONs"
    )
    
    parser.add_argument(
        "--regenerate-tags",
        action="store_true",
        help="Regenerar todos los tag-indexes"
    )
    
    args = parser.parse_args()
    
    # Ejecutar según argumentos
    if args.new_post:
        create_post_interactive()
    elif args.from_json:
        create_post_from_json(args.from_json)
    elif args.update_index:
        print_section("ACTUALIZANDO ÍNDICE DEL BLOG")
        update_index()
    elif args.update_nav:
        update_navigation()
    elif args.regenerate:
        regenerate_blog()
    elif args.regenerate_tags:
        print_section("REGENERANDO TAG-INDEXES")
        regenerate_tag_indexes()
    else:
        # Sin argumentos: mostrar menú interactivo
        interactive_menu()


if __name__ == "__main__":
    main()
