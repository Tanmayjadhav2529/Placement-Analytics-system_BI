/* ============================================================
   PLACEMENT ANALYTICS SYSTEM - JavaScript
   Sidebar toggle, password visibility, upload zone, alerts
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Sidebar Toggle (Mobile) ────────────────────────────
    const sidebar = document.getElementById('sidebar');
    const sidebarOpen = document.getElementById('sidebarOpen');
    const sidebarClose = document.getElementById('sidebarClose');

    if (sidebarOpen) {
        sidebarOpen.addEventListener('click', function () {
            sidebar.classList.add('open');
            getOrCreateOverlay().classList.add('active');
        });
    }

    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    function closeSidebar() {
        sidebar.classList.remove('open');
        const overlay = document.querySelector('.sidebar-overlay');
        if (overlay) overlay.classList.remove('active');
    }

    function getOrCreateOverlay() {
        let overlay = document.querySelector('.sidebar-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            document.body.appendChild(overlay);
            overlay.addEventListener('click', closeSidebar);
        }
        return overlay;
    }

    // ─── Password Toggle (Login) ────────────────────────────
    const togglePassword = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('login-password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function () {
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;
            const icon = this.querySelector('i');
            icon.className = type === 'password' ? 'bi bi-eye' : 'bi bi-eye-slash';
        });
    }

    // ─── Upload Zone ────────────────────────────────────────
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = uploadZone ? uploadZone.querySelector('input[type="file"]') : null;
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileRemove = document.getElementById('file-remove');

    if (uploadZone && fileInput) {
        // Drag & drop
        ['dragenter', 'dragover'].forEach(evt => {
            uploadZone.addEventListener(evt, function (e) {
                e.preventDefault();
                uploadZone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(evt => {
            uploadZone.addEventListener(evt, function (e) {
                e.preventDefault();
                uploadZone.classList.remove('dragover');
            });
        });

        uploadZone.addEventListener('drop', function (e) {
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                showFileInfo(e.dataTransfer.files[0].name);
            }
        });

        fileInput.addEventListener('change', function () {
            if (this.files.length) {
                showFileInfo(this.files[0].name);
            }
        });

        if (fileRemove) {
            fileRemove.addEventListener('click', function () {
                fileInput.value = '';
                hideFileInfo();
            });
        }
    }

    function showFileInfo(name) {
        if (fileInfo && fileName) {
            fileName.textContent = name;
            fileInfo.style.display = 'flex';
            if (uploadZone) {
                uploadZone.querySelector('.upload-zone-content').style.display = 'none';
            }
        }
    }

    function hideFileInfo() {
        if (fileInfo) {
            fileInfo.style.display = 'none';
            if (uploadZone) {
                uploadZone.querySelector('.upload-zone-content').style.display = 'block';
            }
        }
    }

    // ─── Auto-dismiss Alerts ────────────────────────────────
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // ─── Active nav link highlighting ───────────────────────
    // Already handled via Django template tags, but add subtle animation
    const activeLink = document.querySelector('.sidebar-nav .nav-link.active');
    if (activeLink) {
        activeLink.style.animation = 'none'; // prevent re-animation on page load
    }

    // ─── Delete confirmation enhancement ────────────────────
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const btn = form.querySelector('.action-btn.delete');
            if (btn) {
                btn.style.opacity = '0.5';
                btn.style.pointerEvents = 'none';
            }
        });
    });

    // ─── Smooth page transitions ────────────────────────────
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.3s ease';
});
