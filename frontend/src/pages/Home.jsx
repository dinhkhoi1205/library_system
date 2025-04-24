import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Home.css";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";

function Home() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [genre, setGenre] = useState("");
  const [borrowedBooks, setBorrowedBooks] = useState([]);
  const [debouncedSearch, setDebouncedSearch] = useState("");

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      setDebouncedSearch(search);
    }, 400);
    return () => clearTimeout(delayDebounce);
  }, [search]);

  useEffect(() => {
    fetchBooks();
  }, [debouncedSearch, genre]);

  const fetchBooks = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/books/", {
        params: {
          search: debouncedSearch,
          genre: genre || undefined,
        },
      });
      setBooks(res.data);
    } catch (error) {
      console.error("Failed to fetch books", error);
    } finally {
      setLoading(false);
    }
  };

  const handleBorrow = async (bookId) => {
    if (loading || borrowedBooks.includes(bookId)) return; // Prevent borrowing the same book again
    setLoading(true);
    
    try {
      const res = await api.post("/api/borrow/", { book_id: bookId });
      
      if (res.data) {
        console.log("Borrow success data:", res.data); // Assuming the response contains data
      }
      
      alert("Book borrowed successfully!");
      setBorrowedBooks([...borrowedBooks, bookId]); // Add book to the borrowed list
      fetchBooks(); // Refresh the list to get the updated available copies
    } catch (error) {
      alert("Failed to borrow book: " + error?.response?.data?.detail || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-container">
       <Header/>
      <h1>Available Books</h1>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search title or author"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={genre} onChange={(e) => setGenre(e.target.value)}>
          <option value="">All Genres</option>
          <option value="Fantasy">Fantasy</option>
          <option value="Science Fiction">Science Fiction</option>
          <option value="Mystery">Mystery</option>
          <option value="Romance">Romance</option>
          <option value="Thriller">Thriller</option>
        </select>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : books.length > 0 ? (
        <div className="book-grid">
          {books.map((book) => (
            <div key={book.id} className="book-card">
              {book.cover_image ? (
                <img
                  src={`${import.meta.env.VITE_API_URL}${book.cover_image}`}
                  alt={book.title}
                  className="book-cover"
                />
              ) : (
                <div className="book-placeholder">No Image</div>
              )}
              <h3>{book.title}</h3>
              <p><strong>Author:</strong> {book.author}</p>
              <p><strong>Genre:</strong> {book.genre}</p>
              <p><strong>Published Date:</strong> {book.published_date}</p>
              <p><strong>Available:</strong> {book.available_copies}</p>
              {/* Description directly displayed within the card */}
              <p><strong>Description:</strong> {book.description || "No description available."}</p>
              <button
                className="borrow-button"
                onClick={() => handleBorrow(book.id)}
                disabled={book.available_copies <= 0}
              >
                Borrow
              </button>
            </div>
          ))}
        </div>
      ) : (
        <p>No books found.</p>
      )}
    </div>
  );
}

export default Home;
