// Расширяем основной класс для админ-функциональности
class AdminManager {
    constructor() {
        this.modals = {};
    }

    renderAdminDashboard() {
        return `
            <div class="dashboard">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">1,248</div>
                        <div class="stat-label">Всего заявок</div>
                        <div class="stat-icon">📨</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">45</div>
                        <div class="stat-label">Новые заявки</div>
                        <div class="stat-icon">🆕</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">83</div>
                        <div class="stat-label">В работе</div>
                        <div class="stat-icon">⚡</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">156</div>
                        <div class="stat-label">Успешно</div>
                        <div class="stat-icon">✅</div>
                    </div>
                </div>
                
                <div class="dashboard-charts">
                    <div class="chart-card">
                        <h3>📈 Поступление заявок за 7 дней</h3>
                        <div class="chart-placeholder">
                            График загрузки заявок
                        </div>
                    </div>
                </div>
                
                <div class="recent-leads">
                    <div class="card">
                        <h3>Последние заявки</h3>
                        <div class="leads-list">
                            <div class="lead-item">
                                <span class="lead-name">Иван Иванов</span>
                                <span class="lead-contact">+7 (999) 123-45-67</span>
                                <span class="badge badge-primary">Новая</span>
                            </div>
                            <div class="lead-item">
                                <span class="lead-name">Мария Петрова</span>
                                <span class="lead-contact">maria@email.com</span>
                                <span class="badge badge-warning">В работе</span>
                            </div>
                            <div class="lead-item">
                                <span class="lead-name">Петр Сидоров</span>
                                <span class="lead-contact">+7 (999) 987-65-43</span>
                                <span class="badge badge-success">Успешно</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderAdminProjects() {
        return `
            <div class="projects-page">
                <div class="page-header">
                    <button class="btn btn-primary" onclick="adminManager.showCreateProjectModal()">
                        ➕ Создать проект
                    </button>
                    
                    <div class="search-box">
                        <input type="text" class="form-input" placeholder="Поиск проектов...">
                        <span class="search-icon">🔍</span>
                    </div>
                </div>
                
                <div class="projects-grid">
                    <div class="project-card">
                        <h3 class="project-name">Рога и копыта</h3>
                        <p class="project-api">API-ключ: <code>qlm_***abc</code></p>
                        <p class="project-stats">Заявок: 128</p>
                        <div class="project-actions">
                            <button class="btn-icon" title="Редактировать">✏️</button>
                            <button class="btn-icon btn-danger" title="Удалить">🗑️</button>
                        </div>
                    </div>
                    
                    <div class="project-card">
                        <h3 class="project-name">СтройГрад</h3>
                        <p class="project-api">API-ключ: <code>qlm_***def</code></p>
                        <p class="project-stats">Заявок: 45</p>
                        <div class="project-actions">
                            <button class="btn-icon" title="Редактировать">✏️</button>
                            <button class="btn-icon btn-danger" title="Удалить">🗑️</button>
                        </div>
                    </div>
                    
                    <div class="project-card">
                        <h3 class="project-name">ТехноМир</h3>
                        <p class="project-api">API-ключ: <code>qlm_***ghi</code></p>
                        <p class="project-stats">Заявок: 83</p>
                        <div class="project-actions">
                            <button class="btn-icon" title="Редактировать">✏️</button>
                            <button class="btn-icon btn-danger" title="Удалить">🗑️</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderAdminUsers() {
        return `
            <div class="users-page">
                <div class="page-header">
                    <button class="btn btn-primary" onclick="adminManager.showCreateUserModal()">
                        👤 Добавить пользователя
                    </button>
                </div>
                
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Имя</th>
                            <th>Email</th>
                            <th>Роль</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Иван Иванов</td>
                            <td>admin@qlm.ru</td>
                            <td><span class="badge badge-danger">Админ</span></td>
                            <td>
                                <button class="btn-icon" title="Редактировать">✏️</button>
                                <button class="btn-icon btn-danger" title="Удалить">🗑️</button>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>Мария Петрова</td>
                            <td>maria@qlm.ru</td>
                            <td><span class="badge badge-primary">Оператор</span></td>
                            <td>
                                <button class="btn-icon" title="Редактировать">✏️</button>
                                <button class="btn-icon btn-danger" title="Удалить">🗑️</button>
                            </td>
                        </tr>
                        <tr>
                            <td>3</td>
                            <td>Петр Сидоров</td>
                            <td>petr@qlm.ru</td>
                            <td><span class="badge badge-primary">Оператор</span></td>
                            <td>
                                <button class="btn-icon" title="Редактировать">✏️</button>
                                <button class="btn-icon btn-danger" title="Удалить">🗑️</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    }

    renderAdminLeads() {
        return `
            <div class="leads-page">
                <div class="page-header">
                    <div class="page-actions">
                        <button class="btn btn-secondary">📊 Статистика</button>
                        <button class="btn btn-primary" onclick="adminManager.showExportModal()">📤 Выгрузить</button>
                    </div>
                </div>
                
                <div class="filters-card card">
                    <div class="filters-row">
                        <div class="filter-group">
                            <label class="form-label">Проект</label>
                            <select class="form-input">
                                <option>Все проекты</option>
                                <option>Рога и копыта</option>
                                <option>СтройГрад</option>
                                <option>ТехноМир</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label class="form-label">Статус</label>
                            <select class="form-input">
                                <option>Все статусы</option>
                                <option>Новая</option>
                                <option>В работе</option>
                                <option>Перезвонить</option>
                                <option>Успешно</option>
                                <option>Неудача</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label class="form-label">Период</label>
                            <div style="display: flex; gap: 8px; align-items: center;">
                                <input type="date" class="form-input" style="flex: 1;">
                                <span>-</span>
                                <input type="date" class="form-input" style="flex: 1;">
                            </div>
                        </div>
                    </div>
                    
                    <div class="filters-actions">
                        <button class="btn btn-primary">Применить фильтры</button>
                        <button class="btn btn-secondary">Сбросить</button>
                    </div>
                </div>
                
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Имя</th>
                            <th>Телефон</th>
                            <th>Email</th>
                            <th>Проект</th>
                            <th>Статус</th>
                            <th>Дата</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>4582</td>
                            <td>Иван Иванов</td>
                            <td>+7 (999) 123-45-67</td>
                            <td>ivan@mail.ru</td>
                            <td>Рога и копыта</td>
                            <td><span class="badge badge-warning">В работе</span></td>
                            <td>15.12.2023</td>
                            <td>
                                <button class="btn-icon" title="Просмотр">👁️</button>
                            </td>
                        </tr>
                        <tr>
                            <td>4581</td>
                            <td>Мария Петрова</td>
                            <td>maria@email.com</td>
                            <td>maria@email.com</td>
                            <td>СтройГрад</td>
                            <td><span class="badge badge-success">Успешно</span></td>
                            <td>14.12.2023</td>
                            <td>
                                <button class="btn-icon" title="Просмотр">👁️</button>
                            </td>
                        </tr>
                        <tr>
                            <td>4580</td>
                            <td>Петр Сидоров</td>
                            <td>+7 (999) 987-65-43</td>
                            <td>petr@mail.ru</td>
                            <td>ТехноМир</td>
                            <td><span class="badge badge-danger">Неудача</span></td>
                            <td>13.12.2023</td>
                            <td>
                                <button class="btn-icon" title="Просмотр">👁️</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    }

    renderAdminSettings() {
        return `
            <div class="settings-page">
                <div class="card">
                    <h3>⚙ Настройки системы</h3>
                    <p>Здесь будут настройки системы...</p>
                </div>
            </div>
        `;
    }

    showCreateProjectModal() {
        const modalHtml = `
            <div class="modal-overlay" onclick="adminManager.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3>➕ Создать проект</h3>
                    </div>
                    <div class="modal-body">
                        <form id="createProjectForm">
                            <div class="form-group">
                                <label class="form-label">Название проекта</label>
                                <input type="text" class="form-input" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Описание</label>
                                <textarea class="form-input" rows="3"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="adminManager.closeModal()">Отмена</button>
                        <button class="btn btn-primary" onclick="adminManager.createProject()">Создать</button>
                    </div>
                </div>
            </div>
        `;
        
        this.showModal(modalHtml);
    }

    showCreateUserModal() {
        const modalHtml = `
            <div class="modal-overlay" onclick="adminManager.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3>👤 Добавить пользователя</h3>
                    </div>
                    <div class="modal-body">
                        <form id="createUserForm">
                            <div class="form-group">
                                <label class="form-label">Имя</label>
                                <input type="text" class="form-input" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-input" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Роль</label>
                                <select class="form-input" required>
                                    <option value="">Выберите роль</option>
                                    <option value="admin">Администратор</option>
                                    <option value="operator">Оператор</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Пароль</label>
                                <input type="password" class="form-input" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="adminManager.closeModal()">Отмена</button>
                        <button class="btn btn-primary" onclick="adminManager.createUser()">Создать</button>
                    </div>
                </div>
            </div>
        `;
        
        this.showModal(modalHtml);
    }

    showExportModal() {
        const modalHtml = `
            <div class="modal-overlay" onclick="adminManager.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3>📤 Выгрузка данных</h3>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label class="form-label">Формат</label>
                            <div>
                                <label style="display: inline-flex; align-items: center; gap: 8px; margin-right: 20px;">
                                    <input type="radio" name="format" value="csv" checked> CSV
                                </label>
                                <label style="display: inline-flex; align-items: center; gap: 8px;">
                                    <input type="radio" name="format" value="xlsx"> XLSX
                                </label>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Включать поля:</label>
                            <div style="display: flex; flex-direction: column; gap: 8px;">
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox" checked> Основные данные (имя, телефон, email)
                                </label>
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox" checked> UTM-метки
                                </label>
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox"> Дополнительные поля
                                </label>
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox" checked> Даты и время
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="adminManager.closeModal()">Отмена</button>
                        <button class="btn btn-primary" onclick="adminManager.exportData()">✅ Выгрузить данные</button>
                    </div>
                </div>
            </div>
        `;
        
        this.showModal(modalHtml);
    }

    showModal(html) {
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = html;
        document.body.appendChild(modalContainer);
        this.modals.current = modalContainer;
    }

    closeModal() {
        if (this.modals.current) {
            document.body.removeChild(this.modals.current);
            this.modals.current = null;
        }
    }

    createProject() {
        alert('Проект создан!');
        this.closeModal();
    }

    createUser() {
        alert('Пользователь создан!');
        this.closeModal();
    }

    exportData() {
        alert('Данные выгружены!');
        this.closeModal();
    }
}

// Инициализация админ-менеджера
const adminManager = new AdminManager();
window.adminManager = adminManager;

// Расширяем основной класс
Object.assign(QuickLeadManager.prototype, {
    renderAdminDashboard: adminManager.renderAdminDashboard.bind(adminManager),
    renderAdminProjects: adminManager.renderAdminProjects.bind(adminManager),
    renderAdminUsers: adminManager.renderAdminUsers.bind(adminManager),
    renderAdminLeads: adminManager.renderAdminLeads.bind(adminManager),
    renderAdminSettings: adminManager.renderAdminSettings.bind(adminManager)
});