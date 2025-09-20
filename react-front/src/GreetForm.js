import { useState } from "react";

export default function GreetForm() {
    const [name, setName] = useState("");
    const [msg, setMsg] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch("http://localhost:5000/api/greet", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name })
            });
            const data = await res.json();
            // el backend responde { greeting: "Hello, <name>!", saved: true, created: bool }
            setMsg(data.greeting || "Sin mensaje");  // <- CLAVE CORRECTA
            setName("");
        } catch (err) {
            console.error(err);
            setMsg("Error al conectar con el servidor");
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={name}
                    placeholder="Enter your name"
                    onChange={(e) => setName(e.target.value)}
                />
                <button type="submit">Enviar</button>
            </form>

            {msg && <p>{msg}</p>}
        </div>
    );
}
