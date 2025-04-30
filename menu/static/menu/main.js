// menu/static/menu/main.js
document.addEventListener('DOMContentLoaded', function() {

    // --- Мобилдик менюну ачуу/жабуу (CSS классы менен) ---
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-navigation');

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            // 'is-open' классын .main-navigation'га кошуп/алып салуу
            mainNav.classList.toggle('is-open');
            // Кнопканын өзүнө да активдүү класс кошуп/алып салуу (мис: 'X' белгиси үчүн)
            menuToggle.classList.toggle('is-active');
        });
    }

    // --- Dropdown менюну иштетүү (мисал - клик менен) ---
    const dropdownToggles = document.querySelectorAll('.main-navigation .nav-item.dropdown > a'); // Dropdown шилтемелерин тандоо

    dropdownToggles.forEach(toggle => {
        // Эгер шилтеме '#' болсо гана клик иштесин (башка баракка өтпөш үчүн)
        // Же болбосо, preventDefault ар дайым керек
        if (toggle.getAttribute('href') === '#') {
            toggle.addEventListener('click', function(e) {
                e.preventDefault(); // Шилтеменин демейки аракетин токтотуу (# барактын башына жылдырбайт)
                const dropdownItem = this.closest('.nav-item.dropdown'); // Ата-эне .dropdown элементин табуу
                if (dropdownItem) {
                    dropdownItem.classList.toggle('is-open'); // Ата-энеге is-open классын кошуу/алуу
                }
            });
        }
    });

    // Башка жерди басканда ачык dropdown'ду жабуу (кошумча, татаалыраак)
    document.addEventListener('click', function(event) {
        // Эгер клик менюнун сыртында болсо жана ал .dropdown > a эмес болсо
        if (!mainNav.contains(event.target) && !event.target.matches('.menu-toggle')) {
             // Бардык ачык dropdown'дорду жабуу
             document.querySelectorAll('.main-navigation .nav-item.dropdown.is-open').forEach(openDropdown => {
                 openDropdown.classList.remove('is-open');
             });
             // Эгер мобилдик меню ачык болсо, аны да жабуу (керек болсо)
             // if (mainNav.classList.contains('is-open')) {
             //     mainNav.classList.remove('is-open');
             //     menuToggle.classList.remove('is-active');
             // }
        }
    });


    // --- Django messages жабуу ---
    const closeButtons = document.querySelectorAll('.messages .alert .close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });

    // --- Экрандын өлчөмү өзгөргөндө ---
    window.addEventListener('resize', function() {
        // Эгер экран чоңойсо жана мобилдик меню ачык болсо, аны жабуу жана inline стилди тазалоо
        if (window.innerWidth > 768) {
            if (mainNav && mainNav.classList.contains('is-open')) {
                mainNav.classList.remove('is-open');
                // Кнопканын is-active классын да алып салуу
                if (menuToggle && menuToggle.classList.contains('is-active')) {
                    menuToggle.classList.remove('is-active');
                }
            }
             // Чоң экранда ачык dropdown'дорду жабуу (керек болсо)
            // document.querySelectorAll('.main-navigation .nav-item.dropdown.is-open').forEach(openDropdown => {
            //     openDropdown.classList.remove('is-open');
            // });
        }
    });

});
// menu/static/menu/main.js
// ТОЛУК КОД (Мобилдик меню, Dropdown, Messages, Сактоо AJAX, Корзина AJAX)

document.addEventListener('DOMContentLoaded', function() {

    // --- CSRF токенин алуу функциясы ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // --- Жалпы AJAX жөнөтүү функциясы (милдеттүү эмес, бирок кодун кыскартат) ---
    function sendAjaxRequest(url, data, buttonElement) {
         // Кнопканы убактылуу өчүрүп туруу (кайра-кайра басууну алдын алуу)
         if (buttonElement) buttonElement.disabled = true;

        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams(data)
        })
        .then(response => {
            if (!response.ok) {
                 return response.json().then(err => {
                     throw new Error(err.message || `HTTP error! status: ${response.status}`);
                 }).catch(() => {
                     throw new Error(`HTTP error! status: ${response.status}`);
                 });
            }
            return response.json();
        })
        .finally(() => {
            // Кнопканы кайра иштетүү
             if (buttonElement) buttonElement.disabled = false;
        });
    }

    // --- Мобилдик меню ---
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-navigation');
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('is-open');
            menuToggle.classList.toggle('is-active');
        });
    }

    // --- Dropdown меню ---
    const dropdownToggles = document.querySelectorAll('.main-navigation .nav-item.dropdown > a');
    dropdownToggles.forEach(toggle => {
        if (toggle.getAttribute('href') === '#') {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                const dropdownItem = this.closest('.nav-item.dropdown');
                if (dropdownItem) dropdownItem.classList.toggle('is-open');
            });
        }
    });
    document.addEventListener('click', function(event) {
        if (mainNav && !mainNav.contains(event.target) && !event.target.matches('.menu-toggle')) {
             document.querySelectorAll('.main-navigation .nav-item.dropdown.is-open').forEach(openDropdown => {
                 openDropdown.classList.remove('is-open');
             });
             // Мобилдик менюну да жабуу (керек болсо)
             // if (mainNav.classList.contains('is-open')) { ... }
        }
    });

    // --- Django messages жабуу ---
    const closeButtons = document.querySelectorAll('.messages .alert .close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() { this.parentElement.style.display = 'none'; });
    });

    // --- Экран өлчөмү өзгөргөндө ---
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            if (mainNav && mainNav.classList.contains('is-open')) {
                mainNav.classList.remove('is-open');
                if (menuToggle && menuToggle.classList.contains('is-active')) {
                    menuToggle.classList.remove('is-active');
                }
            }
        }
    });

    // ==================== AJAX МЕНЕН САКТОО/ӨЧҮРҮҮ ====================
    document.querySelectorAll('.btn-save-toggle').forEach(button => {
        if (button.tagName === 'A') return; // Логин болбогондо шилтеме болот

        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            let currentAction = this.dataset.action;
            const url = window.toggleSaveUrl; // base.html'ден келет
            const buttonElement = this; // Кнопканы өчүрүп/күйгүзүү үчүн

            sendAjaxRequest(url, { 'product_id': productId, 'action': currentAction }, buttonElement)
            .then(data => {
                if (data.status === 'ok') {
                    const icon = button.querySelector('i');
                    const saveTextSpan = button.querySelector('.save-text');
                    if (data.saved) {
                        button.classList.add('saved');
                        button.dataset.action = 'unsave';
                        button.title = window.jsTranslations.removeSaved;
                        if (icon) { icon.classList.remove('far'); icon.classList.add('fas'); }
                        if (saveTextSpan) saveTextSpan.textContent = window.jsTranslations.saved;
                    } else {
                        button.classList.remove('saved');
                        button.dataset.action = 'save';
                        button.title = window.jsTranslations.save;
                        if (icon) { icon.classList.remove('fas'); icon.classList.add('far'); }
                        if (saveTextSpan) saveTextSpan.textContent = window.jsTranslations.save;
                    }
                    // alert(data.message); // Ийгилик билдирүүсү (милдеттүү эмес)
                } else {
                    alert(window.jsTranslations.errorOccurred + " " + data.message);
                }
            })
            .catch(error => {
                console.error('Save Toggle Error:', error);
                alert(window.jsTranslations.operationError);
            });
        });
    });
    // ==================== САКТОО AJAX АЯГЫ ====================


    // ==================== КОРЗИНАНЫ AJAX МЕНЕН ЖАҢЫРТУУ ====================

    // Жалпы сумма жана шапкадагы эсептегичти жаңыртчу функция
    function updateCartTotals(totalPrice, itemCount) {
        const totalPriceElement = document.getElementById('cart-total-price');
        if (totalPriceElement) {
            totalPriceElement.textContent = '$' + parseFloat(totalPrice).toFixed(2);
        }
        const cartBadge = document.querySelector('.cart-badge'); // Бул классты шапкадагы span'га КОШУУ КЕРЕК
        if (cartBadge) {
            if (itemCount > 0) {
                cartBadge.textContent = itemCount;
                cartBadge.style.display = 'inline-block';
            } else {
                cartBadge.style.display = 'none';
            }
        }
         // Шапкадагы өзүнчө корзина эмес, жалпы санды көрсөткөн жерди да жаңылоо (мисалы)
        const globalCartCount = document.getElementById('global-cart-count'); // Ушундай ID'лүү элемент түзүү керек
        if (globalCartCount) {
            globalCartCount.textContent = itemCount > 0 ? itemCount : '';
        }
    }

    // Корзина бош экенин көрсөтүүчү функция
    function showEmptyCartMessage() {
        const cartContainerWrapper = document.getElementById('cart-container-wrapper');
        if (cartContainerWrapper) {
            // Бул жерде котормо тегдери иштебейт, ошондуктан англисче жазабыз
            // же base.html аркылуу бул тексттерди да JS'ке өткөрүп берүү керек
            cartContainerWrapper.innerHTML = `
                <div class="cart-empty" style="text-align: center; padding: 80px 20px;">
                     <i class="fas fa-shopping-cart" style="font-size: 6em; color: var(--border-color); margin-bottom: 30px;"></i>
                     <h2>Your cart is empty</h2>
                     <p style="font-size: 1.1em; color: var(--text-secondary); margin-bottom: 30px;">
                         Browse our menu to find something you like.
                     </p>
                     <a href="{% url 'menu:menu_list' %}" class="btn btn-primary btn-lg"> {# Бул URL да JS'те иштебейт, түз жазыш керек #}
                     <a href="/menu/" class="btn btn-primary btn-lg">
                         <i class="fas fa-utensils" style="margin-right: 8px;"></i> View Menu
                     </a>
                </div>`;
        }
    }

    // --- Санды өзгөртүүчү кнопкалар үчүн Event Listener ---
    // Эскертүү: Бул listener барак жүктөлгөндө ГАНА кошулат. Эгер корзина
    // динамикалык түрдө жаңыртылса (мис. HTMX менен), event delegation керек болот.
    document.querySelectorAll('.btn-quantity-change').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const change = this.dataset.change;
            const url = "{% url 'menu:update_cart_item' %}"; // Бул да base.html'ге чыгышы керек
            // const url = window.updateCartUrl; // Мисалы
            const buttonElement = this;

             sendAjaxRequest(url, { 'product_id': productId, 'change': change }, buttonElement)
             .then(data => {
                if (data.status === 'ok') {
                    const quantitySpan = document.getElementById(`item-quantity-${productId}`);
                    const itemTotalPriceSpan = document.getElementById(`item-total-price-${productId}`);
                    const itemRow = document.getElementById(`cart-item-row-${productId}`);

                    if (data.item_removed) {
                        if (itemRow) itemRow.remove();
                    } else {
                        if (quantitySpan) quantitySpan.textContent = data.new_quantity;
                        if (itemTotalPriceSpan) itemTotalPriceSpan.textContent = '$' + parseFloat(data.item_total_price).toFixed(2);
                    }
                    updateCartTotals(data.total_cart_price, data.cart_item_count);
                    if (data.cart_item_count === 0) showEmptyCartMessage();
                } else {
                    alert(window.jsTranslations.errorOccurred + " " + data.message); // Котормону колдонуу
                }
             })
             .catch(error => {
                 console.error('Update Cart Error:', error);
                 alert(window.jsTranslations.operationError); // Котормону колдонуу
             });
        });
    });

    // --- Өчүрүү кнопкасы үчүн Event Listener ---
    document.querySelectorAll('.btn-remove-item').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const url = "{% url 'menu:remove_from_cart' %}"; // Бул да base.html'ге чыгышы керек
            // const url = window.removeFromCartUrl; // Мисалы
            const buttonElement = this;

            // Котормону JS'тен алуу кыйыныраак, түз жазалы
            if (!confirm("Бул товарды корзинадан чын эле өчүрөсүзбү?")) {
                 return;
            }

            sendAjaxRequest(url, { 'product_id': productId }, buttonElement)
            .then(data => {
                if (data.status === 'ok') {
                    const itemRow = document.getElementById(`cart-item-row-${productId}`);
                    if (itemRow) itemRow.remove();
                    updateCartTotals(data.total_cart_price, data.cart_item_count);
                    if (data.cart_is_empty) showEmptyCartMessage();
                } else {
                     alert(window.jsTranslations.errorOccurred + " " + data.message);
                }
            })
            .catch(error => {
                 console.error('Remove Item Error:', error);
                 alert(window.jsTranslations.operationError);
            });
        });
    });
    // ==================== КОРЗИНА AJAX АЯГЫ ====================


}); // DOMContentLoaded аягы


// menu/static/menu/main.js
// ТОЛУК КОД (Мобилдик меню, Dropdown, Messages, САКТОО AJAX, КОРЗИНА AJAX)

document.addEventListener('DOMContentLoaded', function() {

    // --- CSRF токенин алуу функциясы ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken') || window.csrfToken; // Cookie'ден же window'дон алуу

    // --- Жалпы AJAX жөнөтүү функциясы ---
    function sendAjaxRequest(url, data, buttonElement) {
         if (buttonElement) buttonElement.disabled = true; // Кнопканы өчүрүү
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken, // CSRF токенин кошуу
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams(data)
        })
        .then(response => {
            // Кнопканы кайра иштетүү (жооп келгенде)
            if (buttonElement) buttonElement.disabled = false;
            if (!response.ok) {
                 return response.json().then(err => {
                     throw new Error(err.message || `HTTP error! status: ${response.status}`);
                 }).catch(() => {
                     throw new Error(`HTTP error! status: ${response.status}`);
                 });
            }
            return response.json();
        })
        .catch(error => { // fetch() өзү ката берсе (мис, тармак катасы)
             if (buttonElement) buttonElement.disabled = false; // Кнопканы кайра иштетүү
             console.error('Fetch/Network Error:', error);
             // Котормону window'дон алуу
             alert(window.jsTranslations.operationError || 'Operation failed due to a network error.');
             throw error; // Ката чынжырын улантуу
         });
    }

    // --- Мобилдик меню ---
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-navigation');
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('is-open');
            menuToggle.classList.toggle('is-active');
        });
    }

    // --- Dropdown меню ---
    const dropdownToggles = document.querySelectorAll('.main-navigation .nav-item.dropdown > a');
    dropdownToggles.forEach(toggle => {
        if (toggle.getAttribute('href') === '#') {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                const dropdownItem = this.closest('.nav-item.dropdown');
                if (dropdownItem) {
                    // Башка ачык dropdown'дорду жабуу (милдеттүү эмес)
                    document.querySelectorAll('.main-navigation .nav-item.dropdown.is-open').forEach(openDrop => {
                        if (openDrop !== dropdownItem) {
                            openDrop.classList.remove('is-open');
                        }
                    });
                    dropdownItem.classList.toggle('is-open');
                }
            });
        }
    });
    // Башка жерди басканда dropdown'ду жабуу
    document.addEventListener('click', function(event) {
        const targetElement = event.target;
        // Эгер клик менюнун же dropdown ачкычтын сыртында болсо
        if (mainNav && !mainNav.contains(targetElement) && !targetElement.closest('.nav-item.dropdown > a')) {
             document.querySelectorAll('.main-navigation .nav-item.dropdown.is-open').forEach(openDropdown => {
                 openDropdown.classList.remove('is-open');
             });
        }
        // Эгер клик менюнун сыртында болсо, мобилдик менюну да жабуу
        if (mainNav && mainNav.classList.contains('is-open') && !mainNav.contains(targetElement) && !targetElement.matches('.menu-toggle')) {
             mainNav.classList.remove('is-open');
             if (menuToggle) menuToggle.classList.remove('is-active');
        }
    });


    // --- Django messages жабуу ---
    const closeButtons = document.querySelectorAll('.messages .alert .close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() { this.parentElement.style.display = 'none'; });
    });

    // --- Экран өлчөмү өзгөргөндө ---
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            if (mainNav && mainNav.classList.contains('is-open')) {
                mainNav.classList.remove('is-open');
                if (menuToggle && menuToggle.classList.contains('is-active')) {
                    menuToggle.classList.remove('is-active');
                }
            }
        }
    });

    // ==================== AJAX МЕНЕН САКТОО/ӨЧҮРҮҮ ====================
    // Бул функция барак жүктөлгөндө да, AJAX аркылуу жаңы контент кошулганда да
    // иштеши үчүн event delegation колдонуу жакшыраак, бирок азыр жөнөкөй кылалы.
    function addSaveToggleListeners() {
        document.querySelectorAll('.btn-save-toggle').forEach(button => {
            // Эгер мурунтан listener кошулган болсо, кайра кошпойбуз
            if (button.hasAttribute('data-listener-added')) return;

            if (button.tagName === 'A') { // Логин болбогондо шилтеме болот
                 button.setAttribute('data-listener-added', 'true');
                 return;
            }

            button.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.dataset.productId;
                let currentAction = this.dataset.action;
                // URL'ди глобалдык өзгөрмөдөн алуу
                const url = window.toggleSaveUrl;
                const buttonElement = this;

                // --- sendAjaxRequest колдонуу ---
                sendAjaxRequest(url, { 'product_id': productId, 'action': currentAction }, buttonElement)
                .then(data => {
                    if (data.status === 'ok') {
                        const icon = buttonElement.querySelector('i');
                        const saveTextSpan = buttonElement.querySelector('.save-text'); // Деталдуу барак үчүн
                        if (data.saved) { // Эгер сакталды деп жооп келсе
                            buttonElement.classList.add('saved');
                            buttonElement.dataset.action = 'unsave';
                            buttonElement.title = window.jsTranslations.removeSaved;
                            if (icon) { icon.classList.remove('far'); icon.classList.add('fas'); }
                            if (saveTextSpan) saveTextSpan.textContent = window.jsTranslations.saved;
                        } else { // Эгер өчүрүлдү деп жооп келсе
                            buttonElement.classList.remove('saved');
                            buttonElement.dataset.action = 'save';
                            buttonElement.title = window.jsTranslations.save;
                            if (icon) { icon.classList.remove('fas'); icon.classList.add('far'); }
                            if (saveTextSpan) saveTextSpan.textContent = window.jsTranslations.save;
                        }
                        // Ийгиликтүү билдирүүнү көрсөтүү (мисалы, кичинекей alert)
                        // showTemporaryMessage(data.message, 'success'); // Бул функцияны түзүү керек
                    } else {
                        // Ката билдирүүсүн көрсөтүү
                         alert(window.jsTranslations.errorOccurred + " " + data.message);
                    }
                })
                .catch(error => {
                    // Тармак катасы же башка fetch катасы
                    // sendAjaxRequest ичинде alert мурунтан эле бар
                    console.error('Save Toggle Error:', error);
                });
            });
            // Listener кошулганын белгилөө
            button.setAttribute('data-listener-added', 'true');
        });
    }
    // Барак жүктөлгөндө listener'лерди кошуу
    addSaveToggleListeners();
    // ==================== САКТОО AJAX АЯГЫ ====================


    // ==================== КОРЗИНАНЫ AJAX МЕНЕН ЖАҢЫРТУУ ====================

    // Жалпы сумма жана шапкадагы эсептегичти жаңыртчу функция
    function updateCartTotals(totalPrice, itemCount) {
        const totalPriceElement = document.getElementById('cart-total-price');
        if (totalPriceElement) {
            totalPriceElement.textContent = '$' + parseFloat(totalPrice).toFixed(2);
        }
        const cartBadge = document.querySelector('.cart-badge'); // Шапкадагы эсептегич
        if (cartBadge) {
            if (itemCount > 0) {
                cartBadge.textContent = itemCount;
                cartBadge.style.display = 'inline-block';
            } else {
                // Эгер сан 0 болсо, жашыруунун ордуна 0 кылып коёлу, же жашыралы
                cartBadge.textContent = '0';
                cartBadge.style.display = 'none'; // Жашыруу
            }
        }
        // Башка жерлердеги санды да жаңылоо (милдеттүү эмес)
        // const globalCartCount = document.getElementById('global-cart-count');
        // if (globalCartCount) { globalCartCount.textContent = itemCount > 0 ? itemCount : ''; }
    }

    // Корзина бош экенин көрсөтүүчү функция
    function showEmptyCartMessage() {
        const cartContainerWrapper = document.getElementById('cart-container-wrapper');
        if (cartContainerWrapper) {
            // Котормолорду глобалдык өзгөрмөдөн алуу
            const title = window.jsTranslations.emptyCartTitle || "Your cart is empty";
            const text = window.jsTranslations.emptyCartText || "Browse our menu to find something you like.";
            const btnText = window.jsTranslations.viewMenuBtn || "View Menu";
            const menuUrl = window.viewMenuUrl || "/menu/"; // base.html'ден

            cartContainerWrapper.innerHTML = `
                <div class="cart-empty" style="text-align: center; padding: 80px 20px;">
                     <i class="fas fa-shopping-cart" style="font-size: 6em; color: var(--border-color); margin-bottom: 30px;"></i>
                     <h2>${title}</h2>
                     <p style="font-size: 1.1em; color: var(--text-secondary); margin-bottom: 30px;">
                         ${text}
                     </p>
                     <a href="${menuUrl}" class="btn btn-primary btn-lg">
                         <i class="fas fa-utensils" style="margin-right: 8px;"></i> ${btnText}
                     </a>
                </div>`;
        }
    }

    // --- Санды өзгөртүүчү жана Өчүрүүчү кнопкалар үчүн Event Delegation ---
    // Биз түздөн-түз кнопкаларга эмес, алардын ата-энесине (мис. таблицага же контейнерге)
    // listener кошобуз, бул AJAX аркылуу жаңы элементтер кошулганда да иштейт.
    const cartTableBody = document.querySelector('.cart-table tbody'); // Таблицанын негизги бөлүгү
    const cartContainerWrapper = document.getElementById('cart-container-wrapper'); // Же жалпы контейнер

    // Эгер корзина таблицасы бар болсо, ага listener кошуу
    if (cartTableBody) {
        cartTableBody.addEventListener('click', function(e) {
            const targetButton = e.target.closest('button'); // Басылган элемент кнопкабы же ичиндеги иконкабы текшерүү

            // Санды өзгөртүүчү кнопка басылса
            if (targetButton && targetButton.classList.contains('btn-quantity-change')) {
                e.preventDefault();
                const productId = targetButton.dataset.productId;
                const change = targetButton.dataset.change;
                const url = window.updateCartUrl; // Глобалдык өзгөрмөдөн
                const buttonElement = targetButton;

                sendAjaxRequest(url, { 'product_id': productId, 'change': change }, buttonElement)
                .then(data => {
                    if (data.status === 'ok') {
                        const quantitySpan = document.getElementById(`item-quantity-${productId}`);
                        const itemTotalPriceSpan = document.getElementById(`item-total-price-${productId}`);
                        const itemRow = document.getElementById(`cart-item-row-${productId}`);

                        if (data.item_removed) {
                            if (itemRow) itemRow.remove(); // Катарды өчүрүү
                        } else {
                            if (quantitySpan) quantitySpan.textContent = data.new_quantity;
                            if (itemTotalPriceSpan) itemTotalPriceSpan.textContent = '$' + parseFloat(data.item_total_price).toFixed(2); // Бул жерде да сомго алмаштыруу керек болот
                        }
                        updateCartTotals(data.total_cart_price, data.cart_item_count);
                        if (data.cart_item_count === 0) showEmptyCartMessage();
                    } else {
                        alert(window.jsTranslations.errorOccurred + " " + data.message);
                    }
                })
                .catch(error => { console.error('Update Cart Error:', error); /* alert бар */ });
            }

            // Өчүрүү кнопкасы басылса
            else if (targetButton && targetButton.classList.contains('btn-remove-item')) {
                e.preventDefault();
                const productId = targetButton.dataset.productId;
                const url = window.removeFromCartUrl; // Глобалдык өзгөрмөдөн
                const buttonElement = targetButton;

                if (!confirm(window.jsTranslations.confirmRemoveItem || "Бул товарды корзинадан чын эле өчүрөсүзбү?")) {
                    return;
                }

                sendAjaxRequest(url, { 'product_id': productId }, buttonElement)
                .then(data => {
                    if (data.status === 'ok') {
                        const itemRow = document.getElementById(`cart-item-row-${productId}`);
                        if (itemRow) itemRow.remove();
                        updateCartTotals(data.total_cart_price, data.cart_item_count);
                        if (data.cart_is_empty) showEmptyCartMessage();
                    } else {
                         alert(window.jsTranslations.errorOccurred + " " + data.message);
                    }
                })
                .catch(error => { console.error('Remove Item Error:', error); /* alert бар */ });
            }
        });
    }
    // ==================== КОРЗИНА AJAX АЯГЫ ====================


}); // DOMContentLoaded аягы