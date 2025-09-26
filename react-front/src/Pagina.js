import "./style.css"
export default function Pagina (){
    return (
        <body>
  <header>
    <div class="banner">
      <h1>Transporte JonCar</h1>
      <p>Turismo por la región de Santander</p>
    </div>
    <nav>
      <ul>
        <li><a href="#inicio">Inicio</a></li>
        <li><a href="#contacto">Contacto</a></li>
        <li><a href="#precios">Precios</a></li>
      </ul>
    </nav>
  </header>

  <section id="inicio">
    <h2>Explora Santander con nosotros</h2>
    <img src="/breakTime.png" />
    <p>Ofrecemos recorridos por los mejores destinos turísticos de Santander con vehículos cómodos y seguros.</p>
  </section>

  <section id="contacto">
    <h2>Contáctanos</h2>
    <form id="formulario">

      <label for="nombre">Nombre:</label>
      <input type="text" id="nombre" name="nombre" required />
      
      <label for="correo">Correo:</label>
      <input type="email" id="correo" name="correo" required />
      
      <label for="telefono">Teléfono:</label>
      <input type="tel" id="telefono" name="telefono" required />
      
      <label for="mensaje">Mensaje:</label>
      <textarea id="mensaje" name="mensaje" rows="4" required></textarea>
      
      <button type="submit">Enviar</button>
    </form>
  </section>

  <section id="precios">
    <h2>Tarifas de Viaje</h2>
    <table>
      <head>
        <tr>
          <th>Destino</th>
          <th>Duración</th>
          <th>Precio</th>
        </tr>
      </head>
      <body>
        <tr>
          <td>Barichara</td>
          <td>1 día</td>
          <td>$600000</td>
        </tr>
        <tr>
          <td>San Gil</td>
          <td>2 días</td>
          <td>$250.000</td>
        </tr>
        <tr>
          <td>Chicamocha</td>
          <td>1 día</td>
          <td>$150.000</td>
        </tr>
        <script src="{{ url_for('static', filename='js/script.js') }}"></script>
      </body>
    </table>
  </section>

  <footer>
    <p><strong>Transporte JonCar</strong></p>
    <p>📞 3174847770 / 3165547544</p>
    <p>📧 mikeastaiza@gmail.com</p>
    <div class="social-icons">
      <img src="https://cdn-icons-png.flaticon.com/24/733/733585.png" alt="WhatsApp" />
      <img src="https://cdn-icons-png.flaticon.com/24/733/733547.png" alt="Facebook" />
      <img src="https://cdn-icons-png.flaticon.com/24/733/733558.png" alt="Instagram" />
    </div>
  </footer>
</body>
    )
}