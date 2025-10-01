/**
 * Main JavaScript file for portfolio site
 * Handles navigation, blog post loading, and project display
 */

// ===========================
// State Management
// ===========================
const state = {
    currentSection: 'blog',
    posts: [],
    projects: []
};

// ===========================
// DOM Elements
// ===========================
const elements = {
    navLinks: document.querySelectorAll('.nav-link[data-section]'),
    sections: document.querySelectorAll('.content-section'),
    blogList: document.getElementById('blog-list'),
    blogPost: document.getElementById('blog-post'),
    postContent: document.getElementById('post-content'),
    backToBlog: document.getElementById('back-to-blog'),
    projectsList: document.getElementById('projects-list'),
    currentYear: document.getElementById('current-year')
};

// ===========================
// Initialization
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Set current year in footer
    if (elements.currentYear) {
        elements.currentYear.textContent = new Date().getFullYear();
    }

    // Setup navigation
    setupNavigation();

    // Load initial content
    loadBlogPosts();
    loadProjects();

    // Handle back button for blog posts
    if (elements.backToBlog) {
        elements.backToBlog.addEventListener('click', showBlogList);
    }

    // Check URL hash for section navigation
    handleInitialHash();
}

// ===========================
// Navigation
// ===========================
function setupNavigation() {
    elements.navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const section = link.dataset.section;
            if (section) {
                e.preventDefault();
                switchSection(section);
            }
        });
    });
}

function switchSection(sectionName) {
    // Update active nav link
    elements.navLinks.forEach(link => {
        if (link.dataset.section === sectionName) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Update active section
    elements.sections.forEach(section => {
        if (section.id === `${sectionName}-section`) {
            section.classList.add('active');
        } else {
            section.classList.remove('active');
        }
    });

    // Update state
    state.currentSection = sectionName;

    // If switching to blog, ensure we show the list view
    if (sectionName === 'blog') {
        showBlogList();
    }
}

function handleInitialHash() {
    const hash = window.location.hash.slice(1); // Remove the '#'
    if (hash === 'projects') {
        switchSection('projects');
    }
}

// ===========================
// Blog Functions
// ===========================
async function loadBlogPosts() {
    try {
        const response = await fetch('blog/posts.json');
        if (!response.ok) throw new Error('Failed to load blog posts');

        state.posts = await response.json();
        renderBlogList();
    } catch (error) {
        console.error('Error loading blog posts:', error);
        elements.blogList.innerHTML = '<p class="error">Unable to load blog posts. Please check that blog/posts.json exists.</p>';
    }
}

function renderBlogList() {
    if (state.posts.length === 0) {
        elements.blogList.innerHTML = '<p class="error">No blog posts available yet.</p>';
        return;
    }

    elements.blogList.innerHTML = state.posts
        .map(post => `
            <article class="blog-item" data-slug="${post.slug}">
                <h3>${post.title}</h3>
                <div class="blog-meta">${formatDate(post.date)}</div>
                <p class="blog-excerpt">${post.excerpt}</p>
            </article>
        `)
        .join('');

    // Add click handlers to blog items
    document.querySelectorAll('.blog-item').forEach(item => {
        item.addEventListener('click', () => {
            const slug = item.dataset.slug;
            loadBlogPost(slug);
        });
    });
}

async function loadBlogPost(slug) {
    try {
        const response = await fetch(`blog/${slug}.md`);
        if (!response.ok) throw new Error('Failed to load blog post');

        const markdown = await response.text();
        const html = marked.parse(markdown);

        elements.postContent.innerHTML = html;
        showBlogPost();
    } catch (error) {
        console.error('Error loading blog post:', error);
        elements.postContent.innerHTML = '<p class="error">Unable to load this blog post.</p>';
        showBlogPost();
    }
}

function showBlogPost() {
    elements.blogList.style.display = 'none';
    elements.blogPost.style.display = 'block';
    window.scrollTo(0, 0);
}

function showBlogList() {
    elements.blogList.style.display = 'grid';
    elements.blogPost.style.display = 'none';
    window.scrollTo(0, 0);
}

// ===========================
// Projects Functions
// ===========================
async function loadProjects() {
    try {
        const response = await fetch('projects/projects.json');
        if (!response.ok) throw new Error('Failed to load projects');

        state.projects = await response.json();
        renderProjects();
    } catch (error) {
        console.error('Error loading projects:', error);
        elements.projectsList.innerHTML = '<p class="error">Unable to load projects. Please check that projects/projects.json exists.</p>';
    }
}

function renderProjects() {
    if (state.projects.length === 0) {
        elements.projectsList.innerHTML = '<p class="error">No projects available yet.</p>';
        return;
    }

    elements.projectsList.innerHTML = state.projects
        .map(project => `
            <article class="project-item">
                <h3>${project.name}</h3>
                <p class="project-description">${project.description}</p>
                ${project.tech ? `<p class="project-tech">Tech: ${project.tech}</p>` : ''}
                ${project.image ? `<img src="projects/images/${project.image}" alt="${project.name}" class="project-image" loading="lazy">` : ''}
                ${renderProjectLinks(project)}
            </article>
        `)
        .join('');
}

function renderProjectLinks(project) {
    const links = [];

    if (project.github) {
        links.push(`<a href="${project.github}" target="_blank" rel="noopener noreferrer">GitHub</a>`);
    }

    if (project.demo) {
        links.push(`<a href="${project.demo}" target="_blank" rel="noopener noreferrer">Live Demo</a>`);
    }

    if (links.length > 0) {
        return `<div class="project-links" style="margin-top: 1rem; display: flex; gap: 1rem;">${links.join(' | ')}</div>`;
    }

    return '';
}

// ===========================
// Utility Functions
// ===========================
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', options);
}