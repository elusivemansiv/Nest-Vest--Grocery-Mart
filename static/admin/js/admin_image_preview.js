/**
 * Modern Django Admin - Global Image Preview Enhancer
 * Automatically detects and displays live image previews for:
 * - All ModelAdmin ImageFields / FileFields with images (e.g., Product, Category, Vendor, SiteSettings, etc.)
 * - Tabular & Stacked Inlines (e.g., Product gallery images)
 * - Immediate live preview upon file selection (URL.createObjectURL)
 * - Graceful handling of "Clear" deletion checkbox
 */

(function () {
    'use strict';

    const IMAGE_EXTENSIONS = /\.(jpg|jpeg|png|webp|gif|svg|avif|bmp|ico)(\?.*)?$/i;

    function isImageField(input, link) {
        if (input.getAttribute('accept') && input.getAttribute('accept').includes('image')) {
            return true;
        }
        if (link && (IMAGE_EXTENSIONS.test(link.href) || link.href.includes('/media/'))) {
            return true;
        }
        const fieldName = (input.name || input.id || '').toLowerCase();
        if (/image|photo|picture|logo|avatar|banner|icon|thumb|cover/i.test(fieldName)) {
            return true;
        }
        const parentField = input.closest('.form-group, .form-row, td, .field-box');
        if (parentField && /image|photo|picture|logo|avatar|banner|icon|thumb|cover/i.test(parentField.className)) {
            return true;
        }
        return false;
    }

    function setupImagePreview(fileInput) {
        if (!fileInput || fileInput.dataset.previewInitialized) return;

        const container = fileInput.closest('.file-upload') || fileInput.parentElement;
        if (!container) return;

        const existingLink = container.querySelector('a');
        if (!isImageField(fileInput, existingLink)) return;

        fileInput.dataset.previewInitialized = 'true';

        // Check if inside inline table
        const isInline = !!fileInput.closest('td, .tabular');

        // Create or find preview container
        let previewCard = container.querySelector('.admin-image-preview-card');
        if (!previewCard) {
            previewCard = document.createElement('div');
            previewCard.className = 'admin-image-preview-card' + (isInline ? ' is-inline' : '');

            const frame = document.createElement('div');
            frame.className = 'admin-image-preview-frame';

            const img = document.createElement('img');
            img.className = 'admin-image-preview-img';
            img.alt = 'Image Preview';

            const badge = document.createElement('span');
            badge.className = 'admin-image-preview-badge';

            frame.appendChild(img);
            frame.appendChild(badge);
            previewCard.appendChild(frame);

            // Action / Full-view link
            const actions = document.createElement('div');
            actions.className = 'admin-image-preview-actions';
            const viewLink = document.createElement('a');
            viewLink.className = 'admin-image-preview-zoom-btn';
            viewLink.target = '_blank';
            viewLink.rel = 'noopener noreferrer';
            viewLink.innerHTML = '<i class="fas fa-search-plus"></i> View Full';
            actions.appendChild(viewLink);
            previewCard.appendChild(actions);

            // Container layout styling
            container.classList.add('admin-image-field-container');
            container.appendChild(previewCard);
        }

        const img = previewCard.querySelector('.admin-image-preview-img');
        const badge = previewCard.querySelector('.admin-image-preview-badge');
        const viewLink = previewCard.querySelector('.admin-image-preview-zoom-btn');
        let initialSrc = '';

        if (existingLink && existingLink.href) {
            initialSrc = existingLink.href;
            img.src = initialSrc;
            if (viewLink) viewLink.href = initialSrc;
            badge.textContent = 'Current';
            badge.className = 'admin-image-preview-badge badge-current';
            previewCard.style.display = 'inline-flex';
        } else {
            previewCard.style.display = 'none';
        }

        // Live preview on file selection
        fileInput.addEventListener('change', function () {
            const file = fileInput.files && fileInput.files[0];
            if (file && (file.type.startsWith('image/') || IMAGE_EXTENSIONS.test(file.name))) {
                const objectUrl = URL.createObjectURL(file);
                img.src = objectUrl;
                if (viewLink) viewLink.href = objectUrl;
                badge.textContent = 'New (Ready)';
                badge.className = 'admin-image-preview-badge badge-new';
                previewCard.style.display = 'inline-flex';
                previewCard.classList.remove('is-cleared');
            } else if (!file && initialSrc) {
                img.src = initialSrc;
                if (viewLink) viewLink.href = initialSrc;
                badge.textContent = 'Current';
                badge.className = 'admin-image-preview-badge badge-current';
                previewCard.style.display = 'inline-flex';
                previewCard.classList.remove('is-cleared');
            } else if (!file) {
                previewCard.style.display = 'none';
            }
        });

        // Listen for Clear checkbox
        const clearCheckbox = container.querySelector('input[type="checkbox"][name$="-clear"]');
        if (clearCheckbox) {
            clearCheckbox.addEventListener('change', function () {
                if (clearCheckbox.checked) {
                    previewCard.classList.add('is-cleared');
                    badge.textContent = 'Marked for Deletion';
                    badge.className = 'admin-image-preview-badge badge-danger';
                } else {
                    previewCard.classList.remove('is-cleared');
                    badge.textContent = 'Current';
                    badge.className = 'admin-image-preview-badge badge-current';
                }
            });
        }
    }

    function initAllPreviews() {
        const inputs = document.querySelectorAll('input[type="file"]');
        inputs.forEach(setupImagePreview);
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAllPreviews);
    } else {
        initAllPreviews();
    }

    // Support dynamic inline additions (e.g. Django formset:added)
    if (window.django && window.django.jQuery) {
        window.django.jQuery(document).on('formset:added', function (event, $row) {
            if ($row && $row.length) {
                $row[0].querySelectorAll('input[type="file"]').forEach(setupImagePreview);
            }
        });
    }

    // MutationObserver fallback for dynamically injected rows or tab switching
    const observer = new MutationObserver(function (mutations) {
        for (let mutation of mutations) {
            for (let node of mutation.addedNodes) {
                if (node.nodeType === 1) {
                    if (node.tagName === 'INPUT' && node.type === 'file') {
                        setupImagePreview(node);
                    } else if (node.querySelectorAll) {
                        node.querySelectorAll('input[type="file"]').forEach(setupImagePreview);
                    }
                }
            }
        }
    });

    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    }
})();
