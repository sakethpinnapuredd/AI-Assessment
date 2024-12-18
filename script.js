document.addEventListener("DOMContentLoaded", () => {
    updateFields(); // Ensure fields are displayed for the initially selected shape
});

function updateFields() {
    const shape = document.getElementById("shape").value;
    const inputsDiv = document.getElementById("inputs");
    inputsDiv.innerHTML = ""; // Clear previous inputs

    if (shape === "Rectangle") {
        inputsDiv.innerHTML += '<label for="length">Length (units):</label><input type="number" id="length" name="length" step="0.01" required><br>';
        inputsDiv.innerHTML += '<label for="width">Width (units):</label><input type="number" id="width" name="width" step="0.01" required><br>';
    } else if (shape === "Triangle") {
        inputsDiv.innerHTML += '<label for="base">Base (units):</label><input type="number" id="base" name="base" step="0.01" required><br>';
        inputsDiv.innerHTML += '<label for="height">Height (units):</label><input type="number" id="height" name="height" step="0.01" required><br>';
    } else if (shape === "Circle") {
        inputsDiv.innerHTML += '<label for="radius">Radius (units):</label><input type="number" id="radius" name="radius" step="0.01" required><br>';
    }
}
