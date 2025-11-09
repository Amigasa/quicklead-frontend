// Класс для клиентской функциональности
class ClientManager {
    constructor() {
        this.currentLeadId = null;
        this.requests = [
            {
                id: 4582,
                title: "Ремонт кухни",
                client: "Мария Петрова",
                status: "warning",
                statusText: "В работе",
                date: "15.12.2023",
                description: "Необходимо заменить столешницу и установить новую мойку"
            },
            {
                id: 4581,
                title: "Установка окон",
                client: "Иван Сидоров",
                status: "success",
                statusText: "Успешно",
                date: "14.12.2023",
                description: "Установка пластиковых окон в квартире"
            },
            {
                id: 4580,
                title: "Консультация",
                client: "Анна Ковалева",
                status: "danger",
                statusText: "Неудача",
                date: "13.12.2023",
                description: "Консультация по дизайну интерьера"
            }
        ];
    }

    renderClientLayout() {
        const pageContent = this.getClientPageContent();
        
        return `
            <div class="client-layout">
                <header class="client-header">
                    <nav class="client-nav">
                        <div class="client-logo">🚀 QuickLead</div>
                        <div class="client-nav-links">
                            <a href="#" class="client-nav-link ${app.currentPage === 'client-request' ? 'active' : ''}" 
                               onclick="app.navigate('client-request')">Оставить заявку</a>
                            <a href="#" class="client-nav-link ${app.currentPage === 'client-status' ? 'active' : ''}" 
                               onclick="app.navigate('client-status')">Отслеживание</a>
                            <a href="#" class="client-nav-link ${app.currentPage === 'client-requests' ? 'active' : ''}" 
                               onclick="app.navigate('client-requests')">Мои заявки</a>
                            <span style="color: var(--gray-600);">👤 ${app.currentUser.name}</span>
                            <a href="#" class="client-nav-link" onclick="app.logout()">Выйти</a>
                        </div>
                    </nav>
                </header>
                
                <main class="client-main">
                    ${pageContent}
                </main>
                
                ${app.currentPage === 'client-requests' ? `
                    <button class="new-request-btn" onclick="app.navigate('client-request')" title="Новая заявка">
                        +
                    </button>
                ` : ''}
            </div>
        `;
    }

    getClientPageContent() {
        switch (app.currentPage) {
            case 'client-request':
                return this.renderClientRequestForm();
            case 'client-status':
                return this.renderClientStatus();
            case 'client-requests':
                return this.renderClientRequests();
            default:
                return this.renderClientRequestForm();
        }
    }

    renderClientRequestForm() {
        return `
            <div class="request-form-container">
                <div class="request-form-card">
                    <h1 class="request-title">🚀 Оставить заявку</h1>
                    <p class="request-subtitle">Ваши контактные данные</p>
                    
                    <form id="clientRequestForm" class="request-form">
                        <div class="form-group">
                            <div class="form-input-with-icon">
                                <span class="icon">👤</span>
                                <input type="text" class="form-input" placeholder="Ваше имя" required>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <div class="form-input-with-icon">
                                <span class="icon">📞</span>
                                <input type="tel" class="form-input" placeholder="+7 (___) ___-____" required>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <div class="form-input-with-icon">
                                <span class="icon">📧</span>
                                <input type="email" class="form-input" placeholder="your@email.com">
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <div class="form-input-with-icon">
                                <span class="icon">💬</span>
                                <textarea class="form-input" placeholder="Опишите вашу проблему или вопрос" rows="4" required></textarea>
                            </div>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            📨 ОТПРАВИТЬ ЗАЯВКУ
                        </button>
                    </form>
                    
                    <p class="form-info">
                        После отправки вы получите номер для отслеживания заявки
                    </p>
                </div>
            </div>
        `;
    }

    renderClientStatus() {
        return `
            <div class="tracking-container">
                <div class="tracking-card">
                    <h2 class="tracking-title">📋 Отслеживание заявки</h2>
                    
                    <div class="tracking-search">
                        <input type="text" class="form-input" id="leadSearchInput" placeholder="Например: 4582">
                        <button class="btn btn-primary" onclick="clientManager.searchLead()">🔍 Найти</button>
                    </div>
                    
                    <div id="leadDetails" class="hidden">
                        <div class="lead-details">
                            <div class="lead-number">Заявка #4582 от 15.12.2023</div>
                            <div class="lead-info">Иван Иванов • +7 (999) 123-45-67</div>
                        </div>
                        
                        <h3 style="margin-bottom: 16px;">Статус заявки</h3>
                        <div class="status-timeline">
                            <div class="status-item completed">
                                <div class="status-dot"></div>
                                <div class="status-content">
                                    <div class="status-name">Новая</div>
                                    <div class="status-date">15.12 10:30</div>
                                </div>
                            </div>
                            <div class="status-item completed">
                                <div class="status-dot"></div>
                                <div class="status-content">
                                    <div class="status-name">В работе</div>
                                    <div class="status-date">15.12 11:15</div>
                                </div>
                            </div>
                            <div class="status-item current">
                                <div class="status-dot"></div>
                                <div class="status-content">
                                    <div class="status-name">Перезвонить</div>
                                    <div class="status-date">--.-- --:--</div>
                                </div>
                            </div>
                            <div class="status-item">
                                <div class="status-dot"></div>
                                <div class="status-content">
                                    <div class="status-name">Успешно</div>
                                    <div class="status-date">--.-- --:--</div>
                                </div>
                            </div>
                            <div class="status-item">
                                <div class="status-dot"></div>
                                <div class="status-content">
                                    <div class="status-name">Неудача</div>
                                    <div class="status-date">--.-- --:--</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="operator-comment">
                            <h4>Комментарий оператора:</h4>
                            "Уточните удобное время для звонка"
                        </div>
                    </div>
                    
                    <div id="noLeadFound" class="hidden" style="text-align: center; padding: 40px; color: var(--gray-500);">
                        Введите номер заявки для отслеживания
                    </div>
                </div>
            </div>
        `;
    }

    renderClientRequests() {
        const requestsHtml = this.requests.map(request => `
            <div class="request-item ${request.status}" onclick="clientManager.showRequestDetails(${request.id})">
                <div class="request-header">
                    <div class="request-id">#${request.id} 
                        <span class="request-status">
                            <span class="status-dot-sm" style="background: var(--${request.status})"></span>
                            ${request.statusText}
                        </span>
                    </div>
                </div>
                <div class="request-description">${request.title} • ${request.client}</div>
                <div class="request-date">Обновлено: ${request.date}</div>
            </div>
        `).join('');

        return `
            <div class="my-requests-container">
                <h1 style="margin-bottom: 24px; font-size: 28px;">📂 Мои заявки</h1>
                
                <div class="requests-filters">
                    <select class="form-input" style="min-width: 200px;">
                        <option>Все заявки</option>
                        <option>Новые</option>
                        <option>В работе</option>
                        <option>Завершенные</option>
                    </select>
                    
                    <div class="search-box">
                        <input type="text" class="form-input" placeholder="Поиск по заявкам...">
                        <span class="search-icon">🔍</span>
                    </div>
                </div>
                
                <div class="requests-list">
                    ${requestsHtml}
                </div>
            </div>
        `;
    }

    searchLead() {
        const input = document.getElementById('leadSearchInput');
        const leadDetails = document.getElementById('leadDetails');
        const noLeadFound = document.getElementById('noLeadFound');
        
        if (input.value.trim() === '4582') {
            leadDetails.classList.remove('hidden');
            noLeadFound.classList.add('hidden');
        } else {
            leadDetails.classList.add('hidden');
            noLeadFound.classList.remove('hidden');
            noLeadFound.innerHTML = 'Заявка не найдена. Проверьте номер и попробуйте снова.';
        }
    }

    showRequestDetails(requestId) {
        const request = this.requests.find(r => r.id === requestId);
        if (request) {
            alert(`Детали заявки #${request.id}\n\nУслуга: ${request.title}\nСтатус: ${request.statusText}\nОписание: ${request.description}`);
        }
    }

    attachClientEventListeners() {
        // Обработчик формы заявки
        const requestForm = document.getElementById('clientRequestForm');
        if (requestForm) {
            requestForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitRequest();
            });
        }

        // Обработчик поиска заявки по Enter
        const searchInput = document.getElementById('leadSearchInput');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.searchLead();
                }
            });
        }
    }

    submitRequest() {
        const form = document.getElementById('clientRequestForm');
        const formData = new FormData(form);
        
        // Имитация отправки заявки
        const newRequestId = Math.floor(Math.random() * 1000) + 4000;
        
        alert(`Заявка #${newRequestId} успешно отправлена!\n\nСкоро с вами свяжется наш специалист.`);
        
        // Переход к отслеживанию
        app.navigate('client-status');
        
        // Автозаполнение номера заявки в поле поиска
        setTimeout(() => {
            const searchInput = document.getElementById('leadSearchInput');
            if (searchInput) {
                searchInput.value = newRequestId;
                this.searchLead();
            }
        }, 100);
    }
}

// Инициализация клиент-менеджера
const clientManager = new ClientManager();
window.clientManager = clientManager;

// Расширяем основной класс для клиентской части
Object.assign(QuickLeadManager.prototype, {
    renderClientLayout: clientManager.renderClientLayout.bind(clientManager),
    renderClientRequestForm: clientManager.renderClientRequestForm.bind(clientManager),
    renderClientStatus: clientManager.renderClientStatus.bind(clientManager),
    renderClientRequests: clientManager.renderClientRequests.bind(clientManager)
});

// Дополняем основной класс для полной функциональности
const originalRender = QuickLeadManager.prototype.render;
QuickLeadManager.prototype.render = function() {
    originalRender.call(this);
    
    if (this.currentUser && (this.currentUser.role === 'client')) {
        clientManager.attachClientEventListeners();
    }
};

const originalAttachEventListeners = QuickLeadManager.prototype.attachEventListeners;
QuickLeadManager.prototype.attachEventListeners = function() {
    originalAttachEventListeners.call(this);
    
    if (this.currentUser && (this.currentUser.role === 'client')) {
        clientManager.attachClientEventListeners();
    }
};