import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Clock, Star, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import ReviewCard from '../components/houses/ReviewCard';
import axios from 'axios';

const ProfilePage: React.FC = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [userReviews, setUserReviews] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate('/login');
    }
  }, [authLoading, isAuthenticated, navigate]);

  // Fetch user reviews
  useEffect(() => {
    const fetchUserReviews = async () => {
      if (!user) return;

      setIsLoading(true);
      try {
        // This is a mock endpoint - you'll need to create this endpoint on your backend
        const response = await axios.get(`/users/${user.id}/reviews`);
        setUserReviews(response.data);
      } catch (error) {
        console.error('Error fetching user reviews:', error);
        setError('Не удалось загрузить ваши отзывы. Пожалуйста, попробуйте позже.');
        // For demo purposes, we'll use empty array
        setUserReviews([]);
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      fetchUserReviews();
    }
  }, [user]);

  const handleEditSuccess = () => {
    // Refresh reviews after edit
    // For a real implementation, you would call fetchUserReviews() here
  };

  // Loading state
  if (authLoading || (!user && isAuthenticated)) {
    return (
      <div className="flex justify-center items-center py-20">
        <Loader2 className="animate-spin text-blue-500 h-10 w-10" />
        <span className="ml-3 text-lg text-gray-600">Загрузка профиля...</span>
      </div>
    );
  }

  // Not authenticated
  if (!isAuthenticated) {
    return null; // Will redirect to login
  }

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Личный кабинет</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex flex-col items-center mb-6">
            <div className="bg-blue-100 p-4 rounded-full mb-4">
              <User className="h-14 w-14 text-blue-600" />
            </div>
            <h2 className="text-xl font-semibold">{user?.full_name}</h2>
            <p className="text-gray-600">{user?.username}</p>
            {user?.email && (
              <p className="text-gray-500 text-sm mt-1">{user.email}</p>
            )}
          </div>

          <div className="border-t pt-4">
            <div className="flex items-center text-gray-700 mb-3">
              <Clock className="h-5 w-5 mr-2 text-gray-500" />
              <div>
                <span className="text-sm text-gray-500 block">В системе с</span>
                <span>
                  {new Date(user?.created_at || Date.now()).toLocaleDateString('ru-RU')}
                </span>
              </div>
            </div>

            <div className="flex items-center text-gray-700">
              <Star className="h-5 w-5 mr-2 text-gray-500" />
              <div>
                <span className="text-sm text-gray-500 block">Роль пользователя</span>
                <span>
                  {user?.role_name === 'Admin'
                    ? 'Администратор'
                    : user?.role_name === 'Super User'
                    ? 'Привилегированный пользователь'
                    : 'Пользователь'}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Мои отзывы</h2>

            {isLoading ? (
              <div className="flex justify-center items-center py-10">
                <Loader2 className="animate-spin text-blue-500 h-8 w-8" />
                <span className="ml-3 text-gray-600">Загрузка отзывов...</span>
              </div>
            ) : error ? (
              <div className="text-center py-6 text-red-500">{error}</div>
            ) : userReviews.length > 0 ? (
              <div className="space-y-4">
                {userReviews.map((review) => (
                  <ReviewCard
                    key={review.id}
                    review={review}
                    canEdit={user?.role_name === 'Super User'}
                    onEditSuccess={handleEditSuccess}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 bg-gray-50 rounded-lg">
                <p className="text-gray-600">У вас пока нет отзывов</p>
                <p className="text-sm text-gray-500 mt-1">
                  Найдите дом и оставьте свой первый отзыв!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;