import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Star } from 'lucide-react';

interface HouseCardProps {
  house: {
    id: string;
    simple_address: string;
    rating?: number | string;
    district: string;
    adm_area: string;
    rating_count: string;
    reviews: any[];
  };
}

const HouseCard: React.FC<HouseCardProps> = ({ house }) => {
  return (
    <Link to={`/house/${house.id}`} className="block">
      <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:translate-y-[-4px] hover:shadow-lg">
        <div className="p-5">
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-2">
              <MapPin className="h-5 w-5 text-blue-500 mt-0.5" />
              <h3 className="text-lg font-semibold text-gray-800">{house.simple_address}</h3>
            </div>
            
            {house.rating !== undefined && (
              <div className="flex items-center space-x-1 bg-yellow-100 px-2 py-1 rounded">
                <Star className="h-4 w-4 text-yellow-500 fill-yellow-500" />
                <span className="font-semibold text-sm">{house.rating}</span>
              </div>
            )}
          </div>
          
          <div className="mt-4 grid grid-cols-2 gap-4">
            {house.district && (
              <div>
                <span className="text-sm text-gray-500">Район</span>
                <p className="text-gray-800">{house.district}</p>
              </div>
            )}
            
            {house.adm_area && (
              <div>
                <span className="text-sm text-gray-500">Округ</span>
                <p className="text-gray-800">{house.adm_area}</p>
              </div>
            )}
          </div>
          
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-500">
                {house.rating_count ? `${house.rating_count} отзыва(ов)` : 'Нет отзывов'}
              </span>
              <span className="text-blue-500 text-sm">Подробнее →</span>
            </div>
          </div>
        </div>
      </div>
    </Link>
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

export default HouseCard;