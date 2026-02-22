import { showWeather } from "./weather.js";
import { startServer, stopServer } from "./minecraftServerApi.js";
import { showError, showStatus, closeModal } from "./server.js";

window.addEventListener("DOMContentLoaded", async () => {
    const loading = document.getElementById("loading");
    const successMessage = document.getElementById("success-message");

    loading.style.display = "block";
    await showStatus();

    const dialog = document.getElementById("dialog");

    dialog.addEventListener("click", async () => await closeModal());

    document
        .getElementById("close")
        .addEventListener("click", async () => await closeModal());

    document
        .getElementById("dialog-content")
        .addEventListener("click", (e) => e.stopPropagation());

    document.getElementById("start").addEventListener("click", async () => {
        document.getElementById("start").style.display = "none";
        loading.style.display = "block";

        const response = await startServer();

        if (response.statusCode !== 200) {
            showError(response);
        } else {
            setTimeout(async () => {
                await showStatus();
            }, 5000);
            successMessage.innerText = response.message;
            dialog.showModal();
        }
    });

    document.getElementById("stop").addEventListener("click", async () => {
        const isConfirmed = window.confirm(
            "Are you sure to stop the Minecraft server?",
        );
        if (isConfirmed) {
            document.getElementById("stop").style.display = "none";
            loading.style.display = "block";

            const response = await stopServer();

            if (response.statusCode !== 200) {
                showError(response);
            } else {
                setTimeout(async () => {
                    await showStatus();
                }, 5000);
                successMessage.innerText = response.message;
                dialog.showModal();
            }
        }
    });

    await showWeather();
});
