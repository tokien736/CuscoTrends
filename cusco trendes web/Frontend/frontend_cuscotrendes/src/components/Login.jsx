import React, { useState } from 'react';
import { login } from '../services/api';  // Asegúrate de que el servicio esté correctamente importado
import 'bootstrap/dist/css/bootstrap.min.css';  // Usar Bootstrap para estilizar el formulario

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);  // Limpiar el error antes de un nuevo intento de inicio de sesión
    try {
      const response = await login({ username: email, password });  // Ajusta el nombre de los campos según la API
      console.log('Login exitoso:', response);
      localStorage.setItem('token', response.access_token);  // Guardar el token en localStorage
      window.location.href = '/dashboard';  // Redirigir al dashboard o a otra página de la aplicación
    } catch (error) {
      setError('Error al iniciar sesión. Verifica tus credenciales.');  // Mensaje de error si la autenticación falla
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h3>Iniciar Sesión</h3>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="form-group mb-3">
                  <label>Email:</label>
                  <input
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Password:</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                {error && <p className="text-danger">{error}</p>}
                <button type="submit" className="btn btn-primary w-100">
                  Iniciar Sesión
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
