"use strict";


/* ==========================================
   ENTIDADES
========================================== */

const ENTIDADES_PERU = {

    "Bancos": [
        "BCP",
        "BBVA",
        "Interbank",
        "Scotiabank",
        "Banco de la Nación",
        "Banco Pichincha",
        "BanBif",
        "Mibanco"
    ],

    "Cajas Municipales": [
        "Caja Arequipa",
        "Caja Huancayo",
        "Caja Piura",
        "Caja Cusco",
        "Caja Trujillo",
        "Caja Ica",
        "Caja Maynas"
    ],

    "Financieras": [
        "Financiera Crediscotia",
        "Financiera Confianza",
        "Financiera Compartamos",
        "Financiera Qapaq",
        "Financiera Proempresa",
        "Financiera Surgir"
    ]
};


/* ==========================================
   ELEMENTOS
========================================== */

const pantallaFormulario =
    document.getElementById("pantallaFormulario");

const pantallaVistaPrevia =
    document.getElementById("pantallaVistaPrevia");

const tipoEntidad =
    document.getElementById("tipoEntidad");

const entidad =
    document.getElementById("entidad");

const monto =
    document.getElementById("monto");

const comisionInfo =
    document.getElementById("comisionInfo");

const btnVistaPrevia =
    document.getElementById("btnVistaPrevia");

const btnModificar =
    document.getElementById("btnModificar");

const btnGuardar =
    document.getElementById("btnGuardar");

const btnCompartir =
    document.getElementById("btnCompartir");

const btnImprimir =
    document.getElementById("btnImprimir");

const ticketEntidad =
    document.getElementById("ticketEntidad");

const ticketMonto =
    document.getElementById("ticketMonto");

const ticketComision =
    document.getElementById("ticketComision");

const ticketTotal =
    document.getElementById("ticketTotal");

const fecha =
    document.getElementById("fecha");

const ticket =
    document.getElementById("ticket");


/* ==========================================
   VARIABLES
========================================== */

let datosActuales = {
    entidad: "",
    monto: 0,
    comision: 0
};


/* ==========================================
   INICIALIZAR ENTIDADES
========================================== */

function actualizarListaEntidades() {

    const tipo = tipoEntidad.value;

    const lista = ENTIDADES_PERU[tipo] || [];

    entidad.innerHTML = "";

    lista.forEach(function(nombre) {

        const opcion = document.createElement("option");

        opcion.value = nombre;
        opcion.textContent = nombre;

        entidad.appendChild(opcion);
    });
}


/* ==========================================
   CALCULAR COMISIÓN
========================================== */

function calcularComision(valor) {

    const numero = Number(valor);

    if (!numero || numero <= 0) {
        return 0;
    }

    return Math.ceil(numero / 100);
}


/* ==========================================
   ACTUALIZAR COMISIÓN
========================================== */

function actualizarComision() {

    const valor = parseFloat(monto.value);

    const comision = calcularComision(valor);

    comisionInfo.innerHTML =
        `Comisión: S/ ${comision.toFixed(2)}
        <br>
        <small>(Regla: S/ 1.00 por cada S/ 100.00)</small>`;
}


/* ==========================================
   MOSTRAR VISTA PREVIA
========================================== */

function mostrarVistaPrevia() {

    const valor = parseFloat(monto.value);

    if (!valor || valor <= 0) {

        alert("Ingrese un monto válido.");

        monto.focus();

        return;
    }

    const comision = calcularComision(valor);

    const nombreEntidad = entidad.value;

    const total = valor + comision;

    datosActuales = {
        entidad: nombreEntidad,
        monto: valor,
        comision: comision
    };


    /* Fecha */

    const ahora = new Date();

    const fechaTexto =
        ahora.toLocaleDateString("es-PE", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        })
        +
        " "
        +
        ahora.toLocaleTimeString("es-PE", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        });


    /* Actualizar ticket */

    fecha.textContent =
        "Fecha: " + fechaTexto;

    ticketEntidad.textContent =
        nombreEntidad;

    ticketMonto.textContent =
        `S/ ${valor.toFixed(2)}`;

    ticketComision.textContent =
        `S/ ${comision.toFixed(2)}`;

    ticketTotal.textContent =
        `S/ ${total.toFixed(2)}`;


    /* Cambiar pantalla */

    pantallaFormulario.classList.remove("activa");

    pantallaVistaPrevia.classList.add("activa");

    window.scrollTo(0, 0);
}


/* ==========================================
   VOLVER A MODIFICAR
========================================== */

function modificarDatos() {

    pantallaVistaPrevia.classList.remove("activa");

    pantallaFormulario.classList.add("activa");

    window.scrollTo(0, 0);
}


/* ==========================================
   CREAR IMAGEN DEL TICKET
========================================== */

async function generarImagen() {

    const ancho = 900;

    const alto = 650;

    const canvas =
        document.createElement("canvas");

    canvas.width = ancho;
    canvas.height = alto;

    const ctx =
        canvas.getContext("2d");


    /* Fondo */

    ctx.fillStyle = "#ffffff";

    ctx.fillRect(
        0,
        0,
        ancho,
        alto
    );


    /* Borde */

    ctx.strokeStyle = "#aaaaaa";

    ctx.lineWidth = 3;

    ctx.strokeRect(
        10,
        10,
        ancho - 20,
        alto - 20
    );


    /* Título */

    ctx.fillStyle = "#111111";

    ctx.textAlign = "center";

    ctx.font =
        "bold 34px Arial";

    ctx.fillText(
        "COMPROBANTE DE FACTURA",
        ancho / 2,
        65
    );


    /* Línea */

    ctx.setLineDash([10, 8]);

    ctx.beginPath();

    ctx.moveTo(50, 90);

    ctx.lineTo(ancho - 50, 90);

    ctx.stroke();

    ctx.setLineDash([]);


    /* Fecha */

    const ahora = new Date();

    const fechaTexto =
        ahora.toLocaleDateString("es-PE", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        })
        +
        " "
        +
        ahora.toLocaleTimeString("es-PE", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        });

    ctx.textAlign = "center";

    ctx.fillStyle = "#555555";

    ctx.font =
        "22px Arial";

    ctx.fillText(
        "Fecha: " + fechaTexto,
        ancho / 2,
        125
    );


    /* Datos */

    ctx.textAlign = "left";

    ctx.fillStyle = "#111111";

    ctx.font =
        "bold 25px Arial";

    ctx.fillText(
        "Entidad:",
        70,
        200
    );

    ctx.font =
        "25px Arial";

    ctx.fillText(
        datosActuales.entidad,
        350,
        200
    );


    ctx.font =
        "bold 25px Arial";

    ctx.fillText(
        "Monto Operación:",
        70,
        260
    );

    ctx.font =
        "25px Arial";

    ctx.fillText(
        `S/ ${datosActuales.monto.toFixed(2)}`,
        350,
        260
    );


    ctx.font =
        "bold 25px Arial";

    ctx.fillText(
        "Comisión:",
        70,
        320
    );

    ctx.font =
        "25px Arial";

    ctx.fillText(
        `S/ ${datosActuales.comision.toFixed(2)}`,
        350,
        320
    );


    /* Línea total */

    ctx.beginPath();

    ctx.moveTo(50, 365);

    ctx.lineTo(ancho - 50, 365);

    ctx.stroke();


    /* Total */

    const total =
        datosActuales.monto +
        datosActuales.comision;

    ctx.font =
        "bold 30px Arial";

    ctx.fillStyle = "#111111";

    ctx.fillText(
        "TOTAL A PAGAR:",
        70,
        425
    );

    ctx.textAlign = "right";

    ctx.fillText(
        `S/ ${total.toFixed(2)}`,
        ancho - 70,
        425
    );


    /* Pie */

    ctx.textAlign = "center";

    ctx.font =
        "20px Arial";

    ctx.fillStyle = "#666666";

    ctx.fillText(
        "¡Gracias por su preferencia!",
        ancho / 2,
        520
    );


    return new Promise(function(resolve) {

        canvas.toBlob(function(blob) {

            resolve(blob);

        }, "image/png");

    });
}


/* ==========================================
   GUARDAR
========================================== */

async function guardarComprobante() {

    const blob =
        await generarImagen();

    const ahora = new Date();

    const nombre =
        "factura_" +
        ahora.getFullYear() +
        String(ahora.getMonth() + 1).padStart(2, "0") +
        String(ahora.getDate()).padStart(2, "0") +
        "_" +
        String(ahora.getHours()).padStart(2, "0") +
        String(ahora.getMinutes()).padStart(2, "0") +
        String(ahora.getSeconds()).padStart(2, "0") +
        ".png";


    const url =
        URL.createObjectURL(blob);

    const enlace =
        document.createElement("a");

    enlace.href = url;

    enlace.download = nombre;

    document.body.appendChild(enlace);

    enlace.click();

    enlace.remove();

    URL.revokeObjectURL(url);
}


/* ==========================================
   COMPARTIR
========================================== */

async function compartirComprobante() {

    const blob =
        await generarImagen();

    const archivo =
        new File(
            [blob],
            "factura.png",
            {
                type: "image/png"
            }
        );


    /* Android moderno */

    if (
        navigator.share &&
        navigator.canShare &&
        navigator.canShare({
            files: [archivo]
        })
    ) {

        try {

            await navigator.share({
                title: "Factura",
                text: "Comprobante",
                files: [archivo]
            });

            return;

        } catch (error) {

            if (error.name === "AbortError") {
                return;
            }
        }
    }


    /* Si el navegador no permite compartir archivos */

    alert(
        "Tu navegador no permite compartir la imagen directamente. " +
        "Primero utiliza Guardar."
    );
}


/* ==========================================
   IMPRIMIR
========================================== */

function imprimirComprobante() {

    window.print();
}


/* ==========================================
   EVENTOS
========================================== */

tipoEntidad.addEventListener(
    "change",
    actualizarListaEntidades
);

monto.addEventListener(
    "input",
    actualizarComision
);

btnVistaPrevia.addEventListener(
    "click",
    mostrarVistaPrevia
);

btnModificar.addEventListener(
    "click",
    modificarDatos
);

btnGuardar.addEventListener(
    "click",
    guardarComprobante
);

btnCompartir.addEventListener(
    "click",
    compartirComprobante
);

btnImprimir.addEventListener(
    "click",
    imprimirComprobante
);


/* ==========================================
   INICIO
========================================== */

actualizarListaEntidades();

actualizarComision();