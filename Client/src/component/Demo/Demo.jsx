import React from "react";
import Jsonprettier from "../Jsonprettier/Jsonprettier";
import "./Demo.css";
import Loader from "../Loader/Loader";
import { motion } from "framer-motion";

import Mapbox from "../Map/Map";
import Highlighter from "react-highlight-words";

const Demo = () => {
  const [search, setSearch] = React.useState("");
  const [data, setData] = React.useState(null);
  const [manipulatedSearch, setManipulatedSearch] = React.useState(null);
  const [status, setStatus] = React.useState("search");
  const [searchData, setSearchData] = React.useState(null);
  const [loader, setLoader] = React.useState(false);
  const [isclose, setIsclose] = React.useState(false);

  const fetchData = async (e) => {
    setLoader(true);
    if (search.length <= 0 || loader) return;

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
      key: search,
    });
    var requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    try {
      let data = await fetch(
        "https://trfmodel.coi6htut061eo.ap-south-1.cs.amazonlightsail.com/geocoder",
        requestOptions
      );

      data = await data.json();

      data = data.replaceAll("None", null);

      manipulateData(data);
    } catch (error) {
      console.log("error", error);
      setLoader(false);
    }

  
  };

  const manipulateData = (data) => {
    let tempData = JSON.parse(data.replaceAll('"', "").replaceAll("'", '"'));
    setSearchData(tempData);
    tempData = Object.keys(tempData);
    setData(tempData);
    const tempManipulatedSearch = search;
    setTimeout(() => {
      setManipulatedSearch(tempManipulatedSearch);
      setStatus("result");
      setLoader(false);
    }, 2000);
  };

  const render = () => {
    switch (status) {
      case "search":
        return (
          <div className="text-area-container">
            <textarea
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="demo-textarea"
              placeholder="Enter text to search"
            />
            <div className="try">
              <button
                onClick={() =>
                  setSearch(
                    "The architectural splendor of Hawa Mahal, a honeycomb-like structure, stood tall, showcasing the city's rich history. Nahargarh Fort, perched atop the hills, offered a panoramic view of the Pink City. Bapu Bazaar enticed me with its colorful textiles, handicrafts, and traditional attire. The tranquil Jal Mahal, floating in the serene waters of Man Sagar Lake, provided a peaceful retreat. Additionally, I was mesmerized by the serene beauty of Albert Hall Museum, an exquisite Indo-Saracenic style building that houses a diverse collection of artifacts, paintings, and sculptures, offering a glimpse into the cultural heritage of Jaipur."
                  )
                }
              >
                Try It out
              </button>
            </div>
          </div>
        );
      case "result":
        return (
          <div className="result-container">
            <Highlighter
              searchWords={data}
              autoEscape={true}
              highlightStyle={{
                color: "#FF5B00",
                padding: "0 .2rem 0 .2rem",
                fontWeight: "bold",
                textDecoration: "underline",
                textDecorationColor: "#0E185F",
                textDecorationThickness: "2px",
                backgroundColor: "white",
              }}
              textToHighlight={search}
            />
          </div>
        );
      case "jsonData":
        return (
          <div className="result-container">
            <Jsonprettier data={searchData} />
          </div>
        );
      default:
        break;
    }
  };

  return (
    <div className="demo-main-container">
      <Mapbox data={searchData} />
      {!isclose ? (
        <div className="demo-search">
          <motion.i
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="fa-solid fa-chevron-left close-button"
            onClick={() => setIsclose(true)}
          ></motion.i>

          <div className="demo-search-subcontainer">
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="demo-search-subcontainer-item"
              onClick={() => {
                setStatus(manipulatedSearch ? "result" : "search");
              }}
            >
              <i className="fa fa-search icon-item" aria-hidden="true"></i>
              <p className="icon-item-text">Geocode</p>
            </motion.div>
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="demo-search-subcontainer-item"
              onClick={() => {
                manipulatedSearch && setStatus("jsonData");
              }}
            >
              <i className="fa fa-eye icon-item" aria-hidden="true"></i>
              <p className="icon-item-text">Result</p>
            </motion.div>
          </div>
          {!loader ? render() : <Loader />}
          {/* {render()} */}
          <div className="demo-footer">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => {
                if (!manipulatedSearch) fetchData();
                else {
                  setStatus("search");
                  setManipulatedSearch(null);
                }
              }}
            >
              {!manipulatedSearch ? "Geocode" : "Back"}
            </motion.button>
          </div>
        </div>
      ) : (
        <div className="demo-nosearch">
          <motion.i
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="fa-solid fa-chevron-right close-button"
            onClick={() => setIsclose(false)}
          ></motion.i>
        </div>
      )}
    </div>
  );
};

export default Demo;
