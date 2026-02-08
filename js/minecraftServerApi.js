import { MINECRAFT_SERVER_API_ENDPOINT } from "./const.js";

const showError = () => {
    document.getElementById("content").style.display = "none";
    document.getElementById("error").style.display = "block";
    document.getElementById("status-code").innerText = 403;
    document.getElementById("error-message").innerText =
        "You are not allowed to stop/start the Minecraft server.";
};

export const getStatus = async () => {
    const minecraftServerStatusRequest = new Request(
        `${MINECRAFT_SERVER_API_ENDPOINT}/status`,
    );

    let response = null;

    try {
        response = await fetch(minecraftServerStatusRequest);
    } catch (e) {
        showError();
        throw e;
    }

    return response.json();
};

export const startServer = async () => {
    const minecraftServerStartRequest = new Request(
        `${MINECRAFT_SERVER_API_ENDPOINT}/start`,
        {
            method: "POST",
        },
    );

    let response = null;

    try {
        response = await fetch(minecraftServerStartRequest);
    } catch (e) {
        showError();
        throw e;
    }

    return response.json();
};

export const stopServer = async () => {
    const minecraftServerStopRequest = new Request(
        `${MINECRAFT_SERVER_API_ENDPOINT}/stop`,
        {
            method: "POST",
        },
    );

    let response = null;

    try {
        response = await fetch(minecraftServerStopRequest);
    } catch (e) {
        showError();
        throw e;
    }

    return response.json();
};
