// src/components/Register.jsx
import React, { useState } from 'react';
import { crearUsuario } from '../services/api';
import 'bootstrap/dist/css/bootstrap.min.css';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [nombre, setNombre] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await crearUsuario({ nombre, email, password });
      setSuccess('Usuario creado exitosamente');
      setError(null);
      console.log('Usuario registrado:', response);
    } catch (error) {
      setError('Error al registrar usuario.');
      setSuccess(null);
    }
  };

  return (
    <div className="register-container d-flex align-items-center justify-content-center">
      <div className="card register-card shadow-lg">
        <div className="card-header text-center">
          <h3 className="register-title">Registro</h3>
        </div>
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label className="form-label">Nombre:</label>
              <input
                type="text"
                className="form-control register-input"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
              />
            </div>
            <div className="form-group mb-3">
              <label className="form-label">Email:</label>
              <input
                type="email"
                className="form-control register-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group mb-3">
              <label className="form-label">Password:</label>
              <input
                type="password"
                className="form-control register-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && <p className="text-danger text-center">{error}</p>}
            {success && <p className="text-success text-center">{success}</p>}
            <button type="submit" className="btn btn-primary w-100 mt-3">
              Registrar
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
