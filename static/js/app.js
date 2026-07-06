/**
 * ERP Application Controller
 * Manages theme toggle, fullscreen, dropdowns, keyboard shortcuts,
 * and global UI behaviors.
 *
 * Built from scratch — Original code.
 */
(function () {
    'use strict';

    /* ══════════════════════════════════════════════
       1. Theme (Dark / Light Mode)
       ══════════════════════════════════════════════ */
    const STORAGE_KEY_THEME = 'erp_theme';
    const htmlEl = document.documentElement;

    function getStoredTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY_THEME);
        } catch (_) {
            return null;
        }
    }

    function setTheme(theme) {
        htmlEl.setAttribute('data-theme', theme);
        try {
            localStorage.setItem(STORAGE_KEY_THEME, theme);
        } catch (_) { /* noop */ }
    }

    function initTheme() {
        const stored = getStoredTheme();
        if (stored) {
            setTheme(stored);
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setTheme('dark');
        }
    }

    initTheme();

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const current = htmlEl.getAttribute('data-theme');
            setTheme(current === 'dark' ? 'light' : 'dark');
        });
    }

    /* Listen for system preference changes */
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
            if (!getStoredTheme()) {
                setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    /* ══════════════════════════════════════════════
       2. Fullscreen Toggle
       ══════════════════════════════════════════════ */
    const fullscreenBtn = document.getElementById('fullscreenBtn');

    function toggleFullscreen() {
        if (!document.fullscreenElement && !document.webkitFullscreenElement) {
            var el = document.documentElement;
            if (el.requestFullscreen) {
                el.requestFullscreen();
            } else if (el.webkitRequestFullscreen) {
                el.webkitRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            }
        }
    }

    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', toggleFullscreen);
    }

    /* Update fullscreen icon */
    document.addEventListener('fullscreenchange', updateFullscreenIcon);
    document.addEventListener('webkitfullscreenchange', updateFullscreenIcon);

    function updateFullscreenIcon() {
        if (!fullscreenBtn) return;
        var icon = fullscreenBtn.querySelector('i');
        if (!icon) return;
        var isFs = !!(document.fullscreenElement || document.webkitFullscreenElement);
        icon.className = isFs ? 'bi bi-fullscreen-exit' : 'bi bi-arrows-fullscreen';
    }

    /* ══════════════════════════════════════════════
       3. Dropdown Manager (Click-based)
       ══════════════════════════════════════════════ */
    const dropdownTriggers = document.querySelectorAll('[data-dropdown-toggle]');

    dropdownTriggers.forEach(function (trigger) {
        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            var targetId = this.getAttribute('data-dropdown-toggle');
            var dropdown = document.getElementById(targetId);
            if (!dropdown) return;

            var isShown = dropdown.classList.contains('show');

            // Close all other dropdowns first
            closeAllDropdowns();

            if (!isShown) {
                dropdown.classList.add('show');
            }
        });
    });

    function closeAllDropdowns() {
        document.querySelectorAll(
            '.company-dropdown.show, .lang-dropdown.show, .user-dropdown.show, .notification-dropdown.show'
        ).forEach(function (d) {
            d.classList.remove('show');
        });
    }

    /* Close dropdowns when clicking outside */
    document.addEventListener('click', function (e) {
        var isInsideDropdown = e.target.closest(
            '.company-dropdown, .lang-dropdown, .user-dropdown, .notification-dropdown'
        );
        if (!isInsideDropdown) {
            closeAllDropdowns();
        }
    });

    /* Close dropdowns on Escape */
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeAllDropdowns();
        }
    });

    /* ══════════════════════════════════════════════
       4. Search Bar Keyboard Shortcut  (Ctrl+K)
       ══════════════════════════════════════════════ */
    var searchInput = document.getElementById('navbarSearch');
    if (searchInput) {
        document.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    /* ══════════════════════════════════════════════
       5. Company Selector
       ══════════════════════════════════════════════ */
    var companyItems = document.querySelectorAll('.company-dropdown-item');
    companyItems.forEach(function (item) {
        item.addEventListener('click', function () {
            companyItems.forEach(function (ci) {
                ci.classList.remove('active');
            });
            this.classList.add('active');

            var name = this.querySelector('.company-name');
            var btn  = document.querySelector('.company-selector-btn .company-text');
            if (name && btn) {
                btn.textContent = name.textContent;
            }

            closeAllDropdowns();
        });
    });

    /* ══════════════════════════════════════════════
       6. Language Selector
       ══════════════════════════════════════════════ */
    var langItems = document.querySelectorAll('.lang-dropdown-item');
    langItems.forEach(function (item) {
        item.addEventListener('click', function () {
            langItems.forEach(function (li) {
                li.classList.remove('active');
            });
            this.classList.add('active');

            var code = this.getAttribute('data-lang');
            var btn  = document.querySelector('.lang-selector-btn');
            if (code && btn) {
                btn.textContent = code;
            }

            closeAllDropdowns();
        });
    });

    /* ══════════════════════════════════════════════
       7. Notification: Mark All as Read
       ══════════════════════════════════════════════ */
    var markReadBtn = document.querySelector('.notification-mark-read');
    if (markReadBtn) {
        markReadBtn.addEventListener('click', function () {
            document.querySelectorAll('.notification-item.unread').forEach(function (item) {
                item.classList.remove('unread');
            });
            var badge = document.querySelector('.notification-count');
            if (badge) badge.remove();
        });
    }

    /* ══════════════════════════════════════════════
       8. Tooltip: Prevent body scroll on mobile overlay
       ══════════════════════════════════════════════ */
    /* (handled in sidebar.js) */

    /* ══════════════════════════════════════════════
       9. Init Animation: Fade in content
       ══════════════════════════════════════════════ */
    window.addEventListener('DOMContentLoaded', function () {
        var content = document.querySelector('.erp-content');
        if (content) {
            content.classList.add('animate-fade-in');
        }
    });

})();
