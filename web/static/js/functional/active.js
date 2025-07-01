import { authApiClient } from '../core/auth.js';

let divisaoCounter = 0;
const divContainer = document.querySelector(".divisoes-container"); // container das divisoes

// Adiciona uma nova divisão dinamicamente
function adicionarDivisao(valor = '') {
    divisaoCounter++;
    const letra = String.fromCharCode(64 + divisaoCounter); // A, B, C, ...

    const div = document.createElement('div');
    div.className = 'input-group mb-2';
    div.innerHTML = `
        <span class="input-group-text">${letra}</span>
        <input type="text" class="form-control" placeholder="Ex: Peito, Tríceps" value="${valor}">
        <button class="btn btn-outline-danger btn-remover-divisao" type="button">
            <i class="bi bi-trash"></i>
        </button>
    `;
    divContainer.appendChild(div);
}

divContainer.addEventListener('click', function(event) {
    if (event.target.closest('.btn-remover-divisao')) {
        const button = event.target.closest('.btn-remover-divisao');
        if (divContainer.children.length > 1) {
            button.parentElement.remove();
            divisaoCounter--;

            // Reordenar letras
            const divs = divContainer.querySelectorAll('.input-group');
            divs.forEach((div, index) => {
                div.querySelector('.input-group-text').textContent = String.fromCharCode(65 + index); // A, B, C, ...
            });
        } else {
            alert('Pelo menos uma divisão é necessária!');
        }
    }
});

// Evento de clique no botão de salvar ficha
const btnSalvarFicha = document.getElementById("btnSalvarFicha");
btnSalvarFicha.addEventListener("click", async () => {
    const nome = document.getElementById("fichaNome").value;
    const objetivo = document.getElementById("fichaObjetivo").value;
    const ativa = document.getElementById("fichaAtiva").checked;
    const divs = divContainer.querySelectorAll("input[type='text']");
    const divisoes = Array.from(divs).map(div => div.value.trim()).filter(Boolean);

    if (!nome || !objetivo || divisoes.length === 0) {
        return alert("Preencha todos os campos.");
    }

    try {
        console.log("Nome:",nome,"objetivo:",objetivo,"ativa:",ativa)
        const planoRes = await authApiClient.post("/api/data/workout_plan/new", {
            workout_plan_name: nome,
            workout_plan_goal: objetivo,
            active: ativa
        });

        if (!planoRes.ok) {
            return alert("Erro ao criar plano de treino.");
        }

        const planoId = planoRes.body.workout_plan_id;

        for (let i = 0; i < divisoes.length; i++) {
            const split = divisoes[i];
            await authApiClient.post("/api/data/workout_split/new", {
                split,
                workout_plan_id: planoId,
                active: true
            });
        }

        alert("Ficha criada com sucesso!");
        bootstrap.Modal.getInstance(document.getElementById("novaFichaModal")).hide();
        carregarFichas();
    } catch (err) {
        console.error("Erro ao salvar ficha:", err);
        alert("Falha ao salvar ficha.");
    }
});

// Carrega fichas do usuário e renderiza os cards
async function carregarFichas() {
    try {
        const container = document.querySelector(".row.g-4");
        //container.innerHTML = "";  Limpa antes de renderizar

        const fichasRes = await authApiClient.get("/api/data/workout_plan");
        const splitsRes = await authApiClient.get("/api/data/workout_split");

        const fichas = fichasRes.body;
        const splits = splitsRes.body;
        if (splits && fichas) {
            fichas.forEach(ficha => {
                const fichaSplits = splits.filter(s => s.workout_plan_id === ficha.workout_plan_id);

                const splitBadges = fichaSplits.map((s, i) => {
                    const letra = String.fromCharCode(65 + i);
                    return `<span class="badge badge-primary">${letra} - ${s.split}</span>`;
                }).join(" ");

                const status = ficha.active ? 'Ativa' : 'Inativa';
                const statusClass = ficha.active ? 'success' : 'secondary';
                const dataCriacao = new Date(ficha.created_at).toLocaleDateString();

                const card = document.createElement('div');
                card.className = 'col-lg-4 col-md-6';
                card.innerHTML = `
                    <div class="card h-100" data-id="${ficha.workout_plan_id}">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">${ficha.workout_plan_name}</h5>
                            <span class="badge bg-${statusClass}">${status}</span>
                        </div>
                        <div class="card-body">
                            <p class="card-text">
                                <strong>Objetivo:</strong> ${ficha.workout_plan_goal}<br>
                                <strong>Divisões:</strong> ${fichaSplits.length > 0 ? fichaSplits.map(s => s.split).join(", ") : "Nenhuma"}<br>
                                <strong>Criada em:</strong> ${dataCriacao}
                            </p>
                            <div class="mb-3 d-flex flex-wrap gap-1">
                                ${splitBadges}
                            </div>
                        </div>
                        <div class="card-footer bg-transparent">
                            <div class="btn-group w-100" role="group">
                                <button class="btn btn-primary btn-sm btn-ver" data-id="${ficha.workout_plan_id}">
                                    <i class="bi bi-eye me-1"></i><span class="d-none d-sm-inline">Ver</span>
                                </button>
                                <button class="btn btn-warning btn-sm btn-editar" data-id="${ficha.workout_plan_id}">
                                    <i class="bi bi-pencil me-1"></i><span class="d-none d-sm-inline">Editar</span>
                                </button>
                                <button class="btn btn-${ficha.active ? 'secondary' : 'success'} btn-sm btn-ativar" data-id="${ficha.workout_plan_id}">
                                    <i class="bi bi-${ficha.active ? 'pause' : 'play-fill'} me-1"></i><span class="d-none d-sm-inline">${ficha.active ? 'Desativar' : 'Ativar'}</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }
    } catch (err) {
        console.error("Erro ao carregar fichas:", err);
    }
}
document.querySelector(".row.g-4").addEventListener("click", (event) => {
    const btnVer = event.target.closest(".btn-ver");
    const btnEditar = event.target.closest(".btn-editar");
    const btnAtivar = event.target.closest(".btn-ativar");

    if (btnVer) {
        verDetalhes(Number(btnVer.dataset.id));
    } else if (btnEditar) {
        editarFicha(Number(btnEditar.dataset.id));
    } else if (btnAtivar) {
    //ativar no banco 
    }
});

function verDetalhes(fichaId) {

    const modal = new bootstrap.Modal(document.getElementById('detalhesModal'));
    modal.show();
}

function editarFicha(fichaId) {
    
    const modal = new bootstrap.Modal(document.getElementById('editarFichaModal'));
    modal.show();
}

function ativarFicha(fichaId) {

    const modal = new bootstrap.Modal(document.getElementById('detalhesModal'));
    modal.show();
}

// Evento inicial
document.getElementById("btnAdicionarDivisao").addEventListener("click", () => adicionarDivisao());
adicionarDivisao();
carregarFichas();
