// Основной класс приложения
class QuickLeadManager {
    constructor() {
        this.currentUser = null;
        this.currentPage = 'login';
        this.init();
    }

    init() {
        this.render();
        this.checkAuth();
    }

    checkAuth() {
        // Проверка авторизации (заглушка)
        const savedUser = localStorage.getItem('qlm_user');
        if (savedUser) {
            this.currentUser = JSON.parse(savedUser);
            this.navigate('dashboard');
        }
    }

    navigate(page) {
        this.currentPage = page;
        this.render();
    }

    login(userData) {
        // Заглушка авторизации
        this.currentUser = userData;
        localStorage.setItem('qlm_user', JSON.stringify(userData));
        this.navigate('dashboard');
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

    demoLogin(role) {
        const users = {
            admin: { id: 1, name: 'Администратор', role: 'admin', email: 'admin@qlm.ru' },
            operator: { id: 2, name: 'Оператор', role: 'operator', email: 'operator@qlm.ru' },
            client: { id: 3, name: 'Иван Иванов', role: 'client', email: 'client@qlm.ru' }
        };
        
        this.login(users[role]);
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