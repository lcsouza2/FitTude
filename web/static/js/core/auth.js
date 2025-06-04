import { exibirMensagem } from './utils.js'; //vou usar ainda
export class ApiClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
  }
  async request(endpoint, options = {}) {
    try {
      const finalOptions = {
        credentials: 'include', // essa peça que vc queria?
        ...options
      };

      const response = await fetch(this.baseURL + endpoint, finalOptions);

      if (!response.ok) {
        const msg = await response.text();
        throw new Error(`Erro que deu ${response.status}: ${msg}`);
      }

      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        return await response.json();
      } else {
        return await response.text();
      }

    } catch (error) {
      console.error("[ApiClient] Erro:", error.message);
      throw error; // isso aqui é pra propagar o erro, se não, não consigo tratar no scriptlogin.js ou em lugar nenhum  
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
