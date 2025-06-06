import { exibirMensagem } from './utils.js'; //vou usar ainda
export class ApiClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
  }
  async request(endpoint, options = {}) {
    try {
      const finalOptions = {
        credentials: 'include',
        ...options
      };

      const response = await fetch(this.baseURL + endpoint, finalOptions);

      if (!response.ok) {
        const msg = await response.text();
        throw new Error(`Erro que deu ${response.status}: ${msg}`);
      }
     
      return {
        headers: response.headers,
        body: response.json()
      };

    } catch (error) {
      console.error("[ApiClient] Erro:", error.message);
      throw error;
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
