import { useNavigate } from "react-router-dom";
import "../styles/Header.css";

function Header() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <header className="app-header">
      <h2 className="logo" onClick={() => navigate("/")}>
        My Library
      </h2>

      <div className="header-actions">
        <button className="nav-button" onClick={() => navigate("/borrowed")}>
          My Borrowed Books
        </button>
        <button className="logout-button" onClick={handleLogout}>
          Log Out
        </button>
      </div>
    </header>
  );
}

export default Header;