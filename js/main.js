import { showWeather } from "./weather.js";
import { startServer, stopServer } from "./minecraftServerApi.js";
import { showError, showStatus, closeModal } from "./server.js";

window.addEventListener("DOMContentLoaded", async () => {
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
        document.getElementById("loading").style.display = "block";

        const response = await startServer();

        if (response.statusCode !== 200) {
            showError(response);
        } else {
            setTimeout(async () => {
                await showStatus();
                document.getElementById("loading").style.display = "none";
            }, 5000);
            document.getElementById("success-message").innerText =
                response.message;
            dialog.showModal();
        }
    });

    document.getElementById("stop").addEventListener("click", async () => {
        const isConfirmed = window.confirm(
            "Are you sure to stop the Minecraft server?",
        );
        if (isConfirmed) {
            // window.open(
            //     "https://o2errkg3cnzogurvtxqn3addre0nwxsy.lambda-url.us-east-1.on.aws/",
            // );
            // setTimeout(() => {
            //     location.reload();
            // }, 5000);
            document.getElementById("stop").style.display = "none";
            document.getElementById("loading").style.display = "block";

            const response = await stopServer();

            if (response.statusCode !== 200) {
                showError(response);
            } else {
                setTimeout(async () => {
                    await showStatus();
                    document.getElementById("loading").style.display = "none";
                }, 5000);
                document.getElementById("success-message").innerText =
                    response.message;
                dialog.showModal();
            }
        }
    });

    await showWeather();
});
