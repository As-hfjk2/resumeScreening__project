document.addEventListener("DOMContentLoaded", function () {

    let score = parseFloat(document.getElementById("score-data").dataset.score);

    if (isNaN(score)) {
        score = 0;
    }

    if (score <= 1) {
        score = score * 100;
    }

    score = Math.round(score);

    const bar = document.getElementById("bar");

    if (bar) {
        bar.style.width = score + "%";
    }

});