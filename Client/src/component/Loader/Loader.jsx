import React from "react";
import './Loader.scss';
import loadgif from './loader.gif';
const Loader = () => {
  return <img className="main-loader" src={loadgif} alt="loader" />
  
};

export default Loader;
