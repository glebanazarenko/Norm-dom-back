import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MapPin, Calendar, Building, Star, Loader2, ChevronLeft } from 'lucide-react';
import { getHouseById } from '../api/house';
import ReviewCard from '../components/houses/ReviewCard';
import AddReviewForm from '../components/houses/AddReviewForm';
import { useAuth } from '../contexts/AuthContext';

const HouseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const [house, setHouse] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHouseDetails = async () => {
    if (!id) return;
    
    setIsLoading(true);
    try {
      const houseData = await getHouseById(id);
      setHouse(houseData);
      setError(null);
    } catch (error) {
      console.error('Error fetching house details:', error);
      setError('Не удалось загрузить информацию о доме. Пожалуйста, попробуйте позже.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHouseDetails();
  }, [id]);

  const handleReviewAdded = () => {
    // Refresh house data to show the new review
    fetchHouseDetails();
  };

  // Helper function to check if user is super user
  const isSuperUser = () => {
    return user && user.role_name === 'Super User';
  };

  // Helper function to check if review belongs to current user
  const isUserReview = (reviewUserId: string) => {
   return user && user.id === reviewUserId;
  };

  // Filter reviews for display (only published ones for regular view)
  const getDisplayedReviews = () => {
    if (!house || !house.reviews) return [];
    
    // Only show published reviews to everyone
    return house.reviews.filter((review: any) => 
      review.is_published && !review.is_deleted
    );
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <Loader2 className="animate-spin text-blue-500 h-10 w-10" />
        <span className="ml-3 text-lg text-gray-600">Загрузка информации о доме...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-500 mb-4">{error}</div>
        <Link to="/search" className="text-blue-500 hover:underline flex items-center justify-center">
          <ChevronLeft size={16} />
          <span>Вернуться к поиску</span>
        </Link>
      </div>
    );
  }

  if (!house) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 mb-4">Дом не найден</div>
        <Link to="/search" className="text-blue-500 hover:underline flex items-center justify-center">
          <ChevronLeft size={16} />
          <span>Вернуться к поиску</span>
        </Link>
      </div>
    );
  }

  const displayedReviews = getDisplayedReviews();

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-4">
        <Link to="/search" className="text-blue-500 hover:underline flex items-center">
          <ChevronLeft size={16} />
          <span>Назад к результатам поиска</span>
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
        <div className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-start space-x-2">
              <MapPin className="h-6 w-6 text-blue-500 mt-1" />
              <h1 className="text-2xl font-bold text-gray-900">{house.full_address}</h1>
            </div>
            
            {house.rating !== undefined && (
              <div className="flex items-center space-x-1 bg-yellow-100 px-3 py-1 rounded-lg">
                <Star className="h-5 w-5 text-yellow-500 fill-yellow-500" />
                <span className="font-semibold">{house.rating}</span>
                <span className="text-sm text-gray-600">
                  ({house.rating_count || 0} {getReviewWord(house.rating_count || 0)})
                </span>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h2 className="text-lg font-semibold mb-3 text-gray-800">Информация о доме</h2>
              <ul className="space-y-3">
                {house.district && (
                  <li className="flex items-center space-x-2 text-gray-700">
                    {/* <Calendar className="h-5 w-5 text-gray-500" /> */}
                    <span>Район: <strong>{house.district}</strong></span>
                  </li>
                )}
                {house.adm_area && (
                  <li className="flex items-center space-x-2 text-gray-700">
                    {/* <Building className="h-5 w-5 text-gray-500" /> */}
                    <span>Округ: <strong>{house.adm_area}</strong></span>
                  </li>
                )}
                {house.kad_n && (
                  <li className="flex items-center space-x-2 text-gray-700">
                    <span>Кадастровый номер: <strong>{house.kad_n}</strong></span>
                  </li>
                )}
                {house.kad_zu && (
                  <li className="flex items-center space-x-2 text-gray-700">
                    <span>Кадастровый земельного участка: <strong>{house.kad_zu}</strong></span>
                  </li>
                )}
                {/* Display additional house information as needed */}
              </ul>
            </div>

            {house.latitude && house.longitude && (
              <div className="h-48 bg-gray-100 rounded-lg">
                {/* Map preview would go here */}
                <div className="h-full flex items-center justify-center text-gray-500">
                  <MapPin className="h-6 w-6 mr-2" />
                  <span>Карта (широта: {house.latitude}, долгота: {house.longitude})</span>
                </div>
              </div>
            )}
          </div>

          {house.description && (
            <div className="mb-6">
              <h2 className="text-lg font-semibold mb-2 text-gray-800">Описание</h2>
              <p className="text-gray-700">{house.description}</p>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          <h2 className="text-xl font-semibold mb-4">
            Отзывы о доме
            {displayedReviews.length > 0 && <span className="text-gray-500 ml-2">({displayedReviews.length})</span>}
          </h2>
          
          {displayedReviews.length > 0 ? (
            <div>
              {displayedReviews.map((review: any) => (
                <ReviewCard 
                  key={review.id} 
                  review={review} 
                  canEdit={isSuperUser() && isUserReview(review.user_id)}
                  onEditSuccess={fetchHouseDetails}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-8 bg-gray-50 rounded-lg">
              <p className="text-gray-600">Пока никто не оставил отзыв об этом доме</p>
              <p className="text-gray-500 mt-1">Будьте первым!</p>
            </div>
          )}
        </div>
        
        <div>
          <AddReviewForm houseId={house.id} onSuccess={handleReviewAdded} />
        </div>
      </div>
    </div>
  );
};

// Helper function to get the correct word form for reviews count
function getReviewWord(count: number): string {
  const lastDigit = count % 10;
  const lastTwoDigits = count % 100;
  
  if (lastTwoDigits >= 11 && lastTwoDigits <= 19) {
    return 'отзывов';
  }
  
  if (lastDigit === 1) {
    return 'отзыв';
  }
  
  if (lastDigit >= 2 && lastDigit <= 4) {
    return 'отзыва';
  }
  
  return 'отзывов';
}

export default HouseDetailPage;