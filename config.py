"""
CONFIGURACIÓN DEL SISTEMA DE BLOG ESTÁTICO
===========================================
Configuración centralizada y robusta para el gestor de blog.
Todos los paths son relativos al directorio donde se ejecuta blog_manager.py
"""

import os

# ============================================================================
# PATHS DEL SISTEMA
# ============================================================================

# Carpeta donde se guardan los posts HTML y JSON individuales
POSTS_FOLDER = "posts"

# Carpeta de thumbnails (miniaturas para el índice)
THUMBNAILS_FOLDER = "assets/thumbnails"

# Carpeta de imágenes destacadas de posts
POST_IMAGES_FOLDER = "assets/post-images"

# Carpeta donde están las plantillas HTML
TEMPLATES_FOLDER = "templates"

# Carpeta de tag-indexes (HTML y JSON de tags)
TAGS_FOLDER = "tags"

# Archivo índice maestro de posts (auto-gestionado)
POSTS_INDEX_FILE = "posts.json"

# Archivo HTML del índice principal
INDEX_HTML_FILE = "index.html"


# ============================================================================
# INFORMACIÓN DEL BLOG Y AUTOR
# ============================================================================
BLOG_NAME = "BIT FORWARD"
AUTHOR_NAME = "María Antiñolo"
AUTHOR_BIO = "🎯 Technical Product Owner | Project Manager | Cross-industry strategist combining technical depth, user-centered design expertise, and business acumen | AI-enhanced product development 🚀"
BLOG_DESCRIPTION = "Digital product strategy, technical lessons, strategic challenges"
PORTFOLIO_URL = "https://bit-oriented.com"


# ============================================================================
# CONFIGURACIÓN DE COMPORTAMIENTO
# ============================================================================

# Número máximo de posts para mostrar en columna única centrada
# Si hay más posts, se activa el grid de 3 columnas
MAX_POSTS_SINGLE_COLUMN = 2

# Validar existencia de imágenes (True = solo advertencia, False = bloquea)
VALIDATE_IMAGES = True
ALLOW_MISSING_IMAGES = True  # True = continúa sin bloquear, False = detiene


# ============================================================================
# NOMBRES DE PLANTILLAS HTML
# ============================================================================

POST_TEMPLATE_FILE = "post_template_V2.html"
INDEX_TEMPLATE_FILE = "index_template_V2.html"
TAG_INDEX_TEMPLATE_FILE = "tag_index_template.html"


# ============================================================================
# FUNCIONES DE UTILIDAD PARA PATHS
# ============================================================================

def get_post_html_path(post_number, slug):
    """Genera el path del archivo HTML del post"""
    return os.path.join(POSTS_FOLDER, f"{post_number}-{slug}.html")

def get_post_json_path(post_number, slug):
    """Genera el path del archivo JSON del post"""
    return os.path.join(POSTS_FOLDER, f"{post_number}-{slug}.json")

def get_thumbnail_path(filename):
    """Genera el path del thumbnail"""
    if filename is None:
        return None
    return os.path.join(THUMBNAILS_FOLDER, filename)

def get_featured_image_path(filename):
    """Genera el path de la imagen destacada"""
    if filename is None:
        return None
    return os.path.join(POST_IMAGES_FOLDER, filename)

def get_template_path(template_name):
    """Genera el path de una plantilla HTML"""
    return os.path.join(TEMPLATES_FOLDER, template_name)

def get_tag_index_html_path(tag_slug):
    """Genera el path del archivo HTML de un tag-index"""
    return os.path.join(TAGS_FOLDER, f"{tag_slug}.html")

def get_tag_index_json_path(tag_slug):
    """Genera el path del archivo JSON de un tag-index"""
    return os.path.join(TAGS_FOLDER, f"posts-{tag_slug}.json")


# ============================================================================
# VALIDACIÓN DE CONFIGURACIÓN
# ============================================================================

def validate_config():
    """
    Valida que la configuración sea correcta y crea carpetas necesarias.
    Retorna True si todo está OK, False si hay errores críticos.
    """
    errors = []
    warnings = []
    
    # Crear carpetas si no existen
    folders = [
        POSTS_FOLDER,
        THUMBNAILS_FOLDER,
        POST_IMAGES_FOLDER,
        TEMPLATES_FOLDER,
        TAGS_FOLDER
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder, exist_ok=True)
                warnings.append(f"✓ Carpeta creada: {folder}")
            except Exception as e:
                errors.append(f"✗ No se pudo crear carpeta {folder}: {e}")
    
    # Validar que existan las plantillas
    post_template = get_template_path(POST_TEMPLATE_FILE)
    index_template = get_template_path(INDEX_TEMPLATE_FILE)
    tag_index_template = get_template_path(TAG_INDEX_TEMPLATE_FILE)
    
    if not os.path.exists(post_template):
        errors.append(f"✗ Plantilla no encontrada: {post_template}")
    
    if not os.path.exists(index_template):
        errors.append(f"✗ Plantilla no encontrada: {index_template}")
    
    if not os.path.exists(tag_index_template):
        warnings.append(f"⚠ Plantilla no encontrada: {tag_index_template}")
    
    # Mostrar warnings
    if warnings:
        for w in warnings:
            print(w)
    
    # Mostrar errores
    if errors:
        print("\n❌ ERRORES DE CONFIGURACIÓN:")
        for e in errors:
            print(f"   {e}")
        return False
    
    return True


# ============================================================================
# INFORMACIÓN DEL SISTEMA
# ============================================================================

SYSTEM_VERSION = "2.1.0"
SYSTEM_NAME = "Blog Manager - Sistema con Tag-Indexes"

def print_system_info():
    """Imprime información del sistema"""
    print(f"\n{'='*70}")
    print(f"  {SYSTEM_NAME} v{SYSTEM_VERSION}")
    print(f"{'='*70}")
    print(f"  Autor: {AUTHOR_NAME}")
    print(f"  Posts folder: {POSTS_FOLDER}")
    print(f"  Tags folder: {TAGS_FOLDER}")
    print(f"  Templates folder: {TEMPLATES_FOLDER}")
    print(f"  Max posts single column: {MAX_POSTS_SINGLE_COLUMN}")
    print(f"{'='*70}\n")
