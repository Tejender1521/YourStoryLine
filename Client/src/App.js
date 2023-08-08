import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./component/Home/Home";
import React from "react";
import Demo from "./component/Demo/Demo";
import "mapbox-gl/dist/mapbox-gl.css";
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/demo" element={<Demo />} />
      </Routes>
    </BrowserRouter>
  );
}
 