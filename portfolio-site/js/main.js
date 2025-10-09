/**
 * Portfolio Site - Main JavaScript
 * Handles carousel, blog pagination, and dynamic content loading
 */

// ===========================
// State Management
// ===========================
const state = {
    projects: [],
    blogPosts: [],
    currentProjectIndex: 0,
    currentBlogPage: 1,
    postsPerPage: 3
};

// ===========================
// DOM Elements
// ===========================
const elements = {
    carouselTrack: document.getElementById('carousel-track'),
    carouselIndicators: document.getElementById('carousel-indicators'),
    carouselPrevBtn: document.querySelector('.carousel-btn-prev'),
    carouselNextBtn: document.querySelector('.carousel-btn-next'),
    blogGrid: document.getElementById('blog-grid'),
    pagination: document.getElementById('pagination'),
    currentYear: document.getElementById('current-year')
};

// ===========================
// Initialization
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    // Set current year
    if (elements.currentYear) {
        elements.currentYear.textContent = new Date().getFullYear();
    }

    // Smooth scrolling for navigation
    setupSmoothScrolling();

    // Load content
    await loadProjects();
    await loadBlogPosts();

    // Setup carousel navigation
    if (elements.carouselPrevBtn && elements.carouselNextBtn) {
        elements.carouselPrevBtn.addEventListener('click', () => moveCarousel(-1));
        elements.carouselNextBtn.addEventListener('click', () => moveCarousel(1));
    }

    // Add scroll effects
    setupScrollEffects();
}

// ===========================
// Smooth Scrolling
// ===========================
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || !href) return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===========================
// Scroll Effects (Navbar)
// ===========================
function setupScrollEffects() {
    const nav = document.getElementById('nav');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            nav.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            nav.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    });
}

// ===========================
// Projects - Carousel
// ===========================
async function loadProjects() {
    try {
        const response = await fetch('projects/projects.json');
        if (!response.ok) throw new Error('Failed to load projects');

        state.projects = await response.json();
        renderProjects();
        renderCarouselIndicators();
    } catch (error) {
        console.error('Error loading projects:', error);
        elements.carouselTrack.innerHTML = '<div style="padding: 2rem; text-align: center; color: #6b6b6b;">Projects coming soon...</div>';
    }
}

function renderProjects() {
    if (state.projects.length === 0) {
        elements.carouselTrack.innerHTML = '<div style="padding: 2rem; text-align: center;">No projects available yet.</div>';
        return;
    }

    elements.carouselTrack.innerHTML = state.projects
        .map(project => `
            <div class="carousel-slide">
                <h3>${escapeHtml(project.name)}</h3>
                <p class="carousel-slide-description">${escapeHtml(project.description)}</p>
                ${project.tech ? `<p class="carousel-slide-tech"><strong>Tech:</strong> ${escapeHtml(project.tech)}</p>` : ''}
                ${renderProjectLinks(project)}
            </div>
        `)
        .join('');

    // Show first slide
    updateCarousel();
}

function renderProjectLinks(project) {
    const links = [];

    if (project.github) {
        links.push(`<a href="${escapeHtml(project.github)}" target="_blank" rel="noopener noreferrer">GitHub</a>`);
    }

    if (project.demo) {
        links.push(`<a href="${escapeHtml(project.demo)}" target="_blank" rel="noopener noreferrer">Live Demo</a>`);
    }

    if (project.link) {
        links.push(`<a href="${escapeHtml(project.link)}" target="_blank" rel="noopener noreferrer">View Project</a>`);
    }

    if (links.length > 0) {
        return `<div class="carousel-slide-links">${links.join('')}</div>`;
    }

    return '';
}

function renderCarouselIndicators() {
    if (state.projects.length <= 1) {
        elements.carouselIndicators.innerHTML = '';
        return;
    }

    elements.carouselIndicators.innerHTML = state.projects
        .map((_, index) => `
            <button class="carousel-indicator ${index === 0 ? 'active' : ''}"
                    data-index="${index}"
                    aria-label="Go to project ${index + 1}">
            </button>
        `)
        .join('');

    // Add click handlers
    document.querySelectorAll('.carousel-indicator').forEach(indicator => {
        indicator.addEventListener('click', (e) => {
            const index = parseInt(e.target.dataset.index);
            goToSlide(index);
        });
    });
}

function moveCarousel(direction) {
    state.currentProjectIndex += direction;

    // Loop around
    if (state.currentProjectIndex < 0) {
        state.currentProjectIndex = state.projects.length - 1;
    } else if (state.currentProjectIndex >= state.projects.length) {
        state.currentProjectIndex = 0;
    }

    updateCarousel();
}

function goToSlide(index) {
    state.currentProjectIndex = index;
    updateCarousel();
}

function updateCarousel() {
    const offset = -state.currentProjectIndex * 100;
    elements.carouselTrack.style.transform = `translateX(${offset}%)`;

    // Update indicators
    document.querySelectorAll('.carousel-indicator').forEach((indicator, index) => {
        if (index === state.currentProjectIndex) {
            indicator.classList.add('active');
        } else {
            indicator.classList.remove('active');
        }
    });
}

// ===========================
// Blog Posts with Pagination
// ===========================
async function loadBlogPosts() {
    try {
        const response = await fetch('blog/posts.json');
        if (!response.ok) throw new Error('Failed to load blog posts');

        state.blogPosts = await response.json();
        renderBlogPage();
    } catch (error) {
        console.error('Error loading blog posts:', error);
        elements.blogGrid.innerHTML = '<div style="padding: 2rem; text-align: center; color: #6b6b6b; grid-column: 1 / -1;">Blog posts coming soon...</div>';
    }
}

function renderBlogPage() {
    if (state.blogPosts.length === 0) {
        elements.blogGrid.innerHTML = '<div style="padding: 2rem; text-align: center; grid-column: 1 / -1;">No blog posts available yet.</div>';
        return;
    }

    // Calculate pagination
    const totalPages = Math.ceil(state.blogPosts.length / state.postsPerPage);
    const startIndex = (state.currentBlogPage - 1) * state.postsPerPage;
    const endIndex = startIndex + state.postsPerPage;
    const postsToShow = state.blogPosts.slice(startIndex, endIndex);

    // Render blog posts
    elements.blogGrid.innerHTML = postsToShow
        .map(post => `
            <article class="blog-card" onclick="window.location.href='blog-post.html?slug=${escapeHtml(post.slug)}'">
                <h3 class="blog-card-title">${escapeHtml(post.title)}</h3>
                <p class="blog-card-date">${formatDate(post.date)}</p>
                <p class="blog-card-excerpt">${escapeHtml(post.excerpt)}</p>
            </article>
        `)
        .join('');

    // Render pagination
    renderPagination(totalPages);
}

function renderPagination(totalPages) {
    if (totalPages <= 1) {
        elements.pagination.innerHTML = '';
        return;
    }

    const buttons = [];

    // Previous button
    buttons.push(`
        <button class="pagination-btn"
                ${state.currentBlogPage === 1 ? 'disabled' : ''}
                onclick="changePage(${state.currentBlogPage - 1})"
                aria-label="Previous page">
            &laquo; Prev
        </button>
    `);

    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        // Show first, last, current, and adjacent pages
        if (
            i === 1 ||
            i === totalPages ||
            (i >= state.currentBlogPage - 1 && i <= state.currentBlogPage + 1)
        ) {
            buttons.push(`
                <button class="pagination-btn ${i === state.currentBlogPage ? 'active' : ''}"
                        onclick="changePage(${i})"
                        aria-label="Go to page ${i}">
                    ${i}
                </button>
            `);
        } else if (
            i === state.currentBlogPage - 2 ||
            i === state.currentBlogPage + 2
        ) {
            buttons.push('<span style="padding: 0.5rem;">...</span>');
        }
    }

    // Next button
    buttons.push(`
        <button class="pagination-btn"
                ${state.currentBlogPage === totalPages ? 'disabled' : ''}
                onclick="changePage(${state.currentBlogPage + 1})"
                aria-label="Next page">
            Next &raquo;
        </button>
    `);

    elements.pagination.innerHTML = buttons.join('');
}

function changePage(page) {
    const totalPages = Math.ceil(state.blogPosts.length / state.postsPerPage);

    if (page < 1 || page > totalPages) return;

    state.currentBlogPage = page;
    renderBlogPage();

    // Scroll to blog section
    document.getElementById('blog').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Make changePage available globally
window.changePage = changePage;

// ===========================
// Utility Functions
// ===========================
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', options);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ===========================
// Performance Optimization
// ===========================
// Lazy load images if any are added in the future
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    });

    // Observe all images with data-src attribute
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}
