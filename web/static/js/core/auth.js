import { exibirMensagem } from './utils.js';
export class ApiClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
    }
  async request(endpoint, options = {}) {
    try {
      const response = await fetch(this.baseURL + endpoint, options);
      
      if (!response.ok) {
        const errorText = await response.text(); // lê a resposta mesmo em erro
        throw new Error(`Erro ${response.status}: ${errorText}`);
      }

      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        return await response.json();
      } else {
        return await response.text();
      }
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
