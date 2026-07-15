import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import MovieDetail from './pages/MovieDetail';
import BookPage from './pages/BookPage';
import Confirmation from './pages/Confirmation';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/movie/:id" element={<MovieDetail />} />
            <Route path="/book/:showtimeId" element={<BookPage />} />
            <Route path="/confirmation/:ref" element={<Confirmation />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
