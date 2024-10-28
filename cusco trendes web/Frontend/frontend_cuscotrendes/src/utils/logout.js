export const logout = () => {
    localStorage.removeItem('token'); // Eliminar el token de autenticación
    console.log("Sesión cerrada con éxito");
  };
  