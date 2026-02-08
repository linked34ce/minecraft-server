import { getStatus } from "./minecraftServerApi.js";

export const showError = (response) => {
    document.getElementById("content").style.display = "none";
    document.getElementById("error").style.display = "block";
    document.getElementById("status-code").innerText = response.statusCode;
    document.getElementById("error-message").innerText = response.message;
};

export const showStatus = async () => {
    const response = await getStatus();
    if (response.statusCode !== 200) {
        showError(response);
    } else {
        document.getElementById("status").innerHTML = response.isRunning
            ? "&#x1F7E2; Running"
            : "&#x1F534; Stopped";

        const buttonIdToDisplay = response.isRunning ? "stop" : "start";
        const buttonIdToHide = response.isRunning ? "start" : "stop";
        document.getElementById(buttonIdToDisplay).style.display = "block";
        document.getElementById(buttonIdToHide).style.display = "none";

        document.getElementById("ip-address").value =
            response.isRunning && response.ipAddress ? response.ipAddress : "-";

        document.getElementById("copy").addEventListener("click", () => {
            navigator.clipboard.writeText(response.ipAddress).then(() => {
                document.getElementById("copy").innerText = "Copied!!";
            });
        });
    }
};

export const closeModal = async () => {
    document.getElementById("dialog").close();
};
