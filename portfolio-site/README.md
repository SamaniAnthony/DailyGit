# Portfolio Website

A modern, minimalist portfolio website with a grayscale color scheme. Features a hero section, projects carousel, and a blog with pagination.

## Features

- **Hero Section**: Eye-catching introduction with call-to-action buttons
- **About Section**: Brief introduction and overview
- **Projects Carousel**: Showcases your projects in an interactive carousel
- **Blog with Pagination**: Displays blog posts with 3 posts per page
- **Responsive Design**: Works perfectly on all devices
- **Lightweight**: No heavy frameworks, just vanilla JavaScript
- **SEO Optimized**: Includes proper meta tags and structured data
- **Accessible**: WCAG compliant with proper ARIA labels

## File Structure

```
portfolio-site/
├── index.html              # Main homepage
├── blog-post.html          # Individual blog post viewer
├── css/
│   └── styles.css          # All styles (minimalist grayscale)
├── js/
│   └── main.js            # Main JavaScript (carousel, pagination, etc.)
├── blog/
│   ├── posts.json         # Blog post metadata
│   └── *.md               # Individual blog posts (Markdown format)
└── projects/
    └── projects.json      # Projects data
```

## How to Add a New Blog Post

### Step 1: Create the Markdown File

1. Create a new `.md` file in the `blog/` directory
2. Name it with a URL-friendly slug (e.g., `my-new-post.md`)
3. Write your content in Markdown format

**Example: `blog/my-new-post.md`**
```markdown
# My New Blog Post Title

This is the introduction paragraph...

## Section Heading

Content here...

- Bullet point 1
- Bullet point 2

## Another Section

More content...
```

### Step 2: Add Metadata to posts.json

1. Open `blog/posts.json`
2. Add a new entry at the **top** of the array (newest posts first)

**Example:**
```json
[
  {
    "slug": "my-new-post",
    "title": "My New Blog Post Title",
    "date": "2025-10-09",
    "excerpt": "A brief description of what this post is about (2-3 sentences)."
  },
  ...existing posts...
]
```

**Important Fields:**
- `slug`: Must match your markdown filename (without .md)
- `title`: The post title shown on the blog page
- `date`: Publication date (YYYY-MM-DD format)
- `excerpt`: A short preview (shown on the blog listing page)

### Step 3: Test Your Post

1. Open `index.html` in your browser
2. Scroll to the blog section
3. Your new post should appear
4. Click on it to view the full post

## How to Add a New Project

1. Open `projects/projects.json`
2. Add a new project object to the array:

```json
[
  {
    "name": "My Awesome Project",
    "description": "A detailed description of what this project does and why it's interesting.",
    "tech": "React, Node.js, MongoDB",
    "github": "https://github.com/username/project",
    "demo": "https://project-demo.com"
  },
  ...existing projects...
]
```

**Fields:**
- `name`: Project name
- `description`: What the project does
- `tech`: Technologies used (comma-separated)
- `github`: (Optional) GitHub repository URL
- `demo`: (Optional) Live demo URL
- `link`: (Optional) Alternative project link

## Customization

### Colors

The site uses a grayscale color scheme. To customize colors, edit the CSS variables in `css/styles.css`:

```css
:root {
    --color-black: #000000;
    --color-gray-900: #2d2d2d;
    --color-gray-700: #525252;
    /* ... etc */
}
```

### Content

#### Change Hero Text
Edit the hero section in `index.html`:
```html
<h1 class="hero-title">Your Title Here</h1>
<p class="hero-subtitle">Your subtitle here</p>
```

#### Change About Text
Edit the about section in `index.html`:
```html
<section class="about" id="about">
    <p class="about-text">Your bio here...</p>
</section>
```

#### Update Contact Email
Find and replace `vnthonysvmvni@gmail.com` with your email address.

### Pagination

To change the number of blog posts per page, edit `js/main.js`:

```javascript
const state = {
    postsPerPage: 3  // Change this number
};
```

## Deployment

### GitHub Pages

1. Push your code to GitHub
2. Go to Settings > Pages
3. Select your branch and save
4. Your site will be live at `https://username.github.io/repository-name`

### Netlify

1. Connect your GitHub repository to Netlify
2. No build settings needed (static site)
3. Deploy!

### Custom Domain

Update the following in `index.html`:
- `<meta property="og:url">` tag
- Structured data URL

## Performance

- **Lighthouse Score**: Optimized for 90+ scores
- **Lazy Loading**: Images lazy load when in viewport
- **Minimal Dependencies**: Only marked.js for Markdown parsing
- **Optimized Fonts**: Google Fonts with preconnect

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please create an issue in the GitHub repository.

---

Built with ❤️ using vanilla HTML, CSS, and JavaScript
