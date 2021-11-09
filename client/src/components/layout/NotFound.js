import { useHistory } from 'react-router-dom';
import { Container, Col, Row } from 'react-bootstrap';

function NotFound() {
    
  const history = useHistory();

  const handleHistory = () => {
    history.push('/home');
  };

  return (
    <>
      <Container>
        <Row>
          <Col xs={1}></Col>
          <Col className='error-page-container' xs={10}>
            <h3 className='error-page-text'>
              Error 404, Sorry the page your looking for cannot be found.
            </h3>
            <button onClick={() => handleHistory()} className='btn-1'>
              Go Home
            </button>
          </Col>
          <Col xs={1}></Col>
        </Row>
      </Container>
    </>
  );
}

export default NotFound;
