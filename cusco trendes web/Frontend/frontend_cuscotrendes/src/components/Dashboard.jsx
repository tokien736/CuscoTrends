// src/components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Modal, Button, Spinner, Container, Row, Col } from 'react-bootstrap';
import { ejecutarAnalisisDatos, ejecutarEDA, ejecutarML, ejecutarScrapingTripadvisor, ejecutarScrapingTrustpilot } from '../services/api';
import { FaTripadvisor, FaSearch, FaRobot } from 'react-icons/fa';

const Dashboard = () => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [analisisResponse, setAnalisisResponse] = useState(null);
  const [imagenesEDA, setImagenesEDA] = useState([]);
  const [imagenesML, setImagenesML] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);

  const obtenerImagenes = async (tipo, setImagenes) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/listar-imagenes/${tipo}`);
      setImagenes(response.data.imagenes);
    } catch (error) {
      console.error(`Error al obtener imágenes de ${tipo}:`, error);
    }
  };

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

  const abrirImagen = (imagen) => {
    setSelectedImage(imagen);
  };

  const cerrarImagen = () => {
    setSelectedImage(null);
  };

  return (
    <Container className="dashboard-container mt-5 text-light">
      <h2 className="dashboard-title mb-4 text-center">Bienvenido al Dashboard</h2>

      <div className="text-center mb-5">
        <Button variant="primary" className="btn-action mx-2" onClick={handleScrapingTripadvisor} disabled={isExecuting}>
          <FaTripadvisor className="me-2" /> Scraping TripAdvisor
        </Button>
        <Button variant="secondary" className="btn-action mx-2" onClick={handleScrapingTrustpilot} disabled={isExecuting}>
          <FaSearch className="me-2" /> Scraping Trustpilot
        </Button>
        <Button variant="success" className="btn-action mx-2" onClick={handleAnalisisDatos} disabled={isExecuting}>
          <FaRobot className="me-2" /> Análisis de Datos
        </Button>
      </div>

      {isExecuting && (
        <div className="d-flex justify-content-center align-items-center mb-5">
          <Spinner animation="border" role="status" className="me-2 spinner-custom">
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

      <div className="mb-5">
        <h3 className="text-center section-title">Imágenes Generadas (EDA)</h3>
        <Row className="mt-4">
          {imagenesEDA.map((imagen) => (
            <Col md={4} key={imagen.nombre} className="mb-4 img-col" onClick={() => abrirImagen(imagen)}>
              <img src={imagen.url} alt={imagen.nombre} className="img-fluid rounded shadow img-card" />
              <p className="text-center img-title">{imagen.nombre}</p>
            </Col>
          ))}
        </Row>
      </div>

      <div className="mb-5">
        <h3 className="text-center section-title">Imágenes Generadas (Machine Learning)</h3>
        <Row className="mt-4">
          {imagenesML.map((imagen) => (
            <Col md={4} key={imagen.nombre} className="mb-4 img-col" onClick={() => abrirImagen(imagen)}>
              <img src={imagen.url} alt={imagen.nombre} className="img-fluid rounded shadow img-card" />
              <p className="text-center img-title">{imagen.nombre}</p>
            </Col>
          ))}
        </Row>
      </div>

      <Modal show={!!selectedImage} onHide={cerrarImagen}>
        <Modal.Header closeButton>
          <Modal.Title>{selectedImage?.nombre}</Modal.Title>
        </Modal.Header>
        <Modal.Body className="text-center">
          <img src={selectedImage?.url} alt={selectedImage?.nombre} className="img-fluid rounded" />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={cerrarImagen}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default Dashboard;
