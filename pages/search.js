import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import Cors from "cors";
import SearchBar from "../components/layout/search-bar";

const SearchPage = () => {
  return (
    <div className="col-12 text-center">
      <h1>Covid Data-Set</h1>
      <SearchBar className="col-12 text-center p-4" />
    </div>
  );
};

export default SearchPage;
