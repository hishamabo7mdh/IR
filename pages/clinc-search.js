import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import Cors from "cors";
import ClincSearchBar from "@/components/layout/ClincSearch-bar";

const SearchPage = () => {
  return (
    <div className="col-12 text-center">
      <h1>Clinc Data-Set </h1>
      <ClincSearchBar className="col-12 text-center p-4" />
    </div>
  );
};

export default SearchPage;
