# Minimalist Portfolio Website

A clean, efficient, and responsive portfolio website built with vanilla HTML, CSS, and JavaScript. Features a blog system with Markdown support and a project showcase section.

## 🎯 Project Overview

This portfolio is designed with minimalism and efficiency in mind. It uses no frameworks or build tools—just pure HTML, CSS, and JavaScript—making it lightweight, fast, and easy to understand. The design follows a mobile-first approach with a grayscale color scheme and generous margins for a clean, professional look.

### Key Features

- **Single-page application** - Smooth transitions between Blog and Projects sections without page reloads
- **Markdown blog** - Write blog posts in Markdown that automatically convert to HTML
- **Project showcase** - Display your development projects with optional images
- **Responsive design** - Mobile-first approach that scales beautifully to desktop
- **Minimalist aesthetic** - Grayscale color scheme with Roboto font and ample whitespace
- **No build process** - Pure vanilla JS, no compilation or bundling required
- **Easy deployment** - Works on GitHub Pages, GoDaddy cPanel, or any static host

## 📁 Project Structure

```
/
├── index.html              # Main page with blog/projects toggle
├── about.html              # About page with bio, resume, and social links
├── css/
│   └── styles.css          # All styles (mobile-first, responsive)
├── js/
│   └── main.js             # All JavaScript functionality
├── blog/
│   ├── posts.json          # Blog post metadata (title, date, excerpt, slug)
│   ├── first-post.md       # Example blog post in Markdown
│   └── learning-web-development.md
├── projects/
│   ├── projects.json       # Project data (name, description, tech, links)
│   └── images/             # Optional project images
│       └── .gitkeep
├── assets/
│   ├── .gitkeep
│   └── resume.pdf          # Your resume (add your own)
└── README.md               # This file
```

## 🚀 Getting Started

### Quick Start

1. **Clone or download** this repository
2. **Customize content** - Update the files with your information
3. **Test locally** - Open `index.html` in a browser
4. **Deploy** - Upload to your hosting provider

### Detailed Setup

#### 1. Personalize About Page

Edit `about.html`:
- Replace the placeholder bio text with your own introduction
- Update social links (GitHub, LinkedIn) with your profile URLs
- Add your resume PDF to `assets/resume.pdf`

#### 2. Add Blog Posts

To create a new blog post:

1. Write your post in Markdown format
2. Save it as `blog/your-post-slug.md`
3. Add an entry to `blog/posts.json`:

```json
{
  "slug": "your-post-slug",
  "title": "Your Post Title",
  "date": "2025-01-15",
  "excerpt": "A brief description of your post that appears in the list."
}
```

**Markdown Support:**
- Headings (`#`, `##`, `###`)
- Bold (`**text**`) and italic (`*text*`)
- Links (`[text](url)`)
- Code blocks with syntax highlighting
- Lists (ordered and unordered)
- Blockquotes
- Images

#### 3. Add Projects

Edit `projects/projects.json` to add your projects:

```json
{
  "name": "Project Name",
  "description": "Brief description of the project and what it does.",
  "tech": "HTML, CSS, JavaScript",
  "github": "https://github.com/yourusername/project",
  "demo": "https://your-demo-url.com",
  "image": "project-screenshot.png"
}
```

**Fields:**
- `name` (required) - Project name
- `description` (required) - Brief description
- `tech` (optional) - Technologies used
- `github` (optional) - GitHub repository URL
- `demo` (optional) - Live demo URL
- `image` (optional) - Image filename (place in `projects/images/`)

**Adding Project Images:**
1. Place image files in `projects/images/`
2. Reference the filename in the `image` field
3. Images automatically optimize with lazy loading

## 🎨 Customization

### Color Scheme

The site uses CSS custom properties (variables) for easy theming. Edit `css/styles.css`:

```css
:root {
    --color-black: #000000;
    --color-dark-gray: #333333;
    --color-medium-gray: #666666;
    --color-light-gray: #999999;
    --color-very-light-gray: #e0e0e0;
    --color-off-white: #f5f5f5;
    --color-white: #ffffff;
}
```

### Typography

Change the font by editing the Google Fonts link in `index.html` and `about.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
```

Then update the CSS variable:

```css
:root {
    --font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

### Margins and Spacing

Adjust responsive margins in `css/styles.css`:

```css
:root {
    --margin-mobile: 1.5rem;
    --margin-tablet: 3rem;
    --margin-desktop: 6rem;
}
```

### Layout

The site uses CSS Grid for layouts. Key responsive breakpoints:
- **Mobile**: Base styles (< 768px)
- **Tablet**: 768px and up
- **Desktop**: 1024px and up

## 💻 How It Works

### Architecture

The site follows a simple client-side architecture:

1. **HTML** - Semantic structure with minimal markup
2. **CSS** - Mobile-first responsive styles with CSS Grid and Flexbox
3. **JavaScript** - Vanilla ES6+ for all functionality

### JavaScript Functionality

**File: `js/main.js`**

Key functions:

- `initializeApp()` - Sets up navigation, loads content, handles events
- `switchSection(sectionName)` - Toggles between Blog and Projects without page reload
- `loadBlogPosts()` - Fetches `blog/posts.json` and renders blog list
- `loadBlogPost(slug)` - Fetches Markdown file, converts to HTML using marked.js
- `loadProjects()` - Fetches `projects/projects.json` and renders projects
- `formatDate(dateString)` - Formats dates for display

### Dependencies

**marked.js** (v11.1.1) - Lightweight Markdown parser loaded from CDN
- Only external dependency
- ~25KB minified
- Loaded via CDN in `index.html`

### State Management

Simple state object tracks current section and loaded data:

```javascript
const state = {
    currentSection: 'blog',
    posts: [],
    projects: []
};
```

### Navigation Flow

1. User clicks nav link or section toggle
2. `switchSection()` updates active states
3. CSS transitions handle visual changes
4. Content stays loaded (no re-fetching)

### Blog System

**Posts List View:**
- Reads `blog/posts.json`
- Displays title, date, and excerpt
- Clickable items load full post

**Post Detail View:**
- Fetches `.md` file based on slug
- Parses Markdown to HTML with marked.js
- Displays with "Back to Blog" button
- Styled for readability

## 🌐 Deployment

### GitHub Pages

1. Create a GitHub repository
2. Push your code
3. Go to Settings > Pages
4. Select branch (usually `main`) and root folder
5. Save and wait for deployment
6. Access at `https://yourusername.github.io/repository-name`

**Important for GitHub Pages:**
- Ensure all links are relative
- No server-side processing required
- May take a few minutes to deploy

### GoDaddy cPanel

1. Log into cPanel
2. Open File Manager
3. Navigate to `public_html` (or your domain's folder)
4. Upload all files and folders
5. Maintain the directory structure
6. Access at your domain

**cPanel Tips:**
- Upload as a `.zip` and extract in cPanel for faster transfer
- Set file permissions to 644 and folders to 755
- Clear browser cache after updates

### Other Static Hosts

This site works with any static hosting service:
- **Netlify** - Drag and drop deployment
- **Vercel** - Connect GitHub repo for auto-deployment
- **Cloudflare Pages** - Fast global CDN
- **AWS S3** - Scalable static hosting

## 🛠️ Development Tips

### Local Testing

**Option 1: Python Simple Server**
```bash
python -m http.server 8000
# Visit http://localhost:8000
```

**Option 2: PHP Built-in Server**
```bash
php -S localhost:8000
```

**Option 3: VS Code Live Server Extension**
- Install "Live Server" extension
- Right-click `index.html` > "Open with Live Server"

### Debugging

**Common Issues:**

1. **Blog posts not loading**
   - Check `blog/posts.json` syntax (valid JSON)
   - Ensure slug matches `.md` filename
   - Check browser console for errors

2. **Projects not displaying**
   - Verify `projects/projects.json` is valid JSON
   - Check image paths if using images

3. **Markdown not rendering**
   - Ensure marked.js CDN link is working
   - Check browser console for script errors

4. **Styling issues**
   - Clear browser cache
   - Check CSS file path in HTML
   - Verify no CSS syntax errors

### Browser Support

- **Modern browsers**: Chrome, Firefox, Safari, Edge (last 2 versions)
- **CSS Grid and Flexbox**: IE11 not supported
- **ES6 JavaScript**: No transpilation included

### Performance

**Optimizations included:**
- Lazy loading for project images
- Minimal CSS (no framework bloat)
- Single CSS/JS files (fewer HTTP requests)
- CDN for external dependencies
- Semantic HTML for SEO

**Lighthouse Scores (Target):**
- Performance: 95+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

## 📝 Content Guidelines

### Writing Blog Posts

**Best Practices:**
- Use clear, descriptive titles
- Write concise excerpts (1-2 sentences)
- Use headings to structure content
- Include code examples when relevant
- Proofread before publishing

**Markdown Tips:**
- Use `##` for main sections
- Use `###` for subsections
- Add code blocks with triple backticks
- Include alt text for images

### Describing Projects

**Effective Descriptions:**
- Explain what the project does (not how)
- Highlight key features or challenges
- Keep it under 2-3 sentences
- Focus on impact and results

**Tech Stack:**
- List main technologies used
- Keep it concise (3-5 items)
- Use common names (React, not React.js)

## 🔧 Extending the Site

### Adding New Sections

1. Add HTML section to `index.html`:
```html
<section id="new-section" class="content-section">
    <h2 class="section-title">New Section</h2>
    <!-- Content here -->
</section>
```

2. Add navigation link:
```html
<li><a href="#" data-section="new" class="nav-link">New</a></li>
```

3. The existing JavaScript will handle the toggle automatically

### Adding Contact Form

For a static site, use a service like:
- **Formspree** - Simple form backend
- **Netlify Forms** - If hosted on Netlify
- **EmailJS** - Client-side email sending

### Adding Analytics

Add to `<head>` in both HTML files:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-ID');
</script>
```

## 🐛 Troubleshooting

### CORS Errors (Local Development)

If you see CORS errors when opening `index.html` directly:
- Use a local server (see Development Tips)
- Browsers block local file access for security

### Images Not Displaying

- Check file paths are correct
- Verify images exist in `projects/images/`
- Check image filenames match (case-sensitive)
- Ensure images are web-optimized formats (JPG, PNG, WebP)

### JSON Parsing Errors

- Validate JSON at [jsonlint.com](https://jsonlint.com)
- Check for trailing commas
- Ensure all strings use double quotes
- Verify no special characters are unescaped

## 📄 License

This project is provided as-is for personal and commercial use. Feel free to modify, distribute, and use as you see fit.

## 🤝 Contributing

This is a personal portfolio template, but suggestions are welcome! If you find bugs or have ideas for improvements, feel free to open an issue or contribute.

## 📞 Support

For questions about using this template:
1. Check this README thoroughly
2. Review the example files
3. Check browser console for errors
4. Ensure file structure matches documentation

## 🎓 Learning Resources

**HTML/CSS/JavaScript:**
- [MDN Web Docs](https://developer.mozilla.org/)
- [web.dev](https://web.dev/)

**Markdown:**
- [Markdown Guide](https://www.markdownguide.org/)
- [CommonMark Spec](https://commonmark.org/)

**Git & GitHub:**
- [GitHub Docs](https://docs.github.com/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)

---

## 🚀 Quick Reference

### Adding a Blog Post
1. Create `blog/your-slug.md`
2. Add entry to `blog/posts.json`
3. Refresh the site

### Adding a Project
1. Edit `projects/projects.json`
2. Add project object with required fields
3. Optionally add image to `projects/images/`
4. Refresh the site

### Customizing Colors
1. Edit CSS variables in `css/styles.css`
2. Update `:root` section
3. Save and refresh

### Deploying
1. Push to GitHub
2. Enable GitHub Pages in Settings
3. Access at provided URL

---

**Built with ❤️ using vanilla HTML, CSS, and JavaScript**