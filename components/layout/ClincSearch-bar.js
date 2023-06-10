import { useState } from "react";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/router";
import queriesData from "../../ClincSuggesstions.json";

const ClincSearchBar = () => {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [precession, setPrecession] = useState("");
  const [avp, setAvp] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  const handleInputChange = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    const matchingQueries = queriesData.queries.filter((item) => {
      // Convert both query and item.query to lowercase for case-insensitive comparison
      const lowercaseQuery = query.toLowerCase();
      const lowercaseItemQuery =
        typeof item.query === "string" ? item.query.toLowerCase() : "";

      // Split the query into individual words
      const queryWords = lowercaseQuery.split(" ");

      // Check if any word in the query is similar to any word in item.query
      return queryWords.some((word) => lowercaseItemQuery.includes(word));
    });

    const querySuggestions = matchingQueries.flatMap(
      (item) => item.suggestions
    );
    var limitedSuggestions = [];
    var words = query;
    const lastChar = words[words.length - 1];
    if (lastChar === " ") {
      console.log(words);
      axios
        .get("http://localhost:5000/spellCheck?q=" + words)
        .then((response) => {
          words = response.data.correctedText;
          words = words.join(" ");
          console.log(words + " corrected");
          limitedSuggestions.push(words);
          setSuggestions(limitedSuggestions);
        })
        .catch((error) => {
          console.log(error);
        });
    } else {
      querySuggestions.slice(0, 5).forEach((suggestion) => {
        limitedSuggestions.push(suggestion);
      });
      setSuggestions(limitedSuggestions);
    }
  };

  const handleSearch = () => {
    setIsLoading(true);
    axios
      .get("http://localhost:5000/Clincsearch?q=" + searchQuery)
      .then((response) => {
        setSearchResults(response.data.documents);
        setAvp(response.data.Avp);
        setPrecession(response.data.precission);
        setIsLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleClick = (id, title, description) => {
    router.push({
      pathname: `/clinc-result/${id}`,
      query: { title, description },
    });
  };

  const handleSuggest = (value) => {
    setSearchQuery(value);
  };

  return (
    <div className="col-4 text-center p-4 mx-auto">
      <input
        className="col-3 p-4 form form-control mx-auto mt-3"
        type="text"
        placeholder="Enter your search query"
        value={searchQuery}
        onChange={handleInputChange}
      />
      {suggestions.length > 0 && (
        <ul className="mx-auto p-1">
          {suggestions.map((suggestion, index) => (
            <li className="form form-control mt-1 mx-auto" key={index}>
              <a onClick={() => handleSuggest(suggestion)}> {suggestion} </a>
            </li>
          ))}
        </ul>
      )}
      <button
        className=" col-12 p-2 btn btn-success mx-auto mt-3"
        onClick={handleSearch}
      >
        Search
      </button>

      {isLoading ? (
        <p>Loading...</p>
      ) : (
        searchResults.length > 0 && (
          <div>
            <p>The avaerage precession is = {avp} </p>
            <p>The precession is = {precession}</p>

            <ul>
              {searchResults.map((result) => (
                <li
                  className=" col-12 p-2 form from-control mt-2 list-group-item list-group-item-info text-primary rounded"
                  key={result.id}
                >
                  <button
                    onClick={() =>
                      handleClick(result.id, result.title, result.description)
                    }
                  >
                    {result.title}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )
      )}
    </div>
  );
};

export default ClincSearchBar;
