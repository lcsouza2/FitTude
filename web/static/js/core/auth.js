import { exibirMensagem, BASE_URL } from "./utils.js"; //vou usar ainda

class TokenManager {
    constructor() {
        this.sessionToken = null;
        this.refreshPromise = null;
        this.isRefreshing = false;
    }

    setSessionToken(token) {
        this.sessionToken = token;
    }

    getSessionToken() {
        return this.sessionToken;
    }

    clearTokens() {
        this.sessionToken = null;
        this.refreshPromise = null;
        this.isRefreshing = false
    }

    async refreshSessionToken() {
        if (this.isRefreshing) {
            return this.refreshPromise;
        }

        this.isRefreshing = true;
        
        this.refreshPromise = fetch(BASE_URL + "/api/")
    }
}

export class ApiClient {
constructor(protected ) {
    this.protected = protected
    this.baseURL = BASE_URL;
}

async request(endpoint, options = {}) {
    try {


        const finalOptions = {
            credentials: "include",
            Authorization: this.protected ? `Bearer ${localStorage.getItem("token")}` : undefined,
            ...options,
        };

        const response = await fetch(this.baseURL + endpoint, finalOptions);

            let data;
        const bodyType = response.headers.get("Content-Type");

        if (bodyType && bodyType.includes("application/json")) {
            data = await response.json();
        } else {
            data = await response.text();
        }

        return {
            headers: response.headers,
            body: data,
        };
    } catch (error) {
        console.error("[ApiClient] :", error.message);
        throw new Error(error);
    }
}

    get(endpoint) {
        return this.request(endpoint, { method: "GET"});
    }

    post(endpoint, body) {
        return this.request(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        });
    }

    put(endpoint, body) {
        return this.request(endpoint, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        });
    }

    delete(endpoint) {
        return this.request(endpoint, { method: "DELETE" });
    }
}
