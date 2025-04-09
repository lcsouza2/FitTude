import jwtDecode from 'jwt-decode';
import axios from 'axios';

class AuthManager {
    constructor() {
        // Usando WeakMap para armazenamento mais seguro em memória
        this.tokenStore = new WeakMap();
        this.instanceKey = {};

        // Bind para eventos de visibilidade
        this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Limpa token quando a página fica invisível (troca de aba/minimiza)
        document.addEventListener('visibilitychange', this.handleVisibilityChange);

        // Limpa token antes de fechar/navegar
        window.addEventListener('beforeunload', () => this.clearSession());

        // Detecta inatividade
        this.setupInactivityDetection();
    }

    handleVisibilityChange() {
        if (document.hidden) {
            this.clearSession();
        }
    }

    setupInactivityDetection() {
        let inactivityTimeout;
        const resetTimeout = () => {
            clearTimeout(inactivityTimeout);
            inactivityTimeout = setTimeout(() => this.clearSession(), 15 * 60 * 1000); // 15min
        };

        ['mousedown', 'keydown', 'touchstart', 'mousemove'].forEach(event => {
            document.addEventListener(event, resetTimeout);
        });
    }

    setSessionToken(token) {
        if (!this.validateToken(token)) {
            throw new Error('Token inválido');
        }

        const decoded = jwtDecode(token);
        // Armazena usando WeakMap para melhor segurança
        this.tokenStore.set(this.instanceKey, {
            token,
            expiration: decoded.exp * 1000
        });
    }

    validateToken(token) {
        try {
            const decoded = jwtDecode(token);
            const now = Date.now();

            return (
                decoded.iss === window.location.origin &&
                decoded.aud === 'web-client' &&
                now < decoded.exp * 1000 &&
                now >= decoded.iat * 1000 &&
                decoded.sub
            );
        } catch {
            return false;
        }
    }

    async getValidSessionToken() {
        const session = this.tokenStore.get(this.instanceKey);

        if (!session || Date.now() >= session.expiration - 30000) { // Renova 30s antes
            await this.refreshSessionToken();
        }

        return this.tokenStore.get(this.instanceKey)?.token;
    }

    clearSession() {
        this.tokenStore.delete(this.instanceKey);
    }

    async refreshSessionToken() {
        const source = axios.CancelToken.source();
        const timeoutId = setTimeout(() => source.cancel(), 5000); // 5s timeout

        try {
            const response = await axios({
                method: 'POST',
                url: '/api/user/renew_token',
                withCredentials: true,
                cancelToken: source.token,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const { token } = response.data;
            this.setSessionToken(token);
        } catch (error) {
            if (axios.isCancel(error)) {
                throw new Error('Timeout ao renovar token');
            }
            throw new Error('Falha ao renovar token');
        } finally {
            clearTimeout(timeoutId);
        }
    }
}

// Singleton com Object.freeze para impedir modificações
const authManager = Object.freeze(new AuthManager());

export const secureRequest = async (url, options = {}) => {
    const source = axios.CancelToken.source();
    const timeoutId = setTimeout(() => source.cancel(), 10000); // 10s timeout

    try {
        const token = await authManager.getValidSessionToken();

        const response = await axios({
            ...options,
            url,
            cancelToken: source.token,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${token}`,
                'X-Requested-With': 'XMLHttpRequest'
            },
            withCredentials: true
        });

        return response;
    } catch (error) {
        if (error.response?.status === 401) {
            await authManager.refreshSessionToken();
            return secureRequest(url, options);
        }

        if (axios.isCancel(error)) {
            throw new Error('Request timeout');
        }

        throw error;
    } finally {
        clearTimeout(timeoutId);
    }
};

export default authManager;