/**
 * File: main.js
 * Description: Skrip JavaScript utama untuk ATHERZ E-commerce.
 * Author: Gemini
 */

document.addEventListener('DOMContentLoaded', function() {

    // ==== DARK MODE TOGGLE ====
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;

    // Fungsi untuk menerapkan tema berdasarkan preferensi yang tersimpan
    const applyTheme = (theme) => {
        htmlElement.setAttribute('data-bs-theme', theme);
        if (darkModeToggle) {
            darkModeToggle.innerHTML = theme === 'dark' ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-stars-fill"></i>';
        }
    };
    
    // Cek tema yang tersimpan di localStorage saat halaman dimuat
    const savedTheme = localStorage.getItem('atherz_theme') || 'light';
    applyTheme(savedTheme);

    // Event listener untuk tombol toggle
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('atherz_theme', newTheme);
            applyTheme(newTheme);
        });
    }

    // ==== AJAX ADD TO CART ====
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Mencegah form submit standar

            const formData = new FormData(this);
            const productId = formData.get('product_id');
            const quantity = formData.get('quantity');

            fetch(`/add_to_cart/${productId}`, {
                method: 'POST',
                body: new URLSearchParams({ quantity: quantity }), // Kirim data sebagai form-urlencoded
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Tampilkan toast notifikasi sukses
                    showToast(data.message, 'success');
                    
                    // Update jumlah item di badge keranjang
                    const cartBadge = document.getElementById('cart-count-badge');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                        cartBadge.classList.add('animate-pop');
                        setTimeout(() => cartBadge.classList.remove('animate-pop'), 300);
                    }
                    
                    // Tutup modal jika ada
                    const modal = this.closest('.modal');
                    if (modal) {
                        const modalInstance = bootstrap.Modal.getInstance(modal);
                        modalInstance.hide();
                    }

                } else {
                    // Tampilkan toast notifikasi error
                    showToast(data.message || 'An error occurred.', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Could not connect to server.', 'danger');
            });
        });
    });
    // ===== LOGIKA BARU UNTUK LIVE SEARCH =====
    const searchInput = document.getElementById('live-search-input');
    const searchResultsContainer = document.getElementById('live-search-results');

    if (searchInput && searchResultsContainer) {
        searchInput.addEventListener('input', function() {
            const query = this.value;

            if (query.length < 2) {
                searchResultsContainer.innerHTML = '';
                searchResultsContainer.style.display = 'none';
                return;
            }

            fetch(`/live_search?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchResultsContainer.innerHTML = ''; // Kosongkan hasil sebelumnya
                    if (data.length > 0) {
                        searchResultsContainer.style.display = 'block';
                        data.forEach(product => {
                            const itemHTML = `
                                <a href="${product.url}" class="search-result-item">
                                    <img src="${product.image_url}" alt="${product.name}" onerror="this.onerror=null;this.src='[https://placehold.co/50x50/EAEAEA/333333?text=](https://placehold.co/50x50/EAEAEA/333333?text=)...';">
                                    <div class="result-text">
                                        <h6>${product.name}</h6>
                                        <small>${product.category}</small>
                                    </div>
                                </a>
                            `;
                            searchResultsContainer.innerHTML += itemHTML;
                        });
                    } else {
                        searchResultsContainer.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Live search error:', error);
                    searchResultsContainer.style.display = 'none';
                });
        });

        // Sembunyikan hasil pencarian saat mengklik di luar
        document.addEventListener('click', function(event) {
            if (!searchResultsContainer.contains(event.target) && event.target !== searchInput) {
                searchResultsContainer.innerHTML = '';
                searchResultsContainer.style.display = 'none';
            }
        });
        // ===== LOGIKA BARU UNTUK WISHLIST =====
    document.body.addEventListener('click', function(event) {
        const wishlistButton = event.target.closest('.wishlist-btn');
        if (wishlistButton) {
            event.preventDefault();
            const productId = wishlistButton.dataset.productId;

            fetch(`/toggle_wishlist/${productId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => {
                if(response.status === 401){ // Jika pengguna belum login
                    window.location.href = '/login';
                    return null; // Hentikan proses
                }
                return response.json();
            })
            .then(data => {
                if (data) {
                    showToast(data.message, 'success');
                    if (data.status === 'added') {
                        wishlistButton.classList.add('active');
                    } else {
                        wishlistButton.classList.remove('active');
                        // Jika di halaman wishlist, hapus kartu produknya
                        if(window.location.pathname.includes('/profile/wishlist')) {
                            wishlistButton.closest('.col').remove();
                        }
                    }
                }
            })
            .catch(error => console.error('Wishlist error:', error));
        }
    });
    }

    // ==== TOAST NOTIFICATION FUNCTION ====
    function showToast(message, category = 'info') {
        // Hapus toast lama jika ada
        const oldToastContainer = document.getElementById('toast-container');
        if(oldToastContainer) {
            oldToastContainer.remove();
        }

        // Buat container toast baru
        const toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1056'; // Di atas modal

        const toastHTML = `
            <div class="toast show align-items-center text-bg-${category} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        toastContainer.innerHTML = toastHTML;
        document.body.appendChild(toastContainer);

        const toastElement = toastContainer.querySelector('.toast');
        const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
        toast.show();
    }
});
