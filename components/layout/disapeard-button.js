function DisapeardButton(props) {
  return (
    <button
      className=" btn btn-success form-control mx-auto col-6  "
      onClick={props.showForm}
    >
      {props.description}
    </button>
  );
}
export default DisapeardButton;
