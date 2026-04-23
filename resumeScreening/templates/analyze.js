// Drag & Drop
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");

dropArea.addEventListener("click", () => fileInput.click());

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.background = "#dbeafe";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.background = "";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
});

// Loader
document.getElementById("form").addEventListener("submit", () => {
    document.getElementById("loader").style.display = "flex";
});

// Circular Progress
window.onload = () => {
    const score = parseInt(document.querySelector(".number")?.innerText) || 0;
    const circle = document.getElementById("progress");

    if (circle) {
        const offset = 377 - (377 * score) / 100;
        circle.style.strokeDashoffset = offset;
    }
};