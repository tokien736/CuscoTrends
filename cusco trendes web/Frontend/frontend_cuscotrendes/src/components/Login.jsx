// src/components/Login.jsx
import React, { useState } from 'react';
import { login } from '../services/api';
import 'bootstrap/dist/css/bootstrap.min.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await login({ username: email, password });
      console.log('Login exitoso:', response);
      localStorage.setItem('token', response.access_token);
      window.location.href = '/dashboard';
    } catch (error) {
      setError('Error al iniciar sesión. Verifica tus credenciales.');
    }
  };

  return (
    <div className="login-container d-flex align-items-center justify-content-center">
      <div className="card login-card shadow-lg">
        <div className="card-header text-center">
          <h3 className="login-title">Iniciar Sesión</h3>
        </div>
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label className="form-label">Email:</label>
              <input
                type="email"
                className="form-control login-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group mb-3">
              <label className="form-label">Password:</label>
              <input
                type="password"
                className="form-control login-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && <p className="text-danger text-center">{error}</p>}
            <button type="submit" className="btn btn-primary w-100 mt-3">
              Iniciar Sesión
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
