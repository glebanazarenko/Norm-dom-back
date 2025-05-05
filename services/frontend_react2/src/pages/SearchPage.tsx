import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, MapPin, X, Loader2 } from 'lucide-react';
import { searchHouses } from '../api/house';
import HouseCard from '../components/houses/HouseCard';

const SearchPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasSearched, setHasSearched] = useState(false);
  const resultsPerPage = 10;

  // Filtered results for current page
  const paginatedResults = searchResults.slice(
    (currentPage - 1) * resultsPerPage,
    currentPage * resultsPerPage
  );

  // Total pages
  const totalPages = Math.ceil(searchResults.length / resultsPerPage);

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    
    if (!searchQuery.trim()) return;
    
    setIsLoading(true);
    setHasSearched(true);
    
    try {
      const results = await searchHouses(searchQuery);
      setSearchResults(results);
      setCurrentPage(1);
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearSearch = () => {
    setSearchQuery('');
    setSearchResults([]);
    setHasSearched(false);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

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

      {isLoading ? (
        <div className="flex justify-center items-center py-20">
          <Loader2 className="animate-spin text-blue-500 h-10 w-10" />
          <span className="ml-3 text-lg text-gray-600">Выполняется поиск...</span>
        </div>
      ) : hasSearched ? (
        <>
          {searchResults.length > 0 ? (
            <div>
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
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="px-4 py-2 border-r border-gray-300 disabled:text-gray-400 hover:bg-gray-50"
                    >
                      Назад
                    </button>
                    
                    {[...Array(totalPages)].map((_, i) => (
                      <button
                        key={i}
                        onClick={() => handlePageChange(i + 1)}
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
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === totalPages}
                      className="px-4 py-2 disabled:text-gray-400 hover:bg-gray-50"
                    >
                      Вперёд
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 bg-gray-50 rounded-lg">
              <p className="text-xl text-gray-600 mb-2">По запросу «{searchQuery}» ничего не найдено</p>
              <p className="text-gray-500">Попробуйте изменить запрос или уточнить адрес</p>
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
  );
};

export default SearchPage;