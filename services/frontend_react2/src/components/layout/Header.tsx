import React, { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Home, Search, Map, LogIn, UserCircle, Menu, X } from 'lucide-react';

const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const activeClassName = "text-blue-600 font-semibold";
  const inactiveClassName = "text-gray-700 hover:text-blue-500 transition-colors";
  
  const navItems = [
    { to: '/', text: 'Главная', icon: <Home size={18} /> },
    { to: '/search', text: 'Поиск домов', icon: <Search size={18} /> },
    { to: '/map', text: 'Карта', icon: <Map size={18} /> }
  ];

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Home className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-blue-800">НормДом</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) => isActive ? activeClassName : inactiveClassName}
              >
                <div className="flex items-center space-x-1">
                  {item.icon}
                  <span>{item.text}</span>
                </div>
              </NavLink>
            ))}
          </nav>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <div className="flex items-center space-x-2 text-gray-700">
                  <UserCircle size={20} />
                  <span>{user?.username}</span>
                </div>
                <div className="flex space-x-2">
                  <Link to="/profile" className="px-4 py-2 text-sm rounded-md border border-blue-500 text-blue-500 hover:bg-blue-50 transition-colors">
                    Профиль
                  </Link>
                  {user?.role_name === 'Admin' && (
                    <Link to="/admin" className="px-4 py-2 text-sm rounded-md border border-purple-500 text-purple-500 hover:bg-purple-50 transition-colors">
                      Админ панель
                    </Link>
                  )}
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 text-sm rounded-md bg-red-500 text-white hover:bg-red-600 transition-colors"
                  >
                    Выход
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="flex items-center space-x-1 px-4 py-2 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition-colors">
                  <LogIn size={18} />
                  <span>Вход</span>
                </Link>
                <Link to="/register" className="px-4 py-2 rounded-md border border-blue-500 text-blue-500 hover:bg-blue-50 transition-colors">
                  Регистрация
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button className="md:hidden" onClick={toggleMenu}>
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden px-4 pb-4">
          <nav className="flex flex-col space-y-3">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) => `py-2 ${isActive ? activeClassName : inactiveClassName}`}
                onClick={() => setIsMenuOpen(false)}
              >
                <div className="flex items-center space-x-2">
                  {item.icon}
                  <span>{item.text}</span>
                </div>
              </NavLink>
            ))}
            <div className="h-px bg-gray-200 my-2"></div>
            {isAuthenticated ? (
              <>
                <div className="py-2 flex items-center space-x-2 text-gray-700">
                  <UserCircle size={20} />
                  <span>{user?.username}</span>
                </div>
                <Link
                  to="/profile"
                  className="py-2 text-blue-500"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Профиль
                </Link>
                {user?.role_name === 'Admin' && (
                  <Link
                    to="/admin"
                    className="py-2 text-purple-500"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Админ панель
                  </Link>
                )}
                <button
                  onClick={handleLogout}
                  className="py-2 text-red-500 text-left"
                >
                  Выход
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="py-2 text-blue-500"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Вход
                </Link>
                <Link
                  to="/register"
                  className="py-2 text-blue-500"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Регистрация
                </Link>
              </>
            )}
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header;