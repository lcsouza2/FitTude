const BASE_URL = 'http://localhost:8000';
class TokenManager {
    constructor() {
        this.sessionToken = null;
        this.tokenExpiresAt = null;
        this.refreshPromise = null;
        this.isRefreshing = false;
    }

    setSessionToken(token, expiresInSeconds) {
        this.sessionToken = token;
        this.tokenExpiresAt = Date.now() + (expiresInSeconds * 1000);
    }

    getSessionToken() {
        return this.sessionToken;
    }

    clearTokens() {
        this.sessionToken = null;
        this.tokenExpiresAt = null;
        this.refreshPromise = null;
        this.isRefreshing = false
    }

    async refreshSessionToken() {
        if (this.isRefreshing) {
            return this.refreshPromise;
        }

        this.isRefreshing = true;

        this.refreshPromise = fetch(BASE_URL + '/api/user/renew_token', {
            credentials: 'include',
        })
            .then(async response => {
                if (!response.ok) {
                    throw new Error('Falha ao renovar token');
                }

                this.setAccessToken(response.headers.get('Authorization'));
                return this.refreshPromise;
            })
            .catch(error => {
                this.clearTokens();
                this.redirectToLogin();
                throw error;
            })
            .finally(() => {
                this.isRefreshing = false;
                this.refreshPromise = null;
            });
        return this.refreshPromise;
    }

    async logout() {
        try {
            await fetch('/api/user/logout', {
                credentials: 'include'
            });
        } catch (error) {
            console.error('Erro no logout:', error);
        } finally {
            this.clearTokens();
            this.redirectToLogin();
        }
    }

    redirectToLogin() {
        if (typeof window !== 'undefined') {
            window.location.href = '/login';
        }
    }

    isTokenExpiringSoon(thresholdMinutes = 5) {
        if (!this.accessToken || !this.tokenExpiresAt) {
            return true;
        }

        const now = Date.now();
        const threshold = thresholdMinutes * 60 * 1000;

            return (this.tokenExpiresAt - now) < threshold;
    }
}


export class ApiClient {
    constructor(needsAuth) {
        this.needsAuth = needsAuth
        BASE_URL;
    }

    async request(endpoint, options = {}) {
        try {

            const finalOptions = {
                credentials: 'include',
                Authorization: this.needsAuth ? `Bearer ${localStorage.getItem('token')}` : undefined,
                ...options,
            };

            const response = await fetch(BASE_URL + endpoint, finalOptions);

            let data;
            const bodyType = response.headers.get('Content-Type');

            if (bodyType && bodyType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            return {
                ok: response.ok,
                status: response.status,
                statusText: response.statusText,
                headers: response.headers,
                body: data,
            };
        } catch (error) {
            console.error('[ApiClient] :', error.message);
            throw new Error(error);
        }
    }

    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
    }

    put(endpoint, body) {
        return this.request(endpoint, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
    }

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

export const tokenManager = new TokenManager();
export const authApiClient = new ApiClient(true);
export const publicApiClient = new ApiClient(false);