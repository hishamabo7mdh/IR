import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import Cors from "cors";

function HomePage() {
  return (
    <div className="col-12 text-center">
      <h1>Data-Sets</h1>
      <div>
        <button className="col-4 btn btn-success mt-4 text-center p-4">
          <Link className="text-light" href="/covid">
            Covid Data-Set
          </Link>
        </button>
      </div>
      <div>
        <button className="col-4 btn btn-success mt-4 text-center p-4">
          <Link className="text-light" href="/clinc">
            Clinc Data-set
          </Link>
        </button>
      </div>
    </div>
  );
}

export default HomePage;
