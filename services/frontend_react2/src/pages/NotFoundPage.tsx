import React from 'react';
import { Link } from 'react-router-dom';
import { Home, Search, Map } from 'lucide-react';

const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
        <h1 className="text-6xl font-bold text-gray-300 mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Страница не найдена</h2>
        <p className="text-gray-600 mb-6">
          Страница, которую вы ищете, не существует или была перемещена.
        </p>
        
        <div className="space-y-4">
          <Link
            to="/"
            className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            <Home className="mr-2" size={18} />
            <span>Вернуться на главную</span>
          </Link>
          
          <div className="grid grid-cols-2 gap-3">
            <Link
              to="/search"
              className="flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            >
              <Search className="mr-2" size={16} />
              <span>Поиск домов</span>
            </Link>
            
            <Link
              to="/map"
              className="flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            >
              <Map className="mr-2" size={16} />
              <span>Карта</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;