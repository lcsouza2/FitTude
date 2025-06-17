const BASE_URL = 'http://localhost:8000';
class TokenManager {
    constructor() {
        this.tokenExpiresAt = null;
        this.refreshPromise = null;
        this.isRefreshing = false;
    }

    setSessionToken(token, expiresInSeconds) {
        sessionStorage.setItem("session_token", token)
        this.tokenExpiresAt = Date.now() + (expiresInSeconds * 1000);
    }

    getSessionToken() {
        return sessionStorage.getItem("session_token")
    }

    clearTokens() {
        this.tokenExpiresAt = null;
        this.refreshPromise = null;
        this.isRefreshing = false
    }    async refreshSessionToken() {
        if (this.isRefreshing) {
            return this.refreshPromise;
        }

        this.isRefreshing = true;

        try {
            const response = await authApiClient.get('/api/user/renew_token');
            
            if (response.status === 401 || response.status === 402 || response.status === 403) {
                this.redirectToLogin();
            } else {
                const token = response.headers.get('Authorization');
                if (token) {
                    this.setSessionToken(token.split(' ')[1], response.body.expires_in);
                }
            }
            return response;
        } 
        catch (error) {
            this.clearTokens();
            this.redirectToLogin();
            throw error;
        }   
        finally {
            this.isRefreshing = false;
            this.refreshPromise = null;
        }
    }

    validateSessionToken() {
        if (!this.tokenExpiresAt) {
            return false;
        }

        authApiClient.get(BASE_URL + '/api/user/validate_token')
        return true;
    }

    logout() {
        try {
            authApiClient.post(BASE_URL + '/api/user/logout')
            this.clearTokens();
            this.redirectToLogin();
        } catch (error) {
            console.error('Erro no logout:', error);
        }
    }

    redirectToLogin() {
        if (typeof window !== 'undefined') {
            window.location.href = '/login';
        }
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
                headers: {
                    Authorization: this.needsAuth ? `Bearer ${sessionStorage.getItem('session_token')}` : null,
                },
                ...options,
            };

            const response = await fetch(BASE_URL + endpoint, finalOptions);

            //Reveja essa logica ai amigão o problema de reload na pagina ta aqui
            // if (response.status === 401) {
            //     await tokenManager.refreshSessionToken();
            // }

            if (response.status === 403) {
                tokenManager.redirectToLogin();
            }

            const bodyType = response.headers.get('Content-Type');
            let data;

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

    async sget(endpoint) {
        try {
            let response = await this.request(endpoint, { method: 'GET' });
            return response
        } catch (error) {
            console.error("Erro: " + error)
        }

    }

    async post(endpoint, body) {
        return await this.request(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
    }

    async put(endpoint, body) {
        return await this.request(endpoint, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
    }

    async delete(endpoint) {
        return await this.request(endpoint, { method: 'DELETE' });
    }
}

export const tokenManager = new TokenManager();
export const authApiClient = new ApiClient(true);
export const publicApiClient = new ApiClient(false);