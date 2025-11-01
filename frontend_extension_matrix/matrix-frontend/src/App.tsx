import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DeepfakeDetection from "./pages/deepfake";
import SpotTheFake from './components/SpotTheFake';
import "./App.css";

// Import your page components
import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import About from "./pages/About";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<SignIn />} />
        <Route path="/register" element={<SignUp />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/deepfake" element={<DeepfakeDetection />} />
        <Route path="/about" element={<About />} />
        <Route path="/spot-the-fake" element={<SpotTheFake />} />
      </Routes>
    </Router>
  );
}

export default App;
