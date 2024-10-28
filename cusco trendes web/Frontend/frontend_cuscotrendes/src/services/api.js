import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';  // Cambia la URL si tu API corre en otro puerto

// Obtener el token almacenado en localStorage
const getToken = () => {
  return localStorage.getItem('token');
};

// Obtener todos los usuarios
export const obtenerUsuarios = async () => {
  try {
    const token = getToken();  // Obtener el token para la autorización
    const response = await axios.get(`${API_URL}/usuarios/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
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
    const token = getToken();  // Obtener el token para la autorización
    const response = await axios.put(`${API_URL}/usuarios/${id}`, usuario, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error al actualizar usuario:', error);
    throw error;
  }
};

// Eliminar usuario
export const eliminarUsuario = async (id) => {
  try {
    const token = getToken();  // Obtener el token para la autorización
    await axios.delete(`${API_URL}/usuarios/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
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

    const response = await axios.post(`${API_URL}/token`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    if (response.data.access_token) {
      // Guardar el token en localStorage
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  } catch (error) {
    console.error('Error al iniciar sesión:', error);
    throw error;
  }
};

// Función para ejecutar el análisis principal
export const ejecutarAnalisisDatos = async () => {
  try {
    const token = localStorage.getItem('token');  // Asegúrate de que tienes el token para autenticación
    const response = await axios.post(`${API_URL}/analisis-datos`, {}, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error ejecutando análisis de datos:', error);
    throw error;
  }
};

// Función para ejecutar EDA.py
export const ejecutarEDA = async () => {
  try {
    const token = localStorage.getItem('token');  // Asegúrate de que tienes el token para autenticación
    const response = await axios.post(`${API_URL}/analisis-eda`, {}, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error ejecutando EDA:', error);
    throw error;
  }
};

// Función para ejecutar machine_learning.py
export const ejecutarML = async () => {
  try {
    const token = localStorage.getItem('token');  // Asegúrate de que tienes el token para autenticación
    const response = await axios.post(`${API_URL}/analisis-ml`, {}, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error ejecutando machine learning:', error);
    throw error;
  }
};
 

// Ejecutar scraping de TripAdvisor con delay entre ejecuciones
export const ejecutarScrapingTripadvisor = async () => {
    try {
      const token = localStorage.getItem('token');  // Asegúrate de que el token esté en el localStorage
      const response = await axios.post(`${API_URL}/scraping-tripadvisor`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`  // Asegura que el token esté en los headers para la autenticación
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error ejecutando scraping de TripAdvisor:', error);
      throw error;
    }
  };
  

// Ejecutar scraping de Trustpilot con delay entre ejecuciones
export const ejecutarScrapingTrustpilot = async () => {
    try {
      const token = getToken();  // Asegúrate de que el token esté en el localStorage
      const response = await axios.post(`${API_URL}/scraping-trustpilot`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`  // Asegura que el token esté en los headers para la autenticación
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error ejecutando scraping de Trustpilot:', error);
      throw error;
    }
  };


// Cerrar sesión (eliminar token de localStorage)
export const logout = () => {
  localStorage.removeItem('token');
};



