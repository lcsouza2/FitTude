const BASE_URL = 'http://sapecaplay.ddns.net:8000';

class TokenManager {
    constructor() {
        this.tokenExpiresAt = null;
        this.refreshPromise = null;
        this.isRefreshing = false;
    }

    setSessionToken(token, expiresInSeconds) {
        if (!token) return;
        sessionStorage.setItem("session_token", token);
        this.tokenExpiresAt = Date.now() + (expiresInSeconds * 1000);
    }

    getSessionToken() {
        return sessionStorage.getItem("session_token");
    }

    clearTokens() {
        sessionStorage.removeItem("session_token");
        this.tokenExpiresAt = null;
        this.refreshPromise = null;
        this.isRefreshing = false;
    }    

    async refreshSessionToken() {
        if (this.isRefreshing) {
            return this.refreshPromise;
        }

        this.isRefreshing = true;

        try {
            const response = await fetch(`${BASE_URL}/api/user/renew_token`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.getSessionToken()}`
                },
                credentials: 'include'
            });
            
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

        return true;
    }

    async logout() {
        try {
            await fetch(`${BASE_URL}/api/user/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.getSessionToken()}`
                },
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
}

export class ApiClient {
    constructor(needsAuth) {
        this.needsAuth = needsAuth;
    }

    async request(endpoint, options = {}) {
        // Configura headers básicos
        const baseHeaders = {
            'Content-Type': 'application/json'
        };

        // Adiciona token se necessário
        if (this.needsAuth) {
            const token = sessionStorage.getItem('session_token');
            if (token) {
                baseHeaders['Authorization'] = `Bearer ${token}`;
            }
        }

        // Mescla headers da requisição com os headers base
        const requestHeaders = {
            ...baseHeaders,
            ...(options.headers || {})
        };

        // Configura opções da requisição
        const requestOptions = {
            ...options,
            headers: requestHeaders,
            credentials: 'include' // Importante para cookies e auth
        };

        try {
            let response = await fetch(BASE_URL + endpoint, requestOptions);

            // Se receber 401 e precisar de auth, tenta renovar o token
            if (response.status === 401 && this.needsAuth) {
                const token = sessionStorage.getItem('session_token');
                if (token) {
                    try {
                        await tokenManager.refreshSessionToken();
                        requestHeaders['Authorization'] = `Bearer ${token}`;
                        console.log(requestHeaders);
                        response = await fetch(BASE_URL + endpoint, {
                        ...requestOptions,
                        headers: requestHeaders
                    });
                    } catch (error) {
                        console.error('Erro ao renovar token:', error);
                        tokenManager.redirectToLogin();
                        throw error;
                    }
                }
            }

            // Se ainda receber 401 ou 403 após tentar renovar, redireciona para login
            if (response.status === 401 || response.status === 403) {
                tokenManager.redirectToLogin();
                throw new Error('Não autorizado');
            }

            // Processa a resposta
            let data;
            const contentType = response.headers.get('Content-Type');
            
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            return {
                ok: response.ok,
                status: response.status,
                statusText: response.statusText,
                headers: response.headers,
                body: data
            };

        } catch (error) {
            console.error('[ApiClient]:', error);
            throw error;
        }
    }

    async get(endpoint, headers) {
        return this.request(endpoint, { 
            method: 'GET',
            headers: { ...headers }

        });
    }

    async post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body)
        });
    }

    async put(endpoint, body) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(body)
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

export const tokenManager = new TokenManager();
export const authApiClient = new ApiClient(true);
export const publicApiClient = new ApiClient(false);
