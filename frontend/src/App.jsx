import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState, useEffect, useMemo } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import MovieDetail from './pages/MovieDetail';
import BookPage from './pages/BookPage';
import Confirmation from './pages/Confirmation';
import { fetchMovies } from './api';
import './App.css';

function App() {
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({ genre: null, language: null, rating: null, release_year: null });
  const [genres, setGenres] = useState([]);
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    fetchMovies().then(data => {
      const movies = data.movies || [];
      setGenres(data.genres || [...new Set(movies.map(m => m.genre).filter(Boolean))].sort());
      setLanguages([...new Set(movies.map(m => m.language).filter(Boolean))].sort());
    }).catch(() => {});
  }, []);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <BrowserRouter>
      <div className="app">
        <Navbar
          search={search}
          onSearch={setSearch}
          filters={filters}
          onFilterChange={handleFilterChange}
          genres={genres}
          languages={languages}
        />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home search={search} filters={filters} />} />
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
