import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { searchHouses } from '../api/house';
import HouseCard from '../components/houses/HouseCard';
import { useNavigate } from 'react-router-dom';
import { MapPin, Search, Loader2, X } from 'lucide-react';
import axios from 'axios';

const SearchPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [selectedAdmArea, setSelectedAdmArea] = useState<string | null>(null);
  const [selectedDistrict, setSelectedDistrict] = useState<string | null>(null);
  const [minRating, setMinRating] = useState<number>(0);
  const [hasReviews, setHasReviews] = useState<boolean>(false);
  const [admAreas, setAdmAreas] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [isLoadingFilters, setIsLoadingFilters] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFilters = async () => {
      try {
        // Извлекаем уникальные adm_areas и districts
        const response_2 = await axios.get('/houses/unique-adm-areas');
        const AdmAreas = response_2.data.adm_areas; // Доступ к правильному ключу
        const uniqueAdmAreas = Array.from(new Set(AdmAreas.map((area: any) => area.name)))
          .sort((a: string, b: string) => a.localeCompare(b, 'ru'));
  
        const response_3 = await axios.get('/houses/unique-districts');
        const Districts = response_3.data.districts; // Доступ к правильному ключу
        const uniqueDistricts = Array.from(new Set(Districts.map((district: any) => district.name)))
          .sort((a: string, b: string) => a.localeCompare(b, 'ru'));
  
        setAdmAreas(uniqueAdmAreas);
        setDistricts(uniqueDistricts);
      } catch (error) {
        console.error('Error fetching filters:', error);
      } finally {
        setIsLoadingFilters(false);
      }
    };
  
    fetchFilters();
  }, []);

  // Fetch search results
  const handleSearch = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!searchQuery.trim() && !selectedAdmArea && !selectedDistrict && minRating <= 0 && !hasReviews) return;

    setIsLoading(true);
    setHasSearched(true);
    try {
      const response = await axios.get(`/houses/search?query=${encodeURIComponent(searchQuery)}`);
      let filteredResults = [...response.data];

      // Apply adm_area filter
      if (selectedAdmArea) {
        filteredResults = filteredResults.filter((house: any) => house.adm_area === selectedAdmArea);
      }

      // Apply district filter
      if (selectedDistrict) {
        filteredResults = filteredResults.filter((house: any) => house.district === selectedDistrict);
      }

      // Apply min rating filter
      if (minRating > 0) {
        filteredResults = filteredResults.filter((house: any) => {
          const rating = parseFloat(house.rating);
          return !isNaN(rating) && rating >= minRating;
        });
      }

      // Apply has reviews filter
      if (hasReviews) {
        filteredResults = filteredResults.filter((house: any) => house.reviews.length > 0);
      }

      setSearchResults(filteredResults);
      setTotalPages(Math.ceil(filteredResults.length / 10));
      setCurrentPage(1);
    } catch (error) {
      console.error('Error searching houses:', error);
      setSearchResults([]);
      setTotalPages(1);
    } finally {
      setIsLoading(false);
    }
  };

  // Clear search and filters
  const clearSearch = () => {
    setSearchQuery('');
    setSearchResults([]);
    setHasSearched(false);
    setSelectedAdmArea(null);
    setSelectedDistrict(null);
    setMinRating(0);
    setHasReviews(false);
    setCurrentPage(1);
  };

  // Paginate results
  const resultsPerPage = 10;
  const paginatedResults = searchResults.slice((currentPage - 1) * resultsPerPage, currentPage * resultsPerPage);

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Поиск домов</h1>
        <p className="text-gray-600">
          Введите адрес или часть адреса для поиска домов в базе данных
        </p>
      </div>

      <div className="mb-8">
        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="relative flex-grow">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Например: Садовая улица"
              className="w-full p-3 pl-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            {searchQuery && (
              <button
                type="button"
                onClick={clearSearch}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <X size={18} />
              </button>
            )}
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
            disabled={isLoading || !searchQuery.trim()}
          >
            {isLoading ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                <span>Поиск...</span>
              </>
            ) : (
              <>
                <Search size={20} />
                <span>Поиск</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Filters Section */}
      <div className="mb-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold mb-4">Фильтры</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Administrative Area Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Округ</label>
            <select
              value={selectedAdmArea || ''}
              onChange={(e) => setSelectedAdmArea(e.target.value || null)}
              className="w-full p-2 border rounded"
              disabled={isLoadingFilters}
            >
              <option value="">Все округа</option>
              {isLoadingFilters ? (
                <option>Загрузка...</option>
              ) : admAreas.length === 0 ? (
                <option>Нет данных</option>
              ) : (
                admAreas.map((area) => (
                  <option key={area} value={area}>
                    {area}
                  </option>
                ))
              )}
            </select>
          </div>

          {/* District Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Район</label>
            <select
              value={selectedDistrict || ''}
              onChange={(e) => setSelectedDistrict(e.target.value || null)}
              className="w-full p-2 border rounded"
              disabled={isLoadingFilters}
            >
              <option value="">Все районы</option>
              {isLoadingFilters ? (
                <option>Загрузка...</option>
              ) : districts.length === 0 ? (
                <option>Нет данных</option>
              ) : (
                districts.map((district) => (
                  <option key={district} value={district}>
                    {district}
                  </option>
                ))
              )}
            </select>
          </div>

          {/* Min Rating Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Минимальный рейтинг</label>
            <input
              type="number"
              min="0"
              max="5"
              step="0.5"
              value={minRating}
              onChange={(e) => setMinRating(parseFloat(e.target.value))}
              className="w-full p-2 border rounded"
              placeholder="0.0"
            />
          </div>

          {/* Has Reviews Filter */}
          <div>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={hasReviews}
                onChange={(e) => setHasReviews(e.target.checked)}
                className="rounded text-blue-600"
              />
              <span className="text-sm text-gray-700">Только с отзывами</span>
            </label>
          </div>
        </div>
      </div>

      {/* Results Display */}
      <div className="mb-8">
        {isLoading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="animate-spin text-blue-500 h-10 w-10" />
            <span className="ml-3 text-lg text-gray-600">Загрузка домов...</span>
          </div>
        ) : hasSearched && searchResults.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-xl text-gray-600 mb-2">По запросу ничего не найдено</p>
            <p className="text-gray-500">Попробуйте изменить запрос или уточнить адрес</p>
          </div>
        ) : hasSearched ? (
          <>
            <div className="mb-4 flex justify-between items-center">
              <p className="text-gray-600">Найдено домов: {searchResults.length}</p>
              {/* <Link to="/map" className="text-blue-600 hover:text-blue-800 flex items-center gap-1">
                <MapPin size={16} />
                <span>Показать на карте</span>
              </Link> */}
            </div>
            <div className="grid gap-6 mb-8">
              {paginatedResults.map((house) => (
                <HouseCard key={house.id} house={house} />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center mt-8 mb-6">
                <div className="flex border border-gray-300 rounded-lg overflow-hidden">
                  <button
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="px-4 py-2 border-r border-gray-300 disabled:text-gray-400 hover:bg-gray-50"
                  >
                    Назад
                  </button>
                  {[...Array(totalPages)].map((_, i) => (
                    <button
                      key={i}
                      onClick={() => setCurrentPage(i + 1)}
                      className={`px-4 py-2 border-r border-gray-300 last:border-r-0 ${
                        currentPage === i + 1
                          ? 'bg-blue-600 text-white'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      {i + 1}
                    </button>
                  ))}
                  <button
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 disabled:text-gray-400 hover:bg-gray-50"
                  >
                    Вперёд
                  </button>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-16 bg-gray-50 rounded-lg">
            <MapPin className="mx-auto h-16 w-16 text-blue-400 mb-4" />
            <h2 className="text-2xl font-semibold mb-2">Введите адрес для поиска</h2>
            <p className="text-gray-600">
              Вы можете искать по улице, номеру дома или району
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;