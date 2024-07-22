copyButton = document.getElementById("copy-button");

copyButton.addEventListener("click", (event) => {
    writeToClipboard(texts.join(""));
    alert("Lessons copied to clipboard!");
})

async function writeToClipboard(text) {
    try {
        navigator.clipboard.writeText(text);
    } catch(error) {
        console.error(error.message);
    }
}