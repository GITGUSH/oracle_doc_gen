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

function ordenarTabela(col) {
    const tabela = document.getElementById("tabelaLista");
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);
    const headers = tabela.getElementsByTagName("th");

    const atual = headers[col].dataset.ordem || "";
    const novaOrdem = atual === "asc" ? "desc" : "asc";

    // limpa outros headers
    Array.from(headers).forEach((h, i) => {
        if (i !== col) {
            h.dataset.ordem = "";
            h.textContent = h.textContent.replace(" ▲", "").replace(" ▼", "");
        }
    });

    linhas.sort((a, b) => {
        const tdA = a.getElementsByTagName("td")[col].textContent.trim();
        const tdB = b.getElementsByTagName("td")[col].textContent.trim();

        const numA = parseFloat(tdA.replace(/\./g, "").replace(",", "."));
        const numB = parseFloat(tdB.replace(/\./g, "").replace(",", "."));

        const isNumerico = !isNaN(numA) && !isNaN(numB);

        if (isNumerico) {
            return novaOrdem === "asc" ? numA - numB : numB - numA;
        } else {
            const strA = tdA.toLowerCase();
            const strB = tdB.toLowerCase();
            if (strA < strB) return novaOrdem === "asc" ? -1 : 1;
            if (strA > strB) return novaOrdem === "asc" ? 1 : -1;
            return 0;
        }
    });

    const tbody = tabela.getElementsByTagName("tbody")[0];
    linhas.forEach(linha => tbody.appendChild(linha));

    // atualiza header clicado
    headers[col].textContent = headers[col].textContent.replace(" ▲", "").replace(" ▼", "");
    headers[col].dataset.ordem = novaOrdem;
    headers[col].textContent += novaOrdem === "asc" ? " ▲" : " ▼";
}

document.addEventListener("DOMContentLoaded", function () {
    const tabela = document.getElementById("tabelaLista");
    if (!tabela) return;

    const headers = tabela.getElementsByTagName("th");
    Array.from(headers).forEach((th, index) => {
        th.style.cursor = "pointer";
        th.title = "Clique para ordenar";
        th.addEventListener("click", () => ordenarTabela(index));
    });
});