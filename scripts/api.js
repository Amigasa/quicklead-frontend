class API {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.token = localStorage.getItem('qlm_token');
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        // Добавляем токен авторизации
        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Авторизация
    async login(username, password) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        this.token = data.access_token;
        localStorage.setItem('qlm_token', this.token);
        localStorage.setItem('qlm_user', JSON.stringify(data.user));
        
        return data;
    }

    // Пользователи
    async getUsers() {
        return await this.request('/users/');
    }

    async createUser(userData) {
        return await this.request('/users/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    // Проекты
    async getProjects() {
        return await this.request('/projects/');
    }

    async createProject(projectData) {
        return await this.request('/projects/', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });
    }

    // Заявки
    async getApplications(filters = {}) {
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) params.append(key, value);
        });
        
        return await this.request(`/applications/?${params}`);
    }

    async createApplication(applicationData) {
        return await this.request('/applications/', {
            method: 'POST',
            body: JSON.stringify(applicationData)
        });
    }

    async getStats() {
        return await this.request('/applications/stats');
    }

    logout() {
        this.token = null;
        localStorage.removeItem('qlm_token');
        localStorage.removeItem('qlm_user');
    }
}

// Создаем глобальный экземпляр API
const api = new API();
window.api = api;