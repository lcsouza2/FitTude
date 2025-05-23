import {  } from './utils.js';
export class ApiClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
    }
  async request(endpoint, options = {}) {
    try {
        const response = await fetch(this.baseURL + endpoint, options);

        if (!response.ok) {
            const errorText = await response.text(); // tenta pegar mensagem do servidor
            throw new Error(`Erro ${response.status}: ${errorText}`);
        }
        
        if (response.ok) {
            console.log("200 OK:", response);
        }
        else if(response.status == 409) {
            exibirMensagem('Email já cadastrado.', 'danger');
            return;
        }
        else if (response.status == 400) {
            exibirMensagem('Erro ao cadastrar usuário. Tente novamente.', 'danger');
            return;
        }else if (response.status == 404) {
            exibirMensagem('Falha na comunição com o servido', 'danger');
            return;
        }   
        else if (response.status == 500) {
            exibirMensagem('Erro interno do servidor. Tente novamente mais tarde.', 'danger');
            return;
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

    } catch (error) {
        console.error("Erro na requisição:", error.message);
        throw error; // repropaga para quem chamou
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
