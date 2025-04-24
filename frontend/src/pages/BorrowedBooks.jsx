import { useEffect, useState } from "react";
import api from "../api";

function BorrowedBooks() {
    const [borrowed, setBorrowed] = useState([]);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      fetchBorrowed();
    }, []);
  
    const fetchBorrowed = async () => {
      try {
        const res = await api.get("/api/borrowed/");
        setBorrowed(res.data);
      } catch (err) {
        console.error("Failed to fetch borrowed books", err);
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <div className="home-container">
        <h1>My Borrowed Books</h1>
        {loading ? (
          <p>Loading...</p>
        ) : borrowed.length > 0 ? (
          <div className="book-grid">
            {borrowed.map((record) => (
              <div key={record.id} className="book-card">
                <h3>{record.book.title}</h3>
                <p><strong>Borrowed on:</strong> {new Date(record.borrow_date).toLocaleDateString()}</p>
                <p><strong>Due date:</strong> {new Date(record.due_date).toLocaleDateString()}</p>
                <p><strong>Status:</strong> {record.status}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>You haven't borrowed any books.</p>
        )}
      </div>
    );
}

export default BorrowedBooks;