document.querySelector(".training-plans").addEventListener("click", (event) => {
    const btnVer = event.target.closest(".btn-ver");
    const btnEditar = event.target.closest(".btn-editar");

    if (btnVer) {
        verDetalhes(Number(btnVer.dataset.id));
    } else if (btnEditar) {
        editarFicha(Number(btnEditar.dataset.id));
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