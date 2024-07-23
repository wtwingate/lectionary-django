copyButton = document.getElementById("copy-button");

copyButton.addEventListener("click", () => {
    writeToClipboard(texts.join("").trim());
    alert("Lessons copied to clipboard!");
})

async function writeToClipboard(text) {
    try {
        navigator.clipboard.writeText(text);
    } catch(error) {
        console.error(error.message);
    }
}