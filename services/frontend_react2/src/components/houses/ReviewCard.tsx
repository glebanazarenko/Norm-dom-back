import React, { useState } from 'react';
import { Star, Edit, Trash } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import EditReviewForm from './EditReviewForm';

interface ReviewCardProps {
  review: {
    id: string;
    house: {
      id: string;
      simple_address: string;
    };
    user_id: string;
    rating: number;
    review_text: string;
    is_published: boolean;
    created_at: string;
    modified_at: string;
  };
  canEdit?: boolean;
  onEditSuccess?: () => void;
}

const ReviewCard: React.FC<ReviewCardProps> = ({ review, canEdit, onEditSuccess }) => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const renderStars = (rating: number) => {
    return Array(5).fill(0).map((_, i) => (
      <Star 
        key={i} 
        className={`h-4 w-4 ${i < rating ? 'text-yellow-500 fill-yellow-500' : 'text-gray-300'}`} 
      />
    ));
  };

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleEditCancel = () => {
    setIsEditing(false);
  };

  const handleEditSuccess = () => {
    setIsEditing(false);
    if (onEditSuccess) {
      onEditSuccess();
    }
  };

  const userCanEdit = canEdit;

  if (isEditing) {
    return (
      <EditReviewForm
        reviewId={review.id}
        initialRating={review.rating}
        initialText={review.review_text}
        onCancel={handleEditCancel}
        onSuccess={handleEditSuccess}
      />
    );
  }

  return (
    <div className={`p-4 border rounded-lg mb-4 ${!review.is_published ? 'bg-gray-50 border-gray-300' : 'bg-white border-gray-200'}`}>
      {review.house && (
        <div className="text-sm text-gray-500 mb-2">
          {review.house.simple_address}
        </div>
      )}
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center space-x-2">
            <div className="flex">{renderStars(review.rating)}</div>
            <span className="font-medium text-gray-700">{user?.full_name || 'Пользователь'}</span>
          </div>
          <div className="text-xs text-gray-500">
            {formatDate(review.created_at)}
            {review.modified_at !== review.created_at && 
              ` (ред. ${formatDate(review.modified_at)})`}
          </div>
        </div>
        
        {userCanEdit && (
          <button 
            onClick={handleEditClick}
            className="p-1 text-blue-600 hover:text-blue-800 transition-colors"
            title="Редактировать отзыв"
          >
            <Edit size={18} />
          </button>
        )}
      </div>
      
      <div className="mt-3">
        <p className="text-gray-800">{review.review_text}</p>
      </div>
      
      {!review.is_published && (
        <div className="mt-2 text-sm text-orange-600 bg-orange-50 p-2 rounded">
          Этот отзыв находится на модерации и будет опубликован после проверки.
        </div>
      )}
    </div>
  );
};

export default ReviewCard;