document.addEventListener('DOMContentLoaded', function() {

    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;

    const applyTheme = (theme) => {
        htmlElement.setAttribute('data-bs-theme', theme);
        if (darkModeToggle) {
            darkModeToggle.innerHTML = theme === 'dark' ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-stars-fill"></i>';
        }
    };
    
    const savedTheme = localStorage.getItem('atherz_theme') || 'light';
    applyTheme(savedTheme);

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('atherz_theme', newTheme);
            applyTheme(newTheme);
        });
    }

    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); 

            const formData = new FormData(this);
            const productId = formData.get('product_id');
            const quantity = formData.get('quantity');

            fetch(`/add_to_cart/${productId}`, {
                method: 'POST',
                body: new URLSearchParams({ quantity: quantity }), 
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message, 'success');
                    
                    const cartBadge = document.getElementById('cart-count-badge');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                        cartBadge.classList.add('animate-pop');
                        setTimeout(() => cartBadge.classList.remove('animate-pop'), 300);
                    }
                    
                    const modal = this.closest('.modal');
                    if (modal) {
                        const modalInstance = bootstrap.Modal.getInstance(modal);
                        modalInstance.hide();
                    }

                } else {
                    showToast(data.message || 'An error occurred.', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Could not connect to server.', 'danger');
            });
        });
    });
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
                    searchResultsContainer.innerHTML = ''; 
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

        document.addEventListener('click', function(event) {
            if (!searchResultsContainer.contains(event.target) && event.target !== searchInput) {
                searchResultsContainer.innerHTML = '';
                searchResultsContainer.style.display = 'none';
            }
        });
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
                if(response.status === 401){ 
                    window.location.href = '/login';
                    return null; 
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
        const navbar = document.getElementById('mainNavbar');

    if (navbar) {
        const handleScroll = () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        };

        window.addEventListener('scroll', handleScroll);
        handleScroll();
    }
    

    function showToast(message, category = 'info') {
        const oldToastContainer = document.getElementById('toast-container');
        if(oldToastContainer) {
            oldToastContainer.remove();
        }

        const toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1056'; 

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
