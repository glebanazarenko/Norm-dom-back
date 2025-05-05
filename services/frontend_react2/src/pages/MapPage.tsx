import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios'; // ✅ Не забудьте импортировать axios
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet.markercluster';
import { useNavigate } from 'react-router-dom';
import { Star, MapPin, Loader2 } from 'lucide-react';

// Типизация данных
interface House {
  id: string;
  ADDRESS: string;
  geodata_center: {
    coordinates: [number, number];
  };
  rating?: number;
  reviews_count?: number;
}

// Конфигурация начального вида карты (центр Москвы)
const INITIAL_VIEW = {
  center: [55.751244, 37.618423] as [number, number],
  zoom: 10
};

const MapPage: React.FC = () => {
  const navigate = useNavigate();
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstance = useRef<L.Map | null>(null);
  const markersRef = useRef<L.MarkerClusterGroup | null>(null);
  const [houses, setHouses] = useState<House[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedHouse, setSelectedHouse] = useState<House | null>(null);

  // Загрузка данных из JSON
  useEffect(() => {
    const loadHouses = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('/houses.json');
        const data = await response.json();
        setHouses(data);
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadHouses();
  }, []);

  // Инициализация карты после загрузки данных
  useEffect(() => {
    if (!mapRef.current || !houses.length) return;

    if (mapInstance.current) {
      mapInstance.current.remove(); // Очистка старой карты
    }

    mapInstance.current = L.map(mapRef.current).setView(INITIAL_VIEW.center, INITIAL_VIEW.zoom);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors'
    }).addTo(mapInstance.current);

    // Создание кластеризатора
    markersRef.current = L.markerClusterGroup();

    // Добавление маркеров
    houses.forEach((house) => {
      const coordinates = house.geodata_center?.coordinates;
      if (coordinates && Array.isArray(coordinates) && coordinates.length === 2) {
        const [lat, lng] = coordinates; // ✅ Исправлено: сохраняем оригинальный порядок [широта, долгота]
      
        const marker = L.marker([lat, lng]) // ✅ Правильный порядок для Leaflet
          .bindPopup(house.ADDRESS || 'Нет адреса')
          .bindTooltip(house.ADDRESS || 'Нет адреса');
      
        marker.on('click', () => {
          setSelectedHouse(house);
        });
      
        markersRef.current?.addLayer(marker);
      } else {
        console.warn('Некорректные координаты:', house);
      }
    });

    // Добавление кластеров на карту
    if (markersRef.current?.getLayers().length) {
      mapInstance.current.addLayer(markersRef.current);
    }

    // Автоматическое центрирование
    const validCoordinates = houses
      .map(h => h.geodata_center?.coordinates)
      .filter(Boolean) as [number, number][];

    if (validCoordinates.length > 0) {
      const bounds = L.latLngBounds(
        validCoordinates.map(([lat, lng]) => [lat, lng]) // ✅ Исправлено: без инверсии
      );
      mapInstance.current.fitBounds(bounds);
    }
  }, [houses]);

  // Очистка при размонтировании
  useEffect(() => {
    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove();
      }
    };
  }, []);

  const handleViewHouse = async () => {
    if (!selectedHouse) return;
  
    try {
      // 1. Отправляем запрос к бэкенду
      const response = await axios.get(`/houses/search`, {
        params: {
          query: selectedHouse.ADDRESS // ✅ Передаем адрес как параметр запроса
        }
      });
  
      // 2. Проверяем, что вернулся хотя бы один дом
      if (response.data.length === 0) {
        throw new Error('Дом не найден');
      }
  
      // 3. Получаем ID первого найденного дома
      const houseId = response.data[0].id;
  
      // 4. Переходим на страницу деталей
      navigate(`/house/${houseId}`);
      
    } catch (error) {
      console.error('Ошибка при поиске дома:', error);
      alert('Не удалось найти дом. Попробуйте еще раз.');
    }
  };

  const handlePopupClose = () => {
    setSelectedHouse(null);
  };

  return (
    <div className="h-[calc(100vh-160px)] min-h-[500px] flex flex-col">
      <div className="mb-4">
        <h1 className="text-3xl font-bold mb-2">Карта домов</h1>
      </div>
      <div className="relative flex-grow border rounded-lg overflow-hidden">
        <div ref={mapRef} id="map" className="w-full h-full" />

        {/* Стили для карты */}
        <style jsx>{`
          /* Скрыть атрибуцию Leaflet */
          .leaflet-attribution-flag {
            display: none !important;
          }
        `}</style>

        {/* Попап при клике на маркер */}
        {selectedHouse && (
          <div
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded shadow-lg"
            style={{ zIndex: 1000 }}
          >
            <h3 className="font-semibold mb-1">{selectedHouse.ADDRESS}</h3>
            {selectedHouse.rating !== undefined && (
              <div className="flex items-center mb-1">
                <Star className="h-4 w-4 text-yellow-500 fill-yellow-500 mr-1" />
                <span>{selectedHouse.rating.toFixed(1)}</span>
                {selectedHouse.reviews_count !== undefined && (
                  <span className="text-sm text-gray-500 ml-1">
                    ({selectedHouse.reviews_count} отзывов)
                  </span>
                )}
              </div>
            )}
            <button
              onClick={handleViewHouse}
              className="w-full mt-2 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
            >
              Подробнее
            </button>
            <button
              onClick={handlePopupClose}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
            >
              &times;
            </button>
          </div>
        )}

        {/* Overlay для загрузки */}
        {isLoading && (
          <div className="absolute inset-0 bg-white bg-opacity-70 flex items-center justify-center">
            <div className="bg-white p-4 rounded-lg shadow-md flex items-center">
              <Loader2 className="animate-spin text-blue-500 mr-3" size={24} />
              <span className="text-gray-800">Загрузка домов...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MapPage;