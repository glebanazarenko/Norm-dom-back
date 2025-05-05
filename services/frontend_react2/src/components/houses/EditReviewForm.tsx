import React, { useState } from 'react';
import { Star } from 'lucide-react';
import { editReview } from '../../api/house';
import { toast } from 'react-toastify';

interface EditReviewFormProps {
  reviewId: string;
  initialRating: number;
  initialText: string;
  onCancel: () => void;
  onSuccess: () => void;
}

const EditReviewForm: React.FC<EditReviewFormProps> = ({
  reviewId,
  initialRating,
  initialText,
  onCancel,
  onSuccess
}) => {
  const [rating, setRating] = useState(initialRating);
  const [reviewText, setReviewText] = useState(initialText);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewText.trim()) {
      toast.error('Пожалуйста, введите текст отзыва');
      return;
    }
    
    try {
      setIsSubmitting(true);
      await editReview(reviewId, rating, reviewText);
      toast.success('Отзыв отправлен на модерацию');
      onSuccess();
    } catch (error) {
      toast.error('Ошибка при редактировании отзыва');
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="p-4 border rounded-lg mb-4 bg-blue-50 border-blue-200">
      <h3 className="text-lg font-semibold mb-2">Редактирование отзыва</h3>
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
            required
          />
        </div>
        
        <div className="flex justify-end space-x-2">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-100 transition-colors"
            disabled={isSubmitting}
          >
            Отмена
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:bg-blue-400"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Сохранение...' : 'Сохранить'}
          </button>
        </div>
        
        <div className="mt-3 text-sm text-blue-600">
          Примечание: После редактирования отзыв будет отправлен на повторную модерацию.
        </div>
      </form>
    </div>
  );
};

export default EditReviewForm;