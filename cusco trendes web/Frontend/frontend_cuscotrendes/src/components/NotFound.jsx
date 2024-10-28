// src/components/NotFound.jsx
import React from 'react';
import { FaExclamationTriangle } from 'react-icons/fa'; // Importa el icono para mejorar la apariencia

const NotFound = () => {
  return (
    <div className="notfound-container d-flex flex-column align-items-center justify-content-center">
      <FaExclamationTriangle className="notfound-icon mb-4" />
      <h2 className="notfound-title">404 - Página No Encontrada</h2>
      <p className="notfound-text">Lo sentimos, la página que buscas no existe o fue movida.</p>
    </div>
  );
};

export default NotFound;
