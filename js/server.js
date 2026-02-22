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
        const serverStatus = response.serverStatus;
        const statusArea = document.getElementById("status");
        const ipAddressInput = document.getElementById("ip-address");
        const copyButton = document.getElementById("copy");

        let buttonIdToDisplay;

        if (serverStatus.isRunning && serverStatus.ipAddress) {
            statusArea.innerHTML = "&#x1F7E2; Running";
            buttonIdToDisplay = "stop";
            ipAddressInput.value = serverStatus.ipAddress;
            copyButton.disabled = false;
        } else {
            statusArea.innerHTML = "&#x1F534; Stopped";
            buttonIdToDisplay = "start";
            ipAddressInput.value = "-";
            copyButton.disabled = true;
        }

        const buttonIdToHide = buttonIdToDisplay == "stop" ? "start" : "stop";
        document.getElementById(buttonIdToDisplay).style.display = "block";
        document.getElementById(buttonIdToHide).style.display = "none";

        document.getElementById("copy").addEventListener("click", () => {
            navigator.clipboard.writeText(serverStatus.ipAddress).then(() => {
                document.getElementById("copy").innerText = "Copied!!";
            });
        });
    }
};

export const closeModal = async () => {
    document.getElementById("dialog").close();
};
