import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import { motion } from "framer-motion";

const Home = () => {
  const navigate = useNavigate();
  const [isActive, setIsActive] = React.useState(false);

  const animate = () => {
    setIsActive(!isActive);
  };

  const animateMenu = (time) => `appear 0.5s forwards ease ${time}`;

  function goDemo() {
    navigate("/demo");
  }

  return (
    <>
      <div className={`container ${isActive ? "active" : ""}`}>
        <div className="navbar">
          <div className="menu">
            <h3 className="logo">
              {/* <span><img src={require("../../assests/applogo.png") } alt="logo"/></span> */}
            </h3>
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="hamburger-menu"
              onClick={animate}
            >
              <div className="bar"></div>
            </motion.div>
          </div>
        </div>

        <div className="main-container">
          <div className="main">
            <header>
              <div className="overlay">
                <div className="inner">
                  <h2 className="title">Text Geocoder</h2>
                  <p>
                    Text Mining tool that helps you to find relevent locations for a given text.
                  </p>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className="btn"
                    onClick={goDemo}
                  >
                    Demo
                  </motion.button>
                </div>
              </div>
            </header>
          </div>

          <div className="shadow one"></div>
          <div className="shadow two"></div>
        </div>

        <div className="links">
          <ul>
            <li>
              <a style={{ animation: animateMenu(0.5) }} href="/">
                Home
              </a>
            </li>
            <li>
              <a style={{ animation: animateMenu(1) }} href="services">
                Services
              </a>
            </li>
            <li>
              <a style={{ animation: animateMenu(1.5) }} href="about">
                About
              </a>
            </li>
            <li>
              <a style={{ animation: animateMenu(2) }} href="contact">
                Contact
              </a>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
};

export default Home;
