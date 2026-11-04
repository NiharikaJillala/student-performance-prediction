// Small frontend validation before the form is sent to Flask.
const form = document.getElementById("predictionForm");

if (form) {
    form.addEventListener("submit", function (event) {
        const fields = form.querySelectorAll("input");
        const message = document.getElementById("formMessage");

        for (const field of fields) {
            const value = Number(field.value);

            if (field.value.trim() === "" || !Number.isFinite(value)) {
                event.preventDefault();
                message.textContent = "Please enter a valid number in every field.";
                return;
            }

            if (value < Number(field.min) || value > Number(field.max)) {
                event.preventDefault();
                message.textContent = `Please enter a value between ${field.min} and ${field.max}.`;
                field.focus();
                return;
            }
        }

        message.textContent = "";
    });
}
