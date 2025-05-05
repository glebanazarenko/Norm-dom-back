import React, { useState, useEffect } from 'react';
import { Search, UserX, Shield, UserCheck, Loader2, Filter } from 'lucide-react';
import { toast } from 'react-toastify';
import axios from 'axios';

interface User {
  id: string;
  username: string;
  full_name: string;
  email: string;
  role_name: string;
  created_at: string;
  reviews_count?: number;
  is_blocked?: boolean;
}

const AdminUsers: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  
  // For filtering
  const [roleFilter, setRoleFilter] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<boolean | null>(null);

  // Fetch users
  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoading(true);
      try {
        // This is a mock endpoint - you'll need to create this endpoint on your backend
        const response = await axios.get('/admin/users');
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
        setError('Не удалось загрузить список пользователей');
        // For demo purposes, we'll use mock data
        setUsers([
          {
            id: '1',
            username: 'ivan',
            full_name: 'Иван Иванов',
            email: 'ivan@example.com',
            role_name: 'User',
            created_at: '2025-01-15T10:30:00Z',
            reviews_count: 5,
            is_blocked: false
          },
          {
            id: '2',
            username: 'maria',
            full_name: 'Мария Петрова',
            email: 'maria@example.com',
            role_name: 'Super User',
            created_at: '2025-02-20T15:20:00Z',
            reviews_count: 12,
            is_blocked: false
          },
          {
            id: '3',
            username: 'Сергей_123',
            full_name: 'Сергей Спамов',
            email: 'sergey@spam.com',
            role_name: 'User',
            created_at: '2025-03-13T09:15:00Z',
            reviews_count: 1,
            is_blocked: true
          },
          {
            id: '4',
            username: 'Admin',
            full_name: 'Администратор',
            email: 'Admin@normdom.ru',
            role_name: 'Admin',
            created_at: '2025-01-01T00:00:00Z',
            reviews_count: 0,
            is_blocked: false
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUsers();
  }, []);

  // Handle user selection
  const handleSelectUser = (user: User) => {
    setSelectedUser(user);
  };

  // Handle blocking/unblocking user
  const handleToggleBlockUser = async () => {
    if (!selectedUser) return;
    
    setIsProcessing(true);
    
    try {
      // This is a mock endpoint - you'll need to create this endpoint on your backend
      await axios.post(`/admin/users/${selectedUser.id}/${selectedUser.is_blocked ? 'unblock' : 'block'}`);
      
      // Update the user in the list
      const updatedUsers = users.map(user => {
        if (user.id === selectedUser.id) {
          return { ...user, is_blocked: !user.is_blocked };
        }
        return user;
      });
      
      setUsers(updatedUsers);
      
      // Update the selected user
      setSelectedUser({ ...selectedUser, is_blocked: !selectedUser.is_blocked });
      
      toast.success(`Пользователь успешно ${selectedUser.is_blocked ? 'разблокирован' : 'заблокирован'}`);
    } catch (error) {
      console.error('Error toggling user block status:', error);
      toast.error(`Ошибка при ${selectedUser.is_blocked ? 'разблокировке' : 'блокировке'} пользователя`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Handle role change
  const handleChangeRole = async (newRole: string) => {
    if (!selectedUser) return;
    
    setIsProcessing(true);
    
    try {
      // This is a mock endpoint - you'll need to create this endpoint on your backend
      await axios.post(`/admin/users/${selectedUser.id}/role`, { role: newRole });
      
      // Update the user in the list
      const updatedUsers = users.map(user => {
        if (user.id === selectedUser.id) {
          return { ...user, role_name: newRole };
        }
        return user;
      });
      
      setUsers(updatedUsers);
      
      // Update the selected user
      setSelectedUser({ ...selectedUser, role_name: newRole });
      
      toast.success(`Роль пользователя успешно изменена на ${getRoleName(newRole)}`);
    } catch (error) {
      console.error('Error changing user role:', error);
      toast.error('Ошибка при изменении роли пользователя');
    } finally {
      setIsProcessing(false);
    }
  };

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  // Get role name in Russian
  const getRoleName = (role: string) => {
    switch (role) {
      case 'Admin':
        return 'Администратор';
      case 'Super User':
        return 'Привилегированный пользователь';
      case 'User':
        return 'Обычный пользователь';
      default:
        return role;
    }
  };

  // Apply filters and search
  const getFilteredUsers = () => {
    return users.filter(user => {
      // Apply search
      const matchesSearch = !searchQuery || 
        user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.full_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.email.toLowerCase().includes(searchQuery.toLowerCase());
      
      // Apply role filter
      const matchesRole = roleFilter === null || user.role_name === roleFilter;
      
      // Apply status filter
      const matchesStatus = statusFilter === null || user.is_blocked === statusFilter;
      
      return matchesSearch && matchesRole && matchesStatus;
    });
  };

  const filteredUsers = getFilteredUsers();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Управление пользователями</h1>

      <div className="flex mb-6">
        <div className="relative flex-grow">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Поиск пользователей..."
            className="w-full p-3 pl-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center py-20">
          <Loader2 className="animate-spin text-blue-500 h-10 w-10" />
          <span className="ml-3 text-lg text-gray-600">Загрузка пользователей...</span>
        </div>
      ) : error ? (
        <div className="text-center py-10 bg-red-50 text-red-600 rounded-lg">
          {error}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1">
            <div className="bg-white rounded-lg shadow-md overflow-hidden mb-4">
              <div className="p-4 bg-gray-50 border-b">
                <h2 className="font-semibold">
                  Пользователи ({filteredUsers.length})
                </h2>
              </div>
              
              <div className="px-4 py-2 border-b flex space-x-2 overflow-x-auto">
                <button
                  onClick={() => setRoleFilter(null)}
                  className={`px-2 py-1 text-xs rounded whitespace-nowrap ${
                    roleFilter === null
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  Все роли
                </button>
                <button
                  onClick={() => setRoleFilter('Admin')}
                  className={`px-2 py-1 text-xs rounded whitespace-nowrap ${
                    roleFilter === 'Admin'
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  Администраторы
                </button>
                <button
                  onClick={() => setRoleFilter('Super User')}
                  className={`px-2 py-1 text-xs rounded whitespace-nowrap ${
                    roleFilter === 'Super User'
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  Привилегированные
                </button>
                <button
                  onClick={() => setRoleFilter('User')}
                  className={`px-2 py-1 text-xs rounded whitespace-nowrap ${
                    roleFilter === 'User'
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  Обычные
                </button>
              </div>
              
              <div className="px-4 py-2 border-b flex space-x-2">
                <button
                  onClick={() => setStatusFilter(null)}
                  className={`px-2 py-1 text-xs rounded ${
                    statusFilter === null
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  Любой статус
                </button>
                <button
                  onClick={() => setStatusFilter(false)}
                  className={`px-2 py-1 text-xs rounded ${
                    statusFilter === false
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  Активные
                </button>
                <button
                  onClick={() => setStatusFilter(true)}
                  className={`px-2 py-1 text-xs rounded ${
                    statusFilter === true
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  Заблокированные
                </button>
              </div>
              
              <div className="overflow-y-auto max-h-[600px]">
                {filteredUsers.length > 0 ? (
                  filteredUsers.map(user => (
                    <div
                      key={user.id}
                      onClick={() => handleSelectUser(user)}
                      className={`p-4 border-b cursor-pointer hover:bg-gray-50 transition-colors ${
                        selectedUser?.id === user.id ? 'bg-blue-50' : ''
                      }`}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <p className="font-medium">{user.username}</p>
                          <p className="text-sm text-gray-600">{user.full_name}</p>
                        </div>
                        {user.is_blocked && (
                          <div className="bg-red-100 text-red-600 text-xs px-2 py-1 rounded">
                            Заблокирован
                          </div>
                        )}
                      </div>
                      <div className="flex justify-between">
                        <p className="text-xs text-gray-500">
                          {getRoleName(user.role_name)}
                        </p>
                        <p className="text-xs text-gray-500">
                          {user.reviews_count !== undefined ? `${user.reviews_count} отзывов` : ''}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="p-4 text-center text-gray-500">
                    Нет пользователей, соответствующих критериям поиска
                  </div>
                )}
              </div>
            </div>
          </div>
          
          <div className="md:col-span-2">
            {selectedUser ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h2 className="text-xl font-semibold">{selectedUser.full_name}</h2>
                    <p className="text-gray-600">{selectedUser.username}</p>
                  </div>
                  
                  <div className={`px-3 py-1 rounded-full text-sm ${
                    selectedUser.is_blocked
                      ? 'bg-red-100 text-red-600'
                      : 'bg-green-100 text-green-600'
                  }`}>
                    {selectedUser.is_blocked ? 'Заблокирован' : 'Активен'}
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Email</p>
                    <p className="font-medium">{selectedUser.email}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Дата регистрации</p>
                    <p className="font-medium">{formatDate(selectedUser.created_at)}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Роль</p>
                    <p className="font-medium">{getRoleName(selectedUser.role_name)}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Отзывы</p>
                    <p className="font-medium">
                      {selectedUser.reviews_count !== undefined ? selectedUser.reviews_count : 'Н/Д'}
                    </p>
                  </div>
                </div>
                
                <div className="mb-8 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium mb-3">Управление пользователем</h3>
                  
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-500 mb-2">Изменить роль</p>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleChangeRole('User')}
                          disabled={isProcessing || selectedUser.role_name === 'User'}
                          className={`px-3 py-1 rounded text-sm ${
                            selectedUser.role_name === 'User'
                              ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                              : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                          }`}
                        >
                          Обычный пользователь
                        </button>
                        
                        <button
                          onClick={() => handleChangeRole('Super User')}
                          disabled={isProcessing || selectedUser.role_name === 'Super User'}
                          className={`px-3 py-1 rounded text-sm ${
                            selectedUser.role_name === 'Super User'
                              ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                              : 'bg-blue-100 hover:bg-blue-200 text-blue-700'
                          }`}
                        >
                          Привилегированный
                        </button>
                        
                        <button
                          onClick={() => handleChangeRole('Admin')}
                          disabled={isProcessing || selectedUser.role_name === 'Admin'}
                          className={`px-3 py-1 rounded text-sm ${
                            selectedUser.role_name === 'Admin'
                              ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                              : 'bg-purple-100 hover:bg-purple-200 text-purple-700'
                          }`}
                        >
                          Администратор
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-sm text-gray-500 mb-2">Статус аккаунта</p>
                      <button
                        onClick={handleToggleBlockUser}
                        disabled={isProcessing}
                        className={`flex items-center px-4 py-2 rounded ${
                          isProcessing
                            ? 'bg-gray-300 cursor-not-allowed'
                            : selectedUser.is_blocked
                            ? 'bg-green-600 hover:bg-green-700 text-white'
                            : 'bg-red-600 hover:bg-red-700 text-white'
                        }`}
                      >
                        {isProcessing ? (
                          <Loader2 className="animate-spin mr-2" size={18} />
                        ) : selectedUser.is_blocked ? (
                          <UserCheck className="mr-2" size={18} />
                        ) : (
                          <UserX className="mr-2" size={18} />
                        )}
                        <span>
                          {selectedUser.is_blocked ? 'Разблокировать пользователя' : 'Заблокировать пользователя'}
                        </span>
                      </button>
                    </div>
                  </div>
                </div>
                
                <div className="border-t pt-4">
                  <button
                    onClick={() => setSelectedUser(null)}
                    className="text-gray-600 hover:text-gray-800"
                  >
                    ← Вернуться к списку пользователей
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <div className="text-gray-400 mb-4">
                  <Shield className="h-16 w-16 mx-auto" />
                </div>
                <h3 className="text-lg font-medium text-gray-700 mb-2">
                  Выберите пользователя
                </h3>
                <p className="text-gray-500">
                  Выберите пользователя из списка слева, чтобы просмотреть детали и выполнить действия администрирования
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUsers;