/**
 * News Curator Frontend JavaScript
 * Handles UI interactions and API calls
 */

// State
let currentPage = 1;
let currentFilters = {
    category: '',
    source: '',
    unread: false,
    starred: false,
    search: ''
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadArticles();
    loadSources();
});

// Load articles with current filters
async function loadArticles(page = 1) {
    currentPage = page;
    const limit = 50;
    const offset = (page - 1) * limit;

    try {
        const params = new URLSearchParams({
            limit,
            offset,
            ...currentFilters
        });

        const response = await fetch(`/api/articles?${params}`);
        const data = await response.json();

        renderArticles(data.articles);
        renderPagination(data.count, limit, page);
    } catch (error) {
        console.error('Error loading articles:', error);
        showError('Failed to load articles');
    }
}

// Render articles list
function renderArticles(articles) {
    const container = document.getElementById('articlesList');

    if (!articles || articles.length === 0) {
        container.innerHTML = '<div class="loading">No articles found</div>';
        return;
    }

    container.innerHTML = articles.map(article => `
        <div class="article-card ${article.is_read ? '' : 'unread'}">
            <div class="article-card-header">
                <h3 class="article-card-title" onclick="openArticle(${article.id})">
                    ${escapeHtml(article.title)}
                </h3>
            </div>

            <div class="article-meta">
                <span class="meta-item">
                    <strong>Source:</strong> ${escapeHtml(article.source_name)}
                </span>
                ${article.author ? `
                    <span class="meta-item">
                        <strong>By:</strong> ${escapeHtml(article.author)}
                    </span>
                ` : ''}
                ${article.published_date ? `
                    <span class="meta-item">
                        📅 ${formatDate(article.published_date)}
                    </span>
                ` : ''}
                ${article.category ? `
                    <span class="category-badge">${escapeHtml(article.category)}</span>
                ` : ''}
            </div>

            ${article.summary ? `
                <p class="article-excerpt">${escapeHtml(article.summary.substring(0, 200))}...</p>
            ` : ''}

            <div class="article-actions">
                <button onclick="toggleStar(${article.id})" class="btn btn-secondary">
                    ${article.is_starred ? '★' : '☆'} Star
                </button>
                <button onclick="markAsRead(${article.id})" class="btn btn-secondary">
                    ✓ Mark Read
                </button>
                <a href="${article.url}" target="_blank" class="btn btn-primary">
                    Read →
                </a>
            </div>
        </div>
    `).join('');
}

// Render pagination
function renderPagination(totalCount, limit, currentPage) {
    const totalPages = Math.ceil(totalCount / limit);
    const container = document.getElementById('pagination');

    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = `
        <button onclick="loadArticles(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            ← Prev
        </button>
    `;

    for (let i = 1; i <= totalPages; i++) {
        if (
            i === 1 ||
            i === totalPages ||
            (i >= currentPage - 2 && i <= currentPage + 2)
        ) {
            html += `
                <button onclick="loadArticles(${i})" class="${i === currentPage ? 'active' : ''}">
                    ${i}
                </button>
            `;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            html += '<span>...</span>';
        }
    }

    html += `
        <button onclick="loadArticles(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            Next →
        </button>
    `;

    container.innerHTML = html;
}

// Apply filters
function applyFilters() {
    currentFilters.category = document.getElementById('categoryFilter').value;
    currentFilters.source = document.getElementById('sourceFilter').value;
    currentFilters.unread = document.getElementById('unreadFilter').checked;
    currentFilters.starred = document.getElementById('starredFilter').checked;

    loadArticles(1);
}

// Handle search with debounce
let searchTimeout;
function handleSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        currentFilters.search = document.getElementById('searchInput').value;
        loadArticles(1);
    }, 500);
}

// Open article
function openArticle(articleId) {
    window.location.href = `/article/${articleId}`;
}

// Toggle star
async function toggleStar(articleId) {
    try {
        await fetch(`/api/article/${articleId}/star`, { method: 'POST' });
        loadArticles(currentPage);
    } catch (error) {
        console.error('Error toggling star:', error);
    }
}

// Mark as read
async function markAsRead(articleId) {
    try {
        await fetch(`/api/article/${articleId}/read`, { method: 'POST' });
        loadArticles(currentPage);
    } catch (error) {
        console.error('Error marking as read:', error);
    }
}

// Fetch feeds
async function fetchFeeds() {
    try {
        const response = await fetch('/api/fetch', { method: 'POST' });
        const data = await response.json();
        alert('Fetching feeds in background. Refresh in a few moments.');
    } catch (error) {
        console.error('Error fetching feeds:', error);
        alert('Failed to fetch feeds');
    }
}

// Load sources for filter dropdown
async function loadSources() {
    try {
        const response = await fetch('/api/sources');
        const data = await response.json();

        const select = document.getElementById('sourceFilter');
        select.innerHTML = '<option value="">All Sources</option>';

        data.sources.forEach(source => {
            const option = document.createElement('option');
            option.value = source.name;
            option.textContent = source.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading sources:', error);
    }
}

// Settings modal
function showSettings() {
    const modal = document.getElementById('settingsModal');
    modal.classList.add('active');
    loadSourcesSettings();
}

function closeSettings() {
    const modal = document.getElementById('settingsModal');
    modal.classList.remove('active');
}

async function loadSourcesSettings() {
    try {
        const response = await fetch('/api/sources?active_only=false');
        const data = await response.json();

        const container = document.getElementById('sourcesList');
        container.innerHTML = data.sources.map(source => `
            <div class="source-item ${source.is_active ? '' : 'inactive'}">
                <div>
                    <strong>${escapeHtml(source.name)}</strong>
                    <br>
                    <small>${escapeHtml(source.category || 'uncategorized')}</small>
                </div>
                <div>
                    ${source.is_active ? '✓ Active' : '✗ Inactive'}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading sources:', error);
    }
}

// Add new source
async function addSource(event) {
    event.preventDefault();

    const source = {
        name: document.getElementById('sourceName').value,
        url: document.getElementById('sourceUrl').value,
        feed_url: document.getElementById('sourceFeedUrl').value,
        category: document.getElementById('sourceCategory').value,
        source_type: 'rss',
        is_active: 1
    };

    try {
        const response = await fetch('/api/sources', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(source)
        });

        if (response.ok) {
            alert('Source added successfully');
            document.getElementById('addSourceForm').reset();
            loadSourcesSettings();
            loadSources();
        } else {
            alert('Failed to add source');
        }
    } catch (error) {
        console.error('Error adding source:', error);
        alert('Failed to add source');
    }
}

// Cleanup old articles
async function cleanupOldArticles() {
    if (!confirm('Delete all articles older than 30 days (except starred)?')) {
        return;
    }

    try {
        const response = await fetch('/api/articles/cleanup?days=30', {
            method: 'DELETE'
        });
        const data = await response.json();
        alert(`Deleted ${data.deleted} old articles`);
        loadArticles(1);
    } catch (error) {
        console.error('Error cleaning up:', error);
        alert('Failed to cleanup articles');
    }
}

// Utility functions
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function showError(message) {
    const container = document.getElementById('articlesList');
    container.innerHTML = `<div class="loading" style="color: red;">${message}</div>`;
}
