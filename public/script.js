const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

function typing(bool) {
  if (bool) {
    $("#typing").classList.remove("hidden");
  } else $("#typing").classList.add("hidden");
}

function message(role, text) {
    document.querySelector("#chat").innerHTML +=
    `<div class="message ${role}">${text}</div>`;
    $("#filesystem").innerHTML = "";
    filesystem($("#filesystem"), JSON.parse(get('/files')))
}

function system(type, text) {
    $('main input[type="text"').value = "";
    $("#chat").innerHTML += `<div class="system ${type}">${text}</div>`;
    $("#filesystem").innerHTML = "";
    filesystem($("#filesystem"), JSON.parse(get('/files')))
}

async function send(input) {
    message("user", input);
    typing(true);

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: input })
        });

        typing(false);

        if (!response.ok) {
            system("error", `Error: ${response.statusText}`);
            return;
        }

        const output = await response.json();

        if (output.error) {
            system("error", output.error);
        } else if (output.response) {
            output.response.forEach((msg) => {
                if(msg.startsWith("$")) {
                    system("info", `Let me run <code>${msg.substring(1).trim()}</code>`);
                } else if(msg.startsWith("!")) {
                    system("warning", msg.substring(1).trim());
                } else if(msg == "None") {
                    system("error", "Please try again.");
                } else {
                    message("ai", msg);
                }
            });
        } else {
            system("error", "Error: No response from server.");
        }

    } catch (err) {
        typing(false);
        system("error", `Network error: ${err.message}`);
    }
}

function onload() {
    $("#input").addEventListener("change", (e) => {
        const input = e.target.value.trim();
        if (input && input.length > 1) {
            send(input);
            e.target.value = "";
        }
    })

    post("/reset")

    $("#filesystem").innerHTML = "";
    filesystem($("#filesystem"), JSON.parse(get('/files')))
}

function filesystem(current, list) {

    for(let el of list) {
        if(el.children) {
            let folder = document.createElement("div");
            folder.classList.add("folder");
            folder.innerHTML = `<div class="folder-name">${el.name}</div>`;
            current.appendChild(folder);

            filesystem(folder, el.children);
        } else {
            let file = document.createElement("div");
            file.classList.add("file");
            file.innerHTML = el.name;
            current.appendChild(file);
        }
    }
}