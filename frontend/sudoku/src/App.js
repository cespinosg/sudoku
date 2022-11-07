import React from "react";
import Header from "./components/Header.js";
import Footer from "./components/Footer.js";
import Grid from "./components/Grid.js";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Header />
      <Grid />
      {/* <Button /> Implemented button within Grid */}
      <Footer />
    </div>
  );
}

export default App;
