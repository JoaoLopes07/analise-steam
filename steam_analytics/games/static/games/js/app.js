let currentPage = 1;

let totalPages = 1;


async function buscarJogos(page = 1) {

    currentPage = page;

    const gamesList =
        document.getElementById("gamesList");

    const loading =
        document.getElementById("loading");

    const errorMessage =
        document.getElementById("errorMessage");

    loading.style.display = "block";

    errorMessage.innerHTML = "";

    gamesList.innerHTML = "";

    try {

        const includeAnd =
            document.getElementById("includeAnd")
            .value
            .trim();

        const includeOr =
            document.getElementById("includeOr")
            .value
            .trim();

        const excludeAnd =
            document.getElementById("excludeAnd")
            .value
            .trim();

        const excludeOr =
            document.getElementById("excludeOr")
            .value
            .trim();

        const sort =
            document.getElementById("sortBy")
            .value;

        let filters = [];

        if (includeAnd) {
            filters.push(
                `INCLUDE_AND ${includeAnd}`
            );
        }

        if (includeOr) {
            filters.push(
                `INCLUDE_OR ${includeOr}`
            );
        }

        if (excludeAnd) {
            filters.push(
                `EXCLUDE_AND ${excludeAnd}`
            );
        }

        if (excludeOr) {
            filters.push(
                `EXCLUDE_OR ${excludeOr}`
            );
        }

        const filterTags =
            filters.join(";");

        const response = await fetch(
            `/api/games/?page=${page}&sort=${sort}&filter_tags=${encodeURIComponent(filterTags)}`
        );

        if (!response.ok) {

            throw new Error(
                "Erro ao buscar API"
            );
        }

        const data =
            await response.json();

        totalPages =
            data.total_pages;

        document.getElementById("pageInfo")
            .innerHTML =
            `Página ${data.page} de ${data.total_pages}`;

        if (data.results.length === 0) {

            errorMessage.innerHTML =
                "Nenhum jogo encontrado.";

            return;
        }

        data.results.forEach(game => {

            gamesList.innerHTML += `

                <div class="game">

                    <h2>${game.name}</h2>

                    <p>
                        💰 Preço:
                        $${game.price ?? 0}
                    </p>

                    <p>
                        ⭐ Reviews:
                        ${game.review_count ?? 0}
                    </p>

                    <p>
                        📈 Receita:
                        $${Math.floor(game.revenue_1year ?? 0)}
                    </p>

                    <p>
                        📅 Lançamento:
                        ${game.release_date ?? "-"}
                    </p>

                    <p>
                        🏷️ Tags:
                        ${game.tags.join(", ")}
                    </p>

                </div>
            `;
        });

    } catch (error) {

        console.error(error);

        errorMessage.innerHTML =
            "Erro ao carregar jogos.";

    } finally {

        loading.style.display = "none";
    }
}


function proximaPagina() {

    if (currentPage < totalPages) {

        buscarJogos(currentPage + 1);
    }
}


function paginaAnterior() {

    if (currentPage > 1) {

        buscarJogos(currentPage - 1);
    }
}


buscarJogos();