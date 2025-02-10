"use client";
import { useRef, useEffect } from "react";
function _modal({data}) {
  const modalRef = useRef(null);
  return (
    <>
      <button className="btn" onClick={() => modalRef.current?.showModal()}>
        open modal
      </button>
      <dialog id="my_modal_4" className="modal" ref={modalRef}>
        <div className="modal-box w-11/12 max-w-5xl">
          <h3 className="font-bold text-lg">Hello!</h3>
          <p className="py-4">Click the button below to close</p>
          <div className="modal-action">
            <form method="dialog">
              {/* if there is a button, it will close the modal */}
              <button className="btn">Close</button>
            </form>
          </div>
        </div>
      </dialog>
    </>
  );
}

export default _modal;
