
const API = "https://gestion-desarrollo-actividad7-api.onrender.com";

// Mensaje de bienvenida
async function cargarBienvenida() {
    const saludo = document.getElementById("saludo");

    try {
        const respuesta = await fetch(`${API}/usuarios/1`);

        if (!respuesta.ok) {
            throw new Error("HTTP " + respuesta.status);
        }

        const usuario = await respuesta.json();

        saludo.textContent = `¡Bienvenido/a, ${usuario.nombre}!`;

    } catch (error) {
        saludo.textContent = "No se pudo conectar con el backend";
        console.error("Error al cargar bienvenida:", error);
    }
}

// Lista de integrantes del equipo
async function cargarUsuarios() {
    const lista = document.getElementById("lista");
    lista.innerHTML = "";

    try {
        const respuesta = await fetch(`${API}/usuarios`);

        if (!respuesta.ok) {
            throw new Error("HTTP " + respuesta.status);
        }

        const usuarios = await respuesta.json();

        usuarios.forEach(usuario => {
            const item = document.createElement("li");

            item.textContent =
                `${usuario.id} · ${usuario.nombre} (${usuario.email})`;

            lista.appendChild(item);
        });

    } catch (error) {
        lista.textContent = "Error al cargar los usuarios";
        console.error("Error al cargar usuarios:", error);
    }
}

// Recargar información
function recargar() {
    cargarBienvenida();
    cargarUsuarios();
}

recargar();
