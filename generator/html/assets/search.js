function filtrarTabela(input) {
    const filtro = input.value.toUpperCase();
    const tabela = document.getElementById("tabelaLista");
    const linhas = tabela.getElementsByTagName("tr");

    let visiveis = 0;
    let total = linhas.length - 1;

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
        if (encontrou) visiveis++;
    }

    // atualiza contador
    let contador = document.getElementById("contadorResultados");
    if (!contador) {
        contador = document.createElement("div");
        contador.id = "contadorResultados";
        contador.style.cssText = "font-size: 12px; color: #888; margin-bottom: 10px; margin-top: -10px;";
        tabela.parentNode.insertBefore(contador, tabela);
    }

    if (filtro === "") {
        contador.textContent = "";
    } else {
        contador.textContent = `${visiveis} de ${total} resultado${total !== 1 ? 's' : ''}`;
    }
}