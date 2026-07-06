/**
 * ERP Sidebar Controller
 * Manages sidebar collapse, mobile toggle, submenu expansion,
 * active state, and tooltip behavior.
 * 
 * Built from scratch — Original code.
 */
(function () {
    'use strict';

    /* ──────────────────────────────────────────────
       Configuration
       ────────────────────────────────────────────── */
    const STORAGE_KEY_COLLAPSED = 'erp_sidebar_collapsed';
    const MOBILE_BREAKPOINT = 991;

    /* ──────────────────────────────────────────────
       DOM References
       ────────────────────────────────────────────── */
    const body      = document.body;
    const sidebar   = document.getElementById('erpSidebar');
    const overlay   = document.getElementById('sidebarOverlay');
    const toggleBtn = document.getElementById('sidebarToggle');
    const mobileBtn = document.getElementById('mobileMenuToggle');

    if (!sidebar) return;

    /* ──────────────────────────────────────────────
       1. Sidebar Collapse (Desktop)
       ────────────────────────────────────────────── */
    function isMobile() {
        return window.innerWidth <= MOBILE_BREAKPOINT;
    }

    function setCollapsed(collapsed) {
        if (isMobile()) return;
        body.classList.toggle('sidebar-collapsed', collapsed);
        try {
            localStorage.setItem(STORAGE_KEY_COLLAPSED, collapsed ? '1' : '0');
        } catch (_) { /* localStorage unavailable */ }
    }

    function restoreCollapsedState() {
        if (isMobile()) return;
        try {
            const val = localStorage.getItem(STORAGE_KEY_COLLAPSED);
            if (val === '1') {
                body.classList.add('sidebar-collapsed');
            }
        } catch (_) { /* noop */ }
    }

    restoreCollapsedState();

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const isCollapsed = body.classList.contains('sidebar-collapsed');
            setCollapsed(!isCollapsed);
        });
    }

    /* ──────────────────────────────────────────────
       2. Mobile Sidebar (Off-canvas)
       ────────────────────────────────────────────── */
    function openMobileSidebar() {
        sidebar.classList.add('mobile-open');
        if (overlay) overlay.classList.add('active');
        body.style.overflow = 'hidden';
    }

    function closeMobileSidebar() {
        sidebar.classList.remove('mobile-open');
        if (overlay) overlay.classList.remove('active');
        body.style.overflow = '';
    }

    if (mobileBtn) {
        mobileBtn.addEventListener('click', function () {
            if (sidebar.classList.contains('mobile-open')) {
                closeMobileSidebar();
            } else {
                openMobileSidebar();
            }
        });
    }

    if (overlay) {
        overlay.addEventListener('click', closeMobileSidebar);
    }

    /* Close mobile sidebar on resize to desktop */
    window.addEventListener('resize', function () {
        if (!isMobile()) {
            closeMobileSidebar();
        }
    });

    /* ──────────────────────────────────────────────
       3. Submenu Toggle
       ────────────────────────────────────────────── */
    const submenuToggles = document.querySelectorAll('[data-submenu-toggle]');

    submenuToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-submenu-toggle');
            const submenu  = document.getElementById(targetId);
            const arrow    = this.querySelector('.sidebar-menu-arrow');

            if (!submenu) return;

            const isOpen = submenu.classList.contains('open');

            // Optionally close all other submenus (accordion behavior)
            document.querySelectorAll('.sidebar-submenu.open').forEach(function (openMenu) {
                if (openMenu.id !== targetId) {
                    openMenu.classList.remove('open');
                    const parentToggle = document.querySelector('[data-submenu-toggle="' + openMenu.id + '"]');
                    if (parentToggle) {
                        const parentArrow = parentToggle.querySelector('.sidebar-menu-arrow');
                        if (parentArrow) parentArrow.classList.remove('rotated');
                    }
                }
            });

            submenu.classList.toggle('open', !isOpen);
            if (arrow) arrow.classList.toggle('rotated', !isOpen);
        });
    });

    /* ──────────────────────────────────────────────
       4. Active Menu Highlight
       ────────────────────────────────────────────── */
    function setActiveMenu() {
        const currentPath = window.location.pathname;
        const allLinks = sidebar.querySelectorAll('.sidebar-menu-link, .sidebar-submenu-link');

        allLinks.forEach(function (link) {
            const href = link.getAttribute('href');
            if (!href || href === '#') return;

            link.classList.remove('active');

            if (href === currentPath || currentPath.startsWith(href + '/')) {
                link.classList.add('active');

                // Auto-expand parent submenu
                const parentSubmenu = link.closest('.sidebar-submenu');
                if (parentSubmenu) {
                    parentSubmenu.classList.add('open');
                    const parentToggle = document.querySelector('[data-submenu-toggle="' + parentSubmenu.id + '"]');
                    if (parentToggle) {
                        const arrow = parentToggle.querySelector('.sidebar-menu-arrow');
                        if (arrow) arrow.classList.add('rotated');
                    }
                }
            }
        });
    }

    setActiveMenu();

    /* ──────────────────────────────────────────────
       5. Keyboard Shortcut: Toggle Sidebar
       ────────────────────────────────────────────── */
    document.addEventListener('keydown', function (e) {
        // Ctrl + B toggles sidebar on desktop
        if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
            e.preventDefault();
            if (isMobile()) {
                if (sidebar.classList.contains('mobile-open')) {
                    closeMobileSidebar();
                } else {
                    openMobileSidebar();
                }
            } else {
                const isCollapsed = body.classList.contains('sidebar-collapsed');
                setCollapsed(!isCollapsed);
            }
        }

        // Escape closes mobile sidebar
        if (e.key === 'Escape') {
            closeMobileSidebar();
        }
    });

})();
