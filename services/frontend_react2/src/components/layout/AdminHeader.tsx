import React from 'react';
import { Home, LogOut } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const AdminHeader: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-gray-900 text-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <Link to="/admin" className="flex items-center space-x-2">
              <Home className="h-6 w-6 text-blue-400" />
              <span className="text-xl font-bold">НормДом</span>
            </Link>
            <div className="px-3 py-1 bg-purple-700 rounded-md text-sm">
              Панель администратора
            </div>
          </div>

          <div className="flex items-center space-x-6">
            <div className="text-gray-300">
              {user?.username} (Администратор)
            </div>
            <div className="flex space-x-2">
              <Link to="/" className="px-3 py-1 text-sm rounded-md text-white hover:bg-gray-700 transition-colors">
                На сайт
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-1 px-3 py-1 text-sm rounded-md bg-red-600 text-white hover:bg-red-700 transition-colors"
              >
                <LogOut size={16} />
                <span>Выход</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default AdminHeader;