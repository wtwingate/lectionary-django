copyButton = document.getElementById("copy-button");

copyButton.addEventListener("click", () => {
  writeToClipboard(texts);
  alert("Lessons copied to clipboard!");
});

async function writeToClipboard(texts) {
  try {
    navigator.clipboard.writeText(texts);
  } catch (error) {
    console.error(error.message);
  }
}
