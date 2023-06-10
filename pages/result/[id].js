import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";
import Link from "next/link";
const Result = (props) => {
  const router = useRouter();

  const { id, title, description } = router.query;
  return (
    <div className="col-12 text-center">
      <h1>Covid Data-Set</h1>
      <div className="col-4 text-center p-4 mx-auto">
        <p className="col-3 p-4 form form-control mx-auto mt-3 " type="text">
          {title}
        </p>
      </div>
      <button className="btn btn-success p-2 col-3">
        <Link className="text-light" href="/search">
          Back
        </Link>
      </button>
      <div className="col-12 mx-auto">
        <ul className="p-4">
          <p className=" col-12 p-5 form from-control mt-2 list-group-item list-group-item-info text-primary rounded">
            {description}
          </p>
        </ul>
      </div>
    </div>
  );
};

export default Result;
