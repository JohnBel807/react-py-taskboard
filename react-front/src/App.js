import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import GreetForm from './GreetForm';

function App() {
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/data")
      .then((res) => res.json())
      .then((data) => {
        setMsg(data.message);
        setLoading(false);
  })
      .catch((err) => console.error(err));
}, []);
return (
    <div className="App">
      <header className="App-header">
        {loading ? "Loading..." : msg}
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <div>
          <h2>Dockerized React App</h2>
          <p>This React application is running inside a Docker container.</p>
        </div>
        <GreetForm />
      </header>
    </div>
    
  );
}

export default App;
