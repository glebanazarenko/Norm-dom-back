import React, { useState } from 'react';
import { Star } from 'lucide-react';
import { addReviewToHouse } from '../../api/house';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-toastify';

interface AddReviewFormProps {
  houseId: string;
  onSuccess: () => void;
}

const AddReviewForm: React.FC<AddReviewFormProps> = ({ houseId, onSuccess }) => {
  const { isAuthenticated } = useAuth();
  const [rating, setRating] = useState(0);
  const [reviewText, setReviewText] = useState('');
  const [hoveredRating, setHoveredRating] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (rating === 0) {
      toast.error('Пожалуйста, выберите оценку');
      return;
    }
    
    if (!reviewText.trim()) {
      toast.error('Пожалуйста, введите текст отзыва');
      return;
    }
    
    try {
      setIsSubmitting(true);
      await addReviewToHouse(houseId, reviewText, rating);
      toast.success('Отзыв отправлен на модерацию');
      setRating(0);
      setReviewText('');
      onSuccess();
    } catch (error) {
      toast.error('Ошибка при добавлении отзыва');
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  if (!isAuthenticated) {
    return (
      <div className="p-4 bg-gray-50 border rounded-lg">
        <p className="text-center text-gray-700">
          Для оставления отзыва необходимо 
          <a href="/login" className="text-blue-600 mx-1 hover:underline">войти в аккаунт</a>
        </p>
      </div>
    );
  }
  
  return (
    <div className="p-4 bg-white border rounded-lg shadow-sm">
      <h3 className="text-lg font-semibold mb-4">Оставить отзыв</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1">Оценка</label>
          <div className="flex space-x-1">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => setRating(star)}
                onMouseEnter={() => setHoveredRating(star)}
                onMouseLeave={() => setHoveredRating(0)}
                className="p-1 focus:outline-none"
              >
                <Star 
                  className={`h-6 w-6 ${
                    (hoveredRating ? star <= hoveredRating : star <= rating)
                      ? 'text-yellow-500 fill-yellow-500' 
                      : 'text-gray-300'
                  }`} 
                />
              </button>
            ))}
          </div>
        </div>
        
        <div className="mb-4">
          <label htmlFor="reviewText" className="block text-gray-700 mb-1">
            Текст отзыва
          </label>
          <textarea
            id="reviewText"
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            rows={4}
            placeholder="Опишите ваши впечатления о доме..."
            required
          />
        </div>
        
        <button
          type="submit"
          className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:bg-blue-400"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Отправка...' : 'Отправить отзыв'}
        </button>
        
        <div className="mt-3 text-sm text-gray-600">
          Ваш отзыв будет опубликован после модерации.
        </div>
      </form>
    </div>
  );
};

export default AddReviewForm;