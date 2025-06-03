import { exibirMensagem } from './utils.js';
export class ApiClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
    }
  async request(endpoint, options = {}) {
      const response = await fetch(this.baseURL + endpoint, options).then

      if (response.ok) {
          console.log("200 OK:", response);
      }
      else if(response.status == 409) {
          exibirMensagem('Email já cadastrado.', 'danger');
          throw new Error(`Erro ${response.status}: ${errorText}`);
      }
      else if (response.status == 401) {
          exibirMensagem('Email ou senha inválidos.', 'danger');
          throw new Error(`Erro ${response.status}: ${errorText}`);

      }else if (response.status == 404) {
          exibirMensagem('Falha na comunição com o servido', 'danger');
          throw new Error(`Erro ${response.status}: ${errorText}`);
      }   
      else if (response.status == 500) {
          exibirMensagem('Erro interno do servidor. Tente novamente mais tarde.', 'danger');
          throw new Error(`Erro ${response.status}: ${errorText}`);
      }
      else {
          return response.json();
      }
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
          return await response.json();
      } else {
          return await response.text(); // caso não seja JSON
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
