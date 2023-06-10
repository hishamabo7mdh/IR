import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import Cors from "cors";

function HomePage() {
  const [map, setMap] = useState("");
  const [avp, setAvp] = useState("");
  const [mrr, setMrr] = useState("");
  const [precession, setPrecesion] = useState("");
  const [recall, setRecall] = useState("");
  const [searchResults, setsearchResults] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const handleSearch = () => {
    setIsLoading(true);
    axios
      .get("http://localhost:5000/map")
      .then((response) => {
        const { map, mrr, avp, pr, rec } = response.data;
        setMap(map);
        setAvp(avp);
        setMrr(mrr);
        setPrecesion(pr);
        setRecall(rec);
        setIsLoading(false);
        setsearchResults(true);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="col-12 text-center">
      <h1>Covid Data-Set</h1>
      <div>
        <button className="col-4 btn btn-success mt-4 text-center p-4">
          <Link className="text-light" href="/search">
            Search page
          </Link>
        </button>
      </div>
      <div>
        <button
          className="col-4 btn btn-success mt-4 text-center p-4"
          onClick={handleSearch}
        >
          Get the MAP
        </button>

        {isLoading ? (
          <p>Loading...</p>
        ) : (
          searchResults && (
            <div>
              <p className="btn btn-Success text-dark col-6 mt-3">
                The MAP is = {map}
              </p>
              <p className="btn btn-Success text-dark col-6 mt-3">
                The MRR is = {mrr}
              </p>
              <p className="btn btn-Success text-dark col-6 mt-3">
                The AVP is = {avp}
              </p>
              <p className="btn btn-Success text-dark col-6 mt-3">
                The Precession is = {precession}
              </p>
              <p className="btn btn-Success text-dark col-6 mt-3">
                The Recall is = {recall}
              </p>
            </div>
          )
        )}
      </div>
    </div>
  );
}

export default HomePage;
