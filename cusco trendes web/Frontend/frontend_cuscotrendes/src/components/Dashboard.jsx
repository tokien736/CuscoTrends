import React, { useState } from 'react';
import { Modal, Button, Spinner } from 'react-bootstrap';
import { ejecutarAnalisisDatos, ejecutarEDA, ejecutarML, ejecutarScrapingTripadvisor, ejecutarScrapingTrustpilot } from '../services/api';  // Asegúrate de que los servicios están importados

const Dashboard = () => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [analisisResponse, setAnalisisResponse] = useState(null);

  // Maneja la ejecución del scraping de TripAdvisor
  const handleScrapingTripadvisor = async () => {
    setIsExecuting(true);  // Muestra el spinner y el texto de carga
    try {
      const response = await ejecutarScrapingTripadvisor();
      console.log('Scraping de TripAdvisor completado:', response);
      alert('Scraping de TripAdvisor completado con éxito.');
    } catch (error) {
      console.error('Error ejecutando scraping de TripAdvisor:', error);
      alert('Error durante el scraping de TripAdvisor.');
    } finally {
      setIsExecuting(false);  // Oculta el spinner
    }
  };

  // Maneja la ejecución del scraping de Trustpilot
  const handleScrapingTrustpilot = async () => {
    setIsExecuting(true);  // Muestra el spinner y el texto de carga
    try {
      const response = await ejecutarScrapingTrustpilot();
      console.log('Scraping de Trustpilot completado:', response);
      alert('Scraping de Trustpilot completado con éxito.');
    } catch (error) {
      console.error('Error ejecutando scraping de Trustpilot:', error);
      alert('Error durante el scraping de Trustpilot.');
    } finally {
      setIsExecuting(false);  // Oculta el spinner
    }
  };

  // Maneja la ejecución del análisis de datos principal
  const handleAnalisisDatos = async () => {
    setIsExecuting(true);
    try {
      const response = await ejecutarAnalisisDatos();
      console.log('Análisis de datos completado:', response);
      setAnalisisResponse(response);
      setShowModal(true);  // Mostrar modal después de ejecutar el análisis
    } catch (error) {
      console.error('Error ejecutando análisis de datos:', error);
      alert('Error durante el análisis de datos.');
    } finally {
      setIsExecuting(false);  // Ocultar la carga
    }
  };

  // Maneja las opciones del modal para ejecutar los otros scripts
  const handleOpciones = async (ruta) => {
    setShowModal(false);
    setIsExecuting(true);  // Mostrar el spinner para los análisis adicionales
    try {
      if (ruta === 'eda') {
        const response = await ejecutarEDA();
        console.log('Análisis EDA completado:', response);
        alert('Análisis EDA completado con éxito.');
      } else if (ruta === 'ml') {
        const response = await ejecutarML();
        console.log('Análisis de machine learning completado:', response);
        alert('Análisis de machine learning completado con éxito.');
      }
    } catch (error) {
      console.error('Error ejecutando análisis:', error);
      alert('Error durante el análisis.');
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Bienvenido al Dashboard</h2>
      <p>Has iniciado sesión con éxito.</p>
      <div className="mt-4">
        <button className="btn btn-primary me-2" onClick={handleScrapingTripadvisor} disabled={isExecuting}>
          <i className="fas fa-search"></i> {isExecuting ? 'Scraping TripAdvisor...' : 'Scraping TripAdvisor'}
        </button>
        <button className="btn btn-secondary me-2" onClick={handleScrapingTrustpilot} disabled={isExecuting}>
          <i className="fas fa-search"></i> {isExecuting ? 'Scraping Trustpilot...' : 'Scraping Trustpilot'}
        </button>
        <button className="btn btn-success" onClick={handleAnalisisDatos} disabled={isExecuting}>
          <i className="fas fa-chart-line"></i> {isExecuting ? 'Ejecutando Análisis...' : 'Análisis de Datos'}
        </button>
      </div>

      {/* Mostrar spinner y texto de carga durante la ejecución */}
      {isExecuting && (
        <div className="mt-4">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Cargando...</span>
          </Spinner>
          <p>Procesando...</p>
        </div>
      )}

      {/* Modal para mostrar las opciones después del análisis */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Opciones de Análisis</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Elige qué análisis deseas ejecutar:</p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => handleOpciones('eda')} disabled={isExecuting}>
            Ejecutar EDA.py
          </Button>
          <Button variant="primary" onClick={() => handleOpciones('ml')} disabled={isExecuting}>
            Ejecutar machine_learning.py
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Dashboard;
