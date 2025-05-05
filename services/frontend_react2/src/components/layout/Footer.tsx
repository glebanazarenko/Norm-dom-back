import React from 'react';
import { Home, Mail, Phone } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Home className="h-6 w-6 text-blue-400" />
              <span className="text-xl font-bold">НормДом</span>
            </div>
            <p className="text-gray-300">
              Сервис для поиска и оценки домов в Москве, объединяющий открытые данные и отзывы жителей.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Навигация</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-300 hover:text-white transition-colors">Главная</a>
              </li>
              <li>
                <a href="/search" className="text-gray-300 hover:text-white transition-colors">Поиск домов</a>
              </li>
              <li>
                <a href="/map" className="text-gray-300 hover:text-white transition-colors">Карта</a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Контакты</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Mail className="h-5 w-5 text-blue-400" />
                <span>info@normdom.ru</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="h-5 w-5 text-blue-400" />
                <span>+7 (999) 123-45-67</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-6 text-center">
          <p className="text-gray-400">© 2025 НормДом. Все права защищены.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;