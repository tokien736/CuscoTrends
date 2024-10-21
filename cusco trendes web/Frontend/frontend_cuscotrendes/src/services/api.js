import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';  // Cambia la URL si tu API corre en otro puerto

// Obtener todos los usuarios
export const obtenerUsuarios = async () => {
  try {
    const response = await axios.get(`${API_URL}/usuarios/`);
    return response.data;
  } catch (error) {
    console.error('Error al obtener usuarios:', error);
    throw error;
  }
};

// Crear nuevo usuario
export const crearUsuario = async (usuario) => {
  try {
    const response = await axios.post(`${API_URL}/register/`, usuario);
    return response.data;
  } catch (error) {
    console.error('Error al crear usuario:', error);
    throw error;
  }
};

// Actualizar usuario
export const actualizarUsuario = async (id, usuario) => {
  try {
    const response = await axios.put(`${API_URL}/usuarios/${id}`, usuario);
    return response.data;
  } catch (error) {
    console.error('Error al actualizar usuario:', error);
    throw error;
  }
};

// Eliminar usuario
export const eliminarUsuario = async (id) => {
  try {
    await axios.delete(`${API_URL}/usuarios/${id}`);
  } catch (error) {
    console.error('Error al eliminar usuario:', error);
    throw error;
  }
};

// Función para el login
export const login = async (credenciales) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', credenciales.username);
    formData.append('password', credenciales.password);

    const response = await axios.post(`${API_URL}/token`, formData);
    return response.data;
  } catch (error) {
    console.error('Error al iniciar sesión:', error);
    throw error;
  }
};
