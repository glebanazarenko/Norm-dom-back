import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Search, MapPin, MessageSquare, Building } from 'lucide-react';

const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="flex flex-col space-y-16">
      {/* Hero section */}
      <section className="relative">
        <div className="max-w-3xl mx-auto text-center py-12 px-4">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Найдите <span className="text-blue-600">идеальный дом</span> в Москве
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            НормДом — это сервис, который объединяет открытые данные о домах и отзывы реальных жителей
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/search" 
              className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
            >
              <Search size={20} />
              <span>Найти дом</span>
            </Link>
            <Link 
              to="/map" 
              className="px-6 py-3 bg-white text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors flex items-center justify-center gap-2"
            >
              <MapPin size={20} />
              <span>Открыть карту</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features section */}
      <section className="bg-gray-50 py-12 px-4 rounded-xl">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Почему НормДом?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md transition-transform hover:translate-y-[-8px]">
              <div className="bg-blue-100 w-14 h-14 rounded-full flex items-center justify-center mb-4">
                <Building className="h-7 w-7 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Актуальные данные</h3>
              <p className="text-gray-600">
                Мы загружаем и обновляем данные о домах из открытых источников Москвы для обеспечения актуальности информации.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md transition-transform hover:translate-y-[-8px]">
              <div className="bg-green-100 w-14 h-14 rounded-full flex items-center justify-center mb-4">
                <MessageSquare className="h-7 w-7 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Отзывы жителей</h3>
              <p className="text-gray-600">
                Реальные отзывы от жителей домов помогут вам получить объективную информацию о состоянии здания и района.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md transition-transform hover:translate-y-[-8px]">
              <div className="bg-purple-100 w-14 h-14 rounded-full flex items-center justify-center mb-4">
                <MapPin className="h-7 w-7 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Интерактивная карта</h3>
              <p className="text-gray-600">
                Удобная карта с кластеризацией позволит быстро найти интересующие вас дома в конкретном районе Москвы.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works section */}
      <section className="max-w-5xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">Как это работает</h2>
        <div className="space-y-12">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="bg-blue-100 rounded-full w-16 h-16 flex-shrink-0 flex items-center justify-center text-2xl font-bold text-blue-600">
              1
            </div>
            <div className="flex-grow">
              <h3 className="text-xl font-semibold mb-2">Найдите дом</h3>
              <p className="text-gray-600">
                Используйте поиск по адресу или интерактивную карту, чтобы найти интересующий вас дом в Москве. Система показывает всю доступную информацию из открытых данных.
              </p>
            </div>
          </div>

          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="bg-blue-100 rounded-full w-16 h-16 flex-shrink-0 flex items-center justify-center text-2xl font-bold text-blue-600">
              2
            </div>
            <div className="flex-grow">
              <h3 className="text-xl font-semibold mb-2">Изучите отзывы</h3>
              <p className="text-gray-600">
                Читайте отзывы реальных жителей о домах, чтобы получить объективное представление. Отзывы проходят модерацию для обеспечения их достоверности.
              </p>
            </div>
          </div>

          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="bg-blue-100 rounded-full w-16 h-16 flex-shrink-0 flex items-center justify-center text-2xl font-bold text-blue-600">
              3
            </div>
            <div className="flex-grow">
              <h3 className="text-xl font-semibold mb-2">Поделитесь опытом</h3>
              <p className="text-gray-600">
                Если вы живете в доме, оставьте свой отзыв и помогите другим пользователям. Ваш отзыв пройдет модерацию и будет опубликован на странице дома.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA section */}
      {!isAuthenticated ? (
        <section className="bg-blue-600 text-white rounded-xl overflow-hidden">
          <div className="max-w-4xl mx-auto py-12 px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Готовы найти свой идеальный дом?</h2>
            <p className="text-xl mb-8 text-blue-100">
              Присоединяйтесь к нашему сообществу и получайте актуальную информацию о домах в Москве
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/register" 
                className="px-6 py-3 bg-white text-blue-600 rounded-lg shadow-md hover:bg-gray-100 transition-colors"
              >
                Зарегистрироваться
              </Link>
              <Link 
                to="/search" 
                className="px-6 py-3 bg-blue-700 text-white border border-blue-400 rounded-lg hover:bg-blue-800 transition-colors"
              >
                Начать поиск
              </Link>
            </div>
          </div>
        </section>
      ) : (
        <></>
      )}
    </div>
  );
};

export default HomePage;