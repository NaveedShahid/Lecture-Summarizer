import { Modal, Button } from 'react-bootstrap';

function VerticalModal(props) {
  return (
    <Modal
      {...props}
      size='md'
      aria-labelledby='contained-modal-title-vcenter'
      centered
    >
      <Modal.Header closeButton></Modal.Header>
      <Modal.Body>
        <h5>Are you sure you want to delete this transcript?</h5>
      </Modal.Body>
      <Modal.Footer>
        <Button name = 'delete' className = 'delete-btn' onClick={props.onHide}>
          Delete
        </Button>
        <Button name = 'cancel' className = 'cancel-btn' onClick={props.onHide}>
          Cancel
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default VerticalModal;
