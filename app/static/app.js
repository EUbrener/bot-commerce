// ==========================================================================
// Mock Database (matching bot-commerce MOCK_PEDIDOS order codes)
// ==========================================================================
const PRODUCTS = [
    {
        id: 1,
        title: "Smartphone Vibe X",
        category: "Celulares",
        price: 3499.00,
        description: "Tela AMOLED de 120Hz, processador topo de linha e acabamento premium em vidro fosco.",
        icon: "fa-solid fa-mobile-screen-button",
        mockOrder: "PED-123456" // Em trânsito
    },
    {
        id: 2,
        title: "Headphone Vibe ANC",
        category: "Áudio",
        price: 899.00,
        description: "Cancelamento de ruído ativo inteligente, drivers acústicos de 40mm e 40h de autonomia.",
        icon: "fa-solid fa-headphones",
        mockOrder: "ORD-555777" // Preparando envio
    },
    {
        id: 3,
        title: "Teclado Mecânico Stealth K",
        category: "Acessórios",
        price: 549.00,
        description: "Switches mecânicos silenciosos, iluminação RGB personalizável e chassi de alumínio aeronáutico.",
        icon: "fa-solid fa-keyboard",
        mockOrder: "PED-456789" // Aguardando pagamento
    },
    {
        id: 4,
        title: "Mouse Gamer Glide M",
        category: "Acessórios",
        price: 299.00,
        description: "Sensor óptico de 16.000 DPI, cabo paracord ultra-leve e switches de alta durabilidade.",
        icon: "fa-solid fa-computer-mouse",
        mockOrder: "PED-111222" // Em separação
    },
    {
        id: 5,
        title: "Carregador Boost Charge 65W",
        category: "Energia",
        price: 189.00,
        description: "Tecnologia GaN de carregamento ultra-rápido de 3 portas para notebook, tablet e celular.",
        icon: "fa-solid fa-plug",
        mockOrder: "PED-789012" // Entregue
    },
    {
        id: 6,
        title: "Smartwatch Orbit Fit",
        category: "Celulares",
        price: 1299.00,
        description: "Monitoramento cardíaco avançado, GPS integrado e bateria de até 14 dias em tela sempre ativa.",
        icon: "fa-regular fa-clock",
        mockOrder: "PED-987654" // Não encontrado no mock
    }
];

// ==========================================================================
// Application State
// ==========================================================================
let cart = [];
let chatHistory = [];
let isChatOpen = false;

// ==========================================================================
// DOM Elements
// ==========================================================================
const productGrid = document.getElementById('product-grid');
const cartDrawer = document.getElementById('cart-drawer');
const cartOverlay = document.getElementById('cart-overlay');
const cartToggleBtn = document.getElementById('cart-toggle-btn');
const cartCloseBtn = document.getElementById('cart-close-btn');
const cartItemsContainer = document.getElementById('cart-items');
const cartBadge = document.getElementById('cart-badge');
const cartSubtotal = document.getElementById('cart-subtotal');
const checkoutBtn = document.getElementById('checkout-btn');

const checkoutModal = document.getElementById('checkout-modal');
const checkoutLoading = document.getElementById('checkout-loading');
const checkoutSuccess = document.getElementById('checkout-success');
const successOrderId = document.getElementById('success-order-id');
const modalCloseBtn = document.getElementById('modal-close-btn');

const chatTrigger = document.getElementById('chat-trigger');
const chatBox = document.getElementById('chat-box');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSendBtn = document.getElementById('chat-send-btn');
const chatSuggestions = document.getElementById('chat-suggestions');

// ==========================================================================
// Initialize Catalog
// ==========================================================================
function renderCatalog() {
    productGrid.innerHTML = PRODUCTS.map(product => `
        <div class="product-card">
            <div class="product-image-container">
                <i class="${product.icon}"></i>
                <div class="product-image-placeholder"></div>
            </div>
            <div class="product-details">
                <span class="product-category">${product.category}</span>
                <h3 class="product-title">${product.title}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-footer">
                    <span class="product-price">R$ ${product.price.toFixed(2).replace('.', ',')}</span>
                    <button class="add-to-cart-btn" onclick="addToCart(${product.id})" title="Adicionar ao Carrinho">
                        <i class="fa-solid fa-plus"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// ==========================================================================
// Shopping Cart Operations
// ==========================================================================
window.addToCart = function(productId) {
    const product = PRODUCTS.find(p => p.id === productId);
    if (!product) return;

    const existingItem = cart.find(item => item.product.id === productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ product, quantity: 1 });
    }

    updateCartUI();
    openCart();
};

function removeFromCart(productId) {
    cart = cart.filter(item => item.product.id !== productId);
    updateCartUI();
}

function adjustQuantity(productId, delta) {
    const item = cart.find(item => item.product.id === productId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
        removeFromCart(productId);
    } else {
        updateCartUI();
    }
}

function updateCartUI() {
    // Update Badge Count
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartBadge.textContent = totalCount;
    cartBadge.style.display = totalCount > 0 ? 'flex' : 'none';

    // Populate Drawer
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="empty-cart-message">
                <i class="fa-solid fa-basket-shopping"></i>
                <p>Seu carrinho está vazio.</p>
            </div>
        `;
        checkoutBtn.disabled = true;
        cartSubtotal.textContent = "R$ 0,00";
    } else {
        cartItemsContainer.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-icon"><i class="${item.product.icon}"></i></div>
                <div class="cart-item-details">
                    <h4>${item.product.title}</h4>
                    <span class="cart-item-price">R$ ${item.product.price.toFixed(2).replace('.', ',')}</span>
                    <div class="cart-item-quantity">
                        <button onclick="adjustQuantity(${item.product.id}, -1)"><i class="fa-solid fa-minus"></i></button>
                        <span>${item.quantity}</span>
                        <button onclick="adjustQuantity(${item.product.id}, 1)"><i class="fa-solid fa-plus"></i></button>
                    </div>
                </div>
                <button class="cart-item-remove" onclick="removeFromCart(${item.product.id})">
                    <i class="fa-regular fa-trash-can"></i>
                </button>
            </div>
        `).join('');
        
        checkoutBtn.disabled = false;
        
        const subtotal = cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
        cartSubtotal.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    }
}

function openCart() {
    cartDrawer.classList.add('open');
    cartOverlay.classList.add('open');
}

function closeCart() {
    cartDrawer.classList.remove('open');
    cartOverlay.classList.remove('open');
}

// ==========================================================================
// Checkout Flow Simulation
// ==========================================================================
checkoutBtn.addEventListener('click', () => {
    closeCart();
    
    // Show Loading
    checkoutModal.classList.add('open');
    checkoutLoading.classList.remove('hidden');
    checkoutSuccess.classList.add('hidden');
    
    // Pick an order ID matching the mock orders for easy conversational testing
    // If multiple distinct products are added, pick one from the cart, otherwise default randomly
    let mockOrder = "PED-123456";
    if (cart.length > 0) {
        mockOrder = cart[0].product.mockOrder;
    }

    setTimeout(() => {
        // Show Success
        checkoutLoading.classList.add('hidden');
        checkoutSuccess.classList.remove('hidden');
        successOrderId.textContent = mockOrder;
        
        // Empty Cart
        cart = [];
        updateCartUI();
    }, 1800);
});

modalCloseBtn.addEventListener('click', () => {
    checkoutModal.classList.remove('open');
});

// ==========================================================================
// Chatbot Client & Service Integration
// ==========================================================================
chatTrigger.addEventListener('click', () => {
    isChatOpen = !isChatOpen;
    chatBox.classList.toggle('open', isChatOpen);
    if (isChatOpen) {
        chatInput.focus();
    }
});

chatClose.addEventListener('click', () => {
    isChatOpen = false;
    chatBox.classList.remove('open');
});

chatSendBtn.addEventListener('click', () => sendUserMessage());
chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        sendUserMessage();
    }
});

// Bind Chips / Suggestions
document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        sendUserMessage(query);
    });
});

async function sendUserMessage(forcedText = null) {
    const text = (forcedText || chatInput.value).trim();
    if (!text) return;

    // Clear input
    chatInput.value = '';

    // Append user message
    appendMessage(text, 'user');

    // Append loading state
    const loadingId = appendLoadingIndicator();

    try {
        // Query FastAPI bot server
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensagem: text,
                historico: chatHistory
            })
        });

        // Remove loading state
        removeLoadingIndicator(loadingId);

        if (!response.ok) {
            throw new Error("Erro de comunicação com o servidor.");
        }

        const data = await response.json();
        
        // Append bot message
        appendMessage(data.resposta, 'bot');

        // Append handover warnings if escalation is requested
        if (data.requer_humano) {
            appendHandoverWarning();
            updateBotStatus(true);
        } else {
            updateBotStatus(false);
        }

        // Add to history
        chatHistory.push([text, data.resposta]);

    } catch (err) {
        removeLoadingIndicator(loadingId);
        appendMessage("Desculpe, tive um problema para me conectar ao servidor. Por favor, tente novamente mais tarde. 🔌", 'bot');
        console.error(err);
    }
}

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    
    // Parse line breaks and simple markdown
    const formattedText = text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');

    msgDiv.innerHTML = `<div class="msg-bubble">${formattedText}</div>`;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
}

function appendLoadingIndicator() {
    const loadingId = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = `message bot`;
    msgDiv.id = loadingId;
    msgDiv.innerHTML = `
        <div class="msg-bubble">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
    return loadingId;
}

function removeLoadingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function appendHandoverWarning() {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'handover-alert';
    alertDiv.innerHTML = `
        <i class="fa-solid fa-headset"></i>
        <span>Atendimento sendo escalado para um atendente humano.</span>
    `;
    chatMessages.appendChild(alertDiv);
    scrollToBottom();
}

function updateBotStatus(isHandedOver) {
    const indicator = document.getElementById('bot-status-indicator');
    const label = document.getElementById('bot-status-label');
    
    if (isHandedOver) {
        indicator.className = 'status-dot transfer';
        label.textContent = 'Suporte Humano solicitado';
    } else {
        indicator.className = 'status-dot online';
        label.textContent = 'Online agora';
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ==========================================================================
// Event Listeners for Drawers
// ==========================================================================
cartToggleBtn.addEventListener('click', openCart);
cartCloseBtn.addEventListener('click', closeCart);
cartOverlay.addEventListener('click', closeCart);

// ==========================================================================
// App Startup
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    renderCatalog();
    updateCartUI();
});

// Bind window-level adjustments
window.removeFromCart = removeFromCart;
window.adjustQuantity = adjustQuantity;
