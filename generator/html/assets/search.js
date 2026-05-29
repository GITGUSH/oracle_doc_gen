function filtrarTabela(input) {
    const filtro = input.value.toUpperCase();
    const tabela = document.getElementById("tabelaLista");
    const linhas = tabela.getElementsByTagName("tr");

    for (let i = 1; i < linhas.length; i++) {
        const celulas = linhas[i].getElementsByTagName("td");
        let encontrou = false;

        for (let j = 0; j < celulas.length; j++) {
            if (celulas[j].textContent.toUpperCase().includes(filtro)) {
                encontrou = true;
                break;
            }
        }

        linhas[i].style.display = encontrou ? "" : "none";
    }
}