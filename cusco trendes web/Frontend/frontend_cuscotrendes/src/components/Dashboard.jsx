import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Modal, Button, Spinner } from 'react-bootstrap';
import { ejecutarAnalisisDatos, ejecutarEDA, ejecutarML, ejecutarScrapingTripadvisor, ejecutarScrapingTrustpilot } from '../services/api';

const Dashboard = () => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [analisisResponse, setAnalisisResponse] = useState(null);
  const [imagenesEDA, setImagenesEDA] = useState([]);
  const [imagenesML, setImagenesML] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null); // Estado para la imagen seleccionada

  // Función para obtener las imágenes desde el backend
  const obtenerImagenes = async (tipo, setImagenes) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/listar-imagenes/${tipo}`);
      setImagenes(response.data.imagenes);
    } catch (error) {
      console.error(`Error al obtener imágenes de ${tipo}:`, error);
    }
  };

  // Cargar las imágenes al montar el componente
  useEffect(() => {
    obtenerImagenes('eda', setImagenesEDA);
    obtenerImagenes('machine_learning', setImagenesML);
  }, []);

  const handleScrapingTripadvisor = async () => {
    setIsExecuting(true);
    try {
      await ejecutarScrapingTripadvisor();
      alert('Scraping de TripAdvisor completado con éxito.');
    } catch (error) {
      alert('Error durante el scraping de TripAdvisor.');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleScrapingTrustpilot = async () => {
    setIsExecuting(true);
    try {
      await ejecutarScrapingTrustpilot();
      alert('Scraping de Trustpilot completado con éxito.');
    } catch (error) {
      alert('Error durante el scraping de Trustpilot.');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleAnalisisDatos = async () => {
    setIsExecuting(true);
    try {
      await ejecutarAnalisisDatos();
      setShowModal(true);
    } catch (error) {
      alert('Error durante el análisis de datos.');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleOpciones = async (ruta) => {
    setShowModal(false);
    setIsExecuting(true);
    try {
      if (ruta === 'eda') {
        await ejecutarEDA();
        obtenerImagenes('eda', setImagenesEDA);
      } else if (ruta === 'ml') {
        await ejecutarML();
        obtenerImagenes('machine_learning', setImagenesML);
      }
    } catch (error) {
      alert('Error durante el análisis.');
    } finally {
      setIsExecuting(false);
    }
  };

  // Función para abrir el modal de imagen
  const abrirImagen = (imagen) => {
    setSelectedImage(imagen);
  };

  // Función para cerrar el modal de imagen
  const cerrarImagen = () => {
    setSelectedImage(null);
  };

  return (
    <div className="container mt-5">
      <h2>Bienvenido al Dashboard</h2>
      <div className="mt-4">
        <button className="btn btn-primary me-2" onClick={handleScrapingTripadvisor} disabled={isExecuting}>
          Scraping TripAdvisor
        </button>
        <button className="btn btn-secondary me-2" onClick={handleScrapingTrustpilot} disabled={isExecuting}>
          Scraping Trustpilot
        </button>
        <button className="btn btn-success" onClick={handleAnalisisDatos} disabled={isExecuting}>
          Análisis de Datos
        </button>
      </div>

      {isExecuting && (
        <div className="mt-4">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Cargando...</span>
          </Spinner>
          <p>Procesando...</p>
        </div>
      )}

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

      <div className="mt-5">
        <h3>Imágenes Generadas (EDA)</h3>
        <div className="row">
          {imagenesEDA.map((imagen) => (
            <div className="col-md-4" key={imagen.nombre} onClick={() => abrirImagen(imagen)}>
              <img src={imagen.url} alt={imagen.nombre} className="img-fluid" style={{ cursor: 'pointer' }} />
              <p>{imagen.nombre}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-5">
        <h3>Imágenes Generadas (Machine Learning)</h3>
        <div className="row">
          {imagenesML.map((imagen) => (
            <div className="col-md-4" key={imagen.nombre} onClick={() => abrirImagen(imagen)}>
              <img src={imagen.url} alt={imagen.nombre} className="img-fluid" style={{ cursor: 'pointer' }} />
              <p>{imagen.nombre}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Modal para mostrar la imagen seleccionada en tamaño grande */}
      <Modal show={!!selectedImage} onHide={cerrarImagen}>
        <Modal.Header closeButton>
          <Modal.Title>{selectedImage?.nombre}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <img src={selectedImage?.url} alt={selectedImage?.nombre} className="img-fluid" />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={cerrarImagen}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Dashboard;
