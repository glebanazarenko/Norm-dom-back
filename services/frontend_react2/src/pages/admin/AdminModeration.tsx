import React, { useState, useEffect } from 'react';
import { Check, X, Loader2, Filter } from 'lucide-react';
import { moderateReview } from '../../api/admin';
import { toast } from 'react-toastify';
import axios from 'axios';

interface Review {
  id: string;
  house_id: string;
  house_address?: string;
  user_id: string;
  username?: string;
  rating: number;
  review_text: string;
  created_at: string;
  modified_at: string;
}

const AdminModeration: React.FC = () => {
  const [pendingReviews, setPendingReviews] = useState<Review[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [processingReviews, setProcessingReviews] = useState<Record<string, boolean>>({});
  const [selectedReview, setSelectedReview] = useState<Review | null>(null);

  // For filtering and sorting
  const [sortOrder, setSortOrder] = useState<'newest' | 'oldest'>('newest');
  const [filterRating, setFilterRating] = useState<number | null>(null);

  // Fetch pending reviews
  useEffect(() => {
    const fetchPendingReviews = async () => {
      setIsLoading(true);
      try {
        // This is a mock endpoint - you'll need to create this endpoint on your backend
        const response = await axios.get('/admin/pending-reviews');
        setPendingReviews(response.data);
      } catch (error) {
        console.error('Error fetching pending reviews:', error);
        setError('Не удалось загрузить отзывы на модерацию');
        // For demo purposes, we'll use mock data
        setPendingReviews([
          {
            id: '1',
            house_id: 'house1',
            house_address: 'ул. Садовая, 123',
            user_id: 'user1',
            username: 'Иван',
            rating: 4,
            review_text: 'Очень хороший дом, но есть проблемы с отоплением зимой.',
            created_at: '2025-05-15T10:30:00Z',
            modified_at: '2025-05-15T10:30:00Z'
          },
          {
            id: '2',
            house_id: 'house2',
            house_address: 'ул. Ленина, 45',
            user_id: 'user2',
            username: 'Мария',
            rating: 2,
            review_text: 'Старый дом, постоянные проблемы с водой. ЖЭК не реагирует на жалобы.',
            created_at: '2025-05-14T15:20:00Z',
            modified_at: '2025-05-14T15:20:00Z'
          },
          {
            id: '3',
            house_id: 'house3',
            house_address: 'пр. Мира, 78',
            user_id: 'user3',
            username: 'Сергей_123',
            rating: 1,
            review_text: 'УЖАСНЫЙ ДОМ! НИКОМУ НЕ РЕКОМЕНДУЮ! МНОГО СПАМА И РЕКЛАМЫ ТУТ! ПЕРЕХОДИТЕ ПО ССЫЛКЕ WWW.SPAM.COM',
            created_at: '2025-05-13T09:15:00Z',
            modified_at: '2025-05-13T09:15:00Z'
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPendingReviews();
  }, []);

  // Handle moderation action
  const handleModerateReview = async (reviewId: string, action: 'approve' | 'reject') => {
    // Mark this review as processing
    setProcessingReviews(prev => ({ ...prev, [reviewId]: true }));

    try {
      await moderateReview(reviewId, action);
      
      // Remove the review from the list
      setPendingReviews(prev => prev.filter(review => review.id !== reviewId));
      
      // If it was the selected review, clear the selection
      if (selectedReview && selectedReview.id === reviewId) {
        setSelectedReview(null);
      }
      
      toast.success(`Отзыв успешно ${action === 'approve' ? 'одобрен' : 'отклонен'}`);
    } catch (error) {
      console.error(`Error ${action}ing review:`, error);
      toast.error(`Ошибка при ${action === 'approve' ? 'одобрении' : 'отклонении'} отзыва`);
    } finally {
      // Remove processing state
      setProcessingReviews(prev => {
        const newState = { ...prev };
        delete newState[reviewId];
        return newState;
      });
    }
  };

  // Handle review selection
  const handleSelectReview = (review: Review) => {
    setSelectedReview(review);
  };

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Apply filters and sorting
  const getFilteredAndSortedReviews = () => {
    let filtered = [...pendingReviews];
    
    // Apply rating filter
    if (filterRating !== null) {
      filtered = filtered.filter(review => review.rating === filterRating);
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();
      return sortOrder === 'newest' ? dateB - dateA : dateA - dateB;
    });
    
    return filtered;
  };

  const filteredReviews = getFilteredAndSortedReviews();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Модерация отзывов</h1>

      {isLoading ? (
        <div className="flex justify-center items-center py-20">
          <Loader2 className="animate-spin text-blue-500 h-10 w-10" />
          <span className="ml-3 text-lg text-gray-600">Загрузка отзывов на модерацию...</span>
        </div>
      ) : error ? (
        <div className="text-center py-10 bg-red-50 text-red-600 rounded-lg">
          {error}
        </div>
      ) : pendingReviews.length === 0 ? (
        <div className="text-center py-10 bg-green-50 text-green-600 rounded-lg">
          <p className="text-lg font-semibold">Нет отзывов, требующих модерации</p>
          <p className="mt-1">Все отзывы обработаны</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1">
            <div className="bg-white rounded-lg shadow-md overflow-hidden mb-4">
              <div className="p-4 bg-gray-50 border-b flex justify-between items-center">
                <h2 className="font-semibold">
                  Отзывы на модерацию ({filteredReviews.length})
                </h2>
                <div className="flex items-center">
                  <Filter size={16} className="text-gray-500 mr-1" />
                  <select
                    value={sortOrder}
                    onChange={(e) => setSortOrder(e.target.value as 'newest' | 'oldest')}
                    className="text-sm border-none bg-transparent"
                  >
                    <option value="newest">Сначала новые</option>
                    <option value="oldest">Сначала старые</option>
                  </select>
                </div>
              </div>
              
              <div className="px-4 py-2 border-b">
                <div className="flex space-x-1">
                  <button
                    onClick={() => setFilterRating(null)}
                    className={`px-2 py-1 text-xs rounded ${
                      filterRating === null
                        ? 'bg-blue-100 text-blue-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    Все
                  </button>
                  {[1, 2, 3, 4, 5].map(rating => (
                    <button
                      key={rating}
                      onClick={() => setFilterRating(rating)}
                      className={`px-2 py-1 text-xs rounded ${
                        filterRating === rating
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}
                    >
                      {rating}★
                    </button>
                  ))}
                </div>
              </div>
              
              <div className="overflow-y-auto max-h-[600px]">
                {filteredReviews.map(review => (
                  <div
                    key={review.id}
                    onClick={() => handleSelectReview(review)}
                    className={`p-4 border-b cursor-pointer hover:bg-gray-50 transition-colors ${
                      selectedReview?.id === review.id ? 'bg-blue-50' : ''
                    }`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-medium">{review.username || 'Пользователь'}</p>
                        <p className="text-sm text-gray-600">{review.house_address}</p>
                      </div>
                      <div className="bg-gray-100 px-2 py-1 rounded text-sm">
                        {review.rating} ★
                      </div>
                    </div>
                    <p className="text-sm text-gray-800 line-clamp-2 mb-1">{review.review_text}</p>
                    <p className="text-xs text-gray-500">{formatDate(review.created_at)}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="md:col-span-2">
            {selectedReview ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start mb-6">
                  <h2 className="text-xl font-semibold">Детали отзыва</h2>
                  <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                    На модерации
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Автор</p>
                    <p className="font-medium">{selectedReview.username || 'Пользователь'}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Дата создания</p>
                    <p className="font-medium">{formatDate(selectedReview.created_at)}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Дом</p>
                    <p className="font-medium">{selectedReview.house_address}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Оценка</p>
                    <p className="font-medium flex items-center">
                      {selectedReview.rating}
                      <span className="ml-1 text-yellow-500">★</span>
                    </p>
                  </div>
                </div>
                
                <div className="mb-8">
                  <p className="text-sm text-gray-500 mb-2">Текст отзыва</p>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="whitespace-pre-wrap">{selectedReview.review_text}</p>
                  </div>
                </div>
                
                <div className="flex space-x-4">
                  <button
                    onClick={() => handleModerateReview(selectedReview.id, 'approve')}
                    disabled={processingReviews[selectedReview.id]}
                    className={`flex items-center px-4 py-2 rounded ${
                      processingReviews[selectedReview.id]
                        ? 'bg-gray-300 cursor-not-allowed'
                        : 'bg-green-600 hover:bg-green-700 text-white'
                    }`}
                  >
                    {processingReviews[selectedReview.id] ? (
                      <Loader2 className="animate-spin mr-2" size={18} />
                    ) : (
                      <Check className="mr-2" size={18} />
                    )}
                    <span>Одобрить</span>
                  </button>
                  
                  <button
                    onClick={() => handleModerateReview(selectedReview.id, 'reject')}
                    disabled={processingReviews[selectedReview.id]}
                    className={`flex items-center px-4 py-2 rounded ${
                      processingReviews[selectedReview.id]
                        ? 'bg-gray-300 cursor-not-allowed'
                        : 'bg-red-600 hover:bg-red-700 text-white'
                    }`}
                  >
                    {processingReviews[selectedReview.id] ? (
                      <Loader2 className="animate-spin mr-2" size={18} />
                    ) : (
                      <X className="mr-2" size={18} />
                    )}
                    <span>Отклонить</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <div className="text-gray-400 mb-4">
                  <Filter className="h-16 w-16 mx-auto" />
                </div>
                <h3 className="text-lg font-medium text-gray-700 mb-2">
                  Выберите отзыв для модерации
                </h3>
                <p className="text-gray-500">
                  Выберите отзыв из списка слева, чтобы просмотреть детали и выполнить действия модерации
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminModeration;