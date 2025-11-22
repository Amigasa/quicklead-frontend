// Основной класс приложения
class QuickLeadManager {
        constructor() {
        this.currentUser = null;
        this.currentPage = 'login';
        this.api = api;
        this.init();
    }

    async init() {
        this.render();
        await this.checkAuth();
    }

    async checkAuth() {
        const savedUser = localStorage.getItem('qlm_user');
        const savedToken = localStorage.getItem('qlm_token');
        
        if (savedUser && savedToken) {
            this.currentUser = JSON.parse(savedUser);
            this.api.token = savedToken;
            this.navigate('dashboard');
        }
    }

    async login(userData) {
        try {
            const result = await this.api.login(userData.username, userData.password);
            this.currentUser = result.user;
            this.navigate('dashboard');
        } catch (error) {
            alert('Ошибка авторизации: ' + error.message);
        }
    }

    async demoLogin(role) {
        const demoCredentials = {
            admin: { username: 'admin', password: 'admin' },
            operator: { username: 'operator', password: 'operator' },
            client: { username: 'client', password: 'client' }
        };
        
        await this.login(demoCredentials[role]);
    }

    navigate(page) {
        this.currentPage = page;
        this.render();
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('qlm_user');
        this.navigate('login');
    }

    render() {
        const app = document.getElementById('app');
        
        if (!this.currentUser) {
            app.innerHTML = this.renderLoginPage();
            this.attachLoginListeners();
            return;
        }

        if (this.currentUser.role === 'admin' || this.currentUser.role === 'operator') {
            app.innerHTML = this.renderAdminLayout();
        } else {
            app.innerHTML = this.renderClientLayout();
        }

        this.attachEventListeners();
    }

    renderLoginPage() {
        return `
            <div class="login-container">
                <div class="login-card">
                    <h1 class="login-title">🔧 QuickLead Manager</h1>
                    <h2 class="login-subtitle">Вход в систему</h2>
                    
                    <form id="loginForm" class="login-form">
                        <div class="form-group">
                            <div class="form-input-with-icon">
                                <span class="icon">👤</span>
                                <input type="text" id="username" class="form-input" placeholder="Введите логин" required>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <div class="form-input-with-icon">
                                <span class="icon">🔒</span>
                                <input type="password" id="password" class="form-input" placeholder="Введите пароль" required>
                            </div>
                        </div>
                        
                        <button type="submit" class="btn btn-primary" style="width: 100%; height: 44px;">
                            🔐 Войти в систему
                        </button>
                    </form>
                    
                    <div class="login-demo-buttons">
                        <button type="button" class="btn btn-secondary" onclick="app.demoLogin('admin')">
                            Демо: Войти как Админ
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="app.demoLogin('operator')">
                            Демо: Войти как Оператор
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="app.demoLogin('client')">
                            Демо: Войти как Клиент
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    attachLoginListeners() {
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                // Для демо используем вход как админ
                this.demoLogin('admin');
            });
        }
    }

    attachEventListeners() {
        // Навигация в админке
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            if (!item.classList.contains('logout-btn')) {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    const page = item.dataset.page;
                    this.navigate(page);
                });
            }
        });
    }
}

// Инициализация приложения
const app = new QuickLeadManager();
window.app = app;