# 📝 Blog Manager v2.0 - Robust Static Blog Management System

Modular Python system for managing a static blog with automatic post generation, index, and navigation. **Completely redesigned for maximum robustness and stability.**

## 🎯 Features

- ✅ **Post creation**: Interactive guided mode or from JSON files (audio removed to avoid dependencies)
- ✅ **Automatic index generation**: Updates `index.html` with all posts
- ✅ **Automatic navigation**: Previous/next links in each post
- ✅ **Separate HTML templates**: No embedded HTML in Python, easy to customize
- ✅ **Self-managed posts.json**: Automatically created and updated
- ✅ **Posts with or without images**: Full support for posts without featured images
- ✅ **Responsive grid**: Adaptive design based on number of posts
- ✅ **Complete regeneration**: Rebuilds entire blog when changing templates
- ✅ **Image validation**: Warns if missing but continues without blocking
- ✅ **Modular and scalable**: Clean, commented, and maintainable code

## 🎨 About Templates and Design

This system was created as a practical exercise for a blog post, focusing on the automation engine rather than design. You'll need to create your own HTML templates, CSS, and any JavaScript you want to use. The real value here is the robust automation—post generation, index updates, navigation, and tag management—all handled with simple commands. Think of this as the engine; you bring the templates and style to make the blog truly yours! 🚀

## 🗃️ System Architecture

### Modules and Responsibilities

```
blog_system/
├── config.py                    # ⚙️ Centralized configuration
├── utils.py                     # 🔧 Shared functions
├── post_generator.py            # 📄 HTML post generation
├── index_generator.py           # 📑 Index generation
├── navigation_updater.py        # 🔗 Navigation updates
├── blog_manager.py              # 🎯 Main orchestrator (RUN THIS)
│
├── templates/                   # 🎨 HTML templates
│   ├── post_template.html       # Individual post template
│   └── index_template.html      # Index template
│
├── posts/                       # 📝 Generated posts
│   ├── 1-post-slug.html
│   ├── 1-post-slug.json
│   ├── 2-another-post.html
│   └── 2-another-post.json
│
├── tags/                        # 🏷️ Generated tag listings
│   ├── tag.html
│   ├── posts-tag.json
│   ├── another.html
│   └── posts-another.json
│
├── assets/
│   ├── thumbnails/              # 🖼️ Index thumbnails
│   │   ├── 1-post-thumb.jpg
│   │   └── 2-another-post-thumb.jpg
│   └── post-images/             # 🖼️ Featured post images
│       ├── post.jpg
│       └── another-post.jpg
│
├── posts.json                   # 📋 Master index (self-managed)
├── index.html                   # 🏠 Blog index (generated)
└── README.md                    # 📖 This file
```

### Data Flow (Model-View-Controller)

```
📊 MODEL (JSON)
├── posts.json              → Master post index
└── posts/*.json            → Individual post data

🎨 VIEW (HTML Templates)
├── templates/post_template.html    → Individual post template
└── templates/index_template.html   → Index template

🎮 CONTROLLER (Python Scripts)
├── blog_manager.py         → Main orchestrator
├── post_generator.py       → Generates HTML from JSON
├── index_generator.py      → Generates index
└── navigation_updater.py   → Updates navigation
```

## ⚙️ Initial Setup

### 1. posts.json Structure

The system automatically manages `posts.json` with this structure:

```json
{
  "posts": [
    {
      "number": 1,
      "slug": "when-the-future-looks-back",
      "title": "When the Future Looks Back",
      "excerpt": "Post excerpt...",
      "tags": ["Future", "AI"],
      "read_time": "3",
      "thumbnail": "1-post-thumb.jpg",
      "featured_image": "post.jpg"
    },
    {
      "number": 2,
      "slug": "another-post",
      "title": "Another Post",
      "excerpt": "...",
      "tags": ["Tech"],
      "read_time": "5",
      "thumbnail": null,
      "featured_image": null
    }
  ]
}
```

**Important notes:**
- `posts.json` is automatically created if it doesn't exist
- Automatically updated when creating/editing posts
- `thumbnail` and `featured_image` can be `null` (no image)
- Posts are automatically sorted by number

### 2. Edit config.py

Open `config.py` and adjust according to your structure:

```python
# Paths (relative to directory where you run blog_manager.py)
POSTS_FOLDER = "posts"
THUMBNAILS_FOLDER = "assets/thumbnails"
POST_IMAGES_FOLDER = "assets/post-images"
TEMPLATES_FOLDER = "templates"

# Blog information
AUTHOR_NAME = "Author name"
BLOG_NAME = "Blog"
AUTHOR_BIO = "Your bio here..."
BLOG_DESCRIPTION = "Your blog description"
PORTFOLIO_URL = "Your main site or domain URL"

# Responsive grid (NEW FEATURE!)
MAX_POSTS_SINGLE_COLUMN = 4  # If ≤4 posts: centered single column
                              # If >4 posts: 3-column grid

# Image validation
VALIDATE_IMAGES = True          # Validate image existence
ALLOW_MISSING_IMAGES = True     # True = warns only, False = blocks
```

### 3. Individual Post JSON Structure

Example of `1-post.json`:

```json
{
  "number": 1,
  "slug": "once-upon-a-time",
  "title": "Once Upon a Time",
  "excerpt": "Excerpt...",
  "tags": ["Future", "Story", "AI"],
  "read_time": "3",
  "thumbnail": "1-post-thumb.jpg",
  "featured_image": "post.jpg",
  "content": "<p>Complete HTML post content...</p>",
  "prev_post": null,
  "next_post": {
    "number": 2,
    "slug": "another-post",
    "title": "Another Post"
  }
}
```

## 🚀 System Usage

### Interactive Menu (Recommended)

```bash
python3 blog_manager.py
```

You'll see:
```
1. Create new post (guided mode)
2. Update blog index
3. Update post navigation
4. Regenerate entire blog
5. Exit
```

### Direct Commands

#### Create new post (guided mode)
```bash
# On Linux/Mac (to paste HTML >1023 characters)
stty -icanon; python3 blog_manager.py --new-post

# On Windows
python3 blog_manager.py --new-post
```

The system will ask for:
- Post title
- Slug (automatically generated from title)
- Excerpt
- Tags (comma-separated)
- Reading time
- Thumbnail (optional, Enter to skip)
- Featured image (optional, Enter to skip)
- HTML content (type `END` to finish)

**Automatic flow after creating post:**
1. ✅ Generates post HTML
2. ✅ Saves individual JSON
3. ✅ Updates posts.json
4. ✅ Regenerates index.html
5. ✅ Regenerates tag listings and updates tag clouds on existing pages and listings
6. ✅ Updates navigation for all posts

#### Create post from JSON
```bash
python3 blog_manager.py --from-json my-post.json
```

JSON file format:
```json
{
  "title": "My New Post",
  "excerpt": "Post summary",
  "content": "<p>HTML content...</p>",
  "tags": ["Tag1", "Tag2"],
  "read_time": "5",
  "thumbnail": "1-my-post-thumb.jpg",
  "featured_image": "my-post.jpg"
}
```

**Notes:**
- `number` and `slug` are automatically generated
- `thumbnail` and `featured_image` are optional

#### Update index only
```bash
python3 blog_manager.py --update-index
```

#### Regenerate tag indexes
```bash
python3 blog_manager.py --regenerate-tags
```

#### Update navigation only
```bash
python3 blog_manager.py --update-nav
```

#### Regenerate entire blog
```bash
python3 blog_manager.py --regenerate
```

**Use this when:**
- You change HTML templates
- You modify CSS styles in templates
- posts.json becomes out of sync
- index.html layout isn't updating according to post count (delete posts.json before regenerating if this is the case)
- You want to rebuild everything from scratch

## 📝 Common Workflows

### Create a new post with images

1. **Prepare images**:
   ```bash
   # Thumbnail for index
   cp image.jpg assets/thumbnails/3-my-post-thumb.jpg
   
   # Featured image for post
   cp large-image.jpg assets/post-images/my-post.jpg
   ```

2. **Run post creator**:
   ```bash
   python3 blog_manager.py --new-post
   ```

3. **Follow instructions**

4. **Result**:
   - ✅ HTML post generated in `posts/`
   - ✅ Individual JSON saved
   - ✅ posts.json updated
   - ✅ index.html regenerated
   - ✅ Navigation updated

### Create a post WITHOUT images

1. **Run creator**:
   ```bash
   python3 blog_manager.py --new-post
   ```

2. **Press Enter on image fields**:
   ```
   Thumbnail name (or Enter if none): [Enter]
   Featured image name (or Enter if none): [Enter]
   ```

3. **Result**:
   - Post without `<img>` block in HTML
   - Index card without thumbnail
   - Everything works perfectly

### Change HTML templates

1. **Edit templates**:
   ```bash
   # Edit post template
   nano templates/post_template.html
   
   # Edit index template
   nano templates/index_template.html
   ```

2. **Regenerate everything**:
   ```bash
   python3 blog_manager.py --regenerate
   ```

3. **Result**: All posts and index use new templates

### Edit existing post content

1. **Edit individual JSON**:
   ```bash
   nano posts/1-my-post.json
   ```

2. **Modify `content` field**

3. **Regenerate post**:
   ```bash
   python3 blog_manager.py --regenerate
   ```

## 🎨 Template Customization

### Individual Post Template (post_template.html)

**Available placeholders:**

- `{title}` - Post title
- `{excerpt}` - Post excerpt
- `{author}` - Author name (from config.py)
- `{author_bio}` - Author bio
- `{content}` - Post HTML content
- `{tags_html}` - Tags formatted in HTML
- `{read_time}` - Reading time
- `{featured_image_html}` - Featured image (empty if none)
- `{navigation_html}` - Prev/next navigation (empty if none)
- `{index_file}` - Index file name

**Example usage in template:**
```html
<h1>{title}</h1>
<div>{content}</div>
{featured_image_html}
{tags_html}
```

### Index Template (index_template.html)

**Available placeholders:**

- `{author}` - Author name
- `{blog_name}` - Blog name
- `{blog_description}` - Blog description
- `{portfolio_url}` - Portfolio URL
- `{author_bio}` - Author bio
- `{posts_cards}` - HTML of all post cards
- `{grid_class}` - Grid CSS class:
  - `"single-post"` if posts ≤ MAX_POSTS_SINGLE_COLUMN
  - `"small-cards"` if posts > MAX_POSTS_SINGLE_COLUMN

**Responsive Grid:**

The system automatically applies CSS classes based on post count:

```css
/* 1-4 posts: Centered single column */
.posts-grid.single-post {
    grid-template-columns: 1fr;
    max-width: 800px;
}

/* 5+ posts: 3-column grid with small cards */
.posts-grid.small-cards {
    grid-template-columns: repeat(3, 1fr);
}
.small-cards .post-thumbnail {
    height: 180px;  /* Smaller */
}
```

## 🔧 Troubleshooting

### Error: "Template not found"

**Cause**: `templates/post_template.html` or `templates/index_template.html` doesn't exist

**Solution**:
```bash
# Verify templates exist
ls templates/

# If they don't exist, create them from original files
```

### Error: "No module named 'config'"

**Cause**: Running script from incorrect folder

**Solution**:
```bash
# Run from project root folder
cd /path/to/blog_system
python blog_manager.py
```

### Thumbnails don't show in index

**Cause**: Incorrect path or image doesn't exist

**Solution**:
1. Verify image exists:
   ```bash
   ls assets/thumbnails/1-post-thumb.jpg
   ```

2. Verify paths in `config.py`:
   ```python
   THUMBNAILS_FOLDER = "assets/thumbnails"
   ```

3. Verify path in `posts.json`:
   ```json
   "thumbnail": "1-post-thumb.jpg"
   ```

### Navigation (prev/next) is broken

**Solution**:
```bash
python3 blog_manager.py --update-nav
```

This recalculates all navigation links.

### posts.json is out of sync

**Solution**:
```bash
# Delete posts.json
rm posts.json

# System will rebuild it automatically
python3 blog_manager.py --regenerate
```

### Want to start from scratch

```bash
# 1. Backup (just in case)
cp -r posts posts_backup
cp posts.json posts.json.backup

# 2. Clean everything
rm posts.json
rm posts/*.html
rm posts/*.json

# 3. Create first post
python3 blog_manager.py --new-post
```

## 📚 Complete File Structure

```
blog_system/
│
├── 🎯 MAIN EXECUTABLES
│   └── blog_manager.py          # RUN THIS for everything
│
├── ⚙️ CONFIGURATION
│   └── config.py                # Centralized configuration
│
├── 🔧 INTERNAL MODULES
│   ├── utils.py                 # Shared functions
│   ├── post_generator.py        # Generates HTML posts
│   ├── index_generator.py       # Generates HTML index
│   └── navigation_updater.py    # Updates navigation
│
├── 🎨 HTML TEMPLATES
│   └── templates/
│       ├── post_template.html   # Individual post template
│       └── index_template.html  # Index template
│
├── 📝 GENERATED POSTS
│   └── posts/
│       ├── 1-post.html          # Post HTML
│       ├── 1-post.json          # Post data
│       ├── 2-another.html
│       └── 2-another.json
│
├── 🏷️ GENERATED TAG LISTS
│   └── tags/
│       ├── tag.html             # Listing HTML
│       ├── posts-tag.json       # Listing data
│       ├── another.html
│       └── posts-another.json
│
├── 🖼️ RESOURCES
│   └── assets/
│       ├── thumbnails/          # Index thumbnails
│       │   ├── 1-post-thumb.jpg
│       │   └── 2-another-thumb.jpg
│       └── post-images/         # Featured images
│           ├── post.jpg
│           └── another.jpg
│
├── 📋 INDEXES
│   ├── posts.json               # Master index (self-managed)
│   └── index.html               # HTML index (generated)
│
└── 📖 DOCUMENTATION
    └── README.md                # This file
```

## 🚀 Possible Future Improvements

The system is designed to be extensible:

- [ ] Improved file structure (Data file for all JSON data, etc.)
- [ ] Category support
- [ ] sitemap.xml generation
- [ ] Draft system
- [ ] Blog search
- [ ] RSS feed
- [ ] Index pagination
- [ ] Export to Markdown
- [ ] Preview before publishing

## 📄 License

AGPL-3.0 license

---

**Questions or issues?** Review the commented code or this README. All modules are exhaustively documented.

**System developed with:** Python 3.x | HTML5 | CSS3