import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

// Set up axios defaults
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'https://localhost:5001/';

// Types
interface User {
  id: string;
  username: string;
  full_name: string;
  email?: string;
  role_name: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is authenticated
  const checkAuth = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('/users/getuser');
      setUser(response.data);
    } catch (error) {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Login function
  const login = useCallback(async (username: string, password: string) => {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      
      await axios.post('/login', formData);
      await checkAuth();
      toast.success('Вы успешно вошли в систему!');
    } catch (error) {
      toast.error('Ошибка при входе. Проверьте логин и пароль.');
      throw error;
    }
  }, [checkAuth]);

  // Register function
  const register = useCallback(async (userData: any) => {
    try {
      await axios.post('/register', userData);
      toast.success('Регистрация успешна! Теперь вы можете войти в систему.');
    } catch (error) {
      toast.error('Ошибка при регистрации. Пожалуйста, попробуйте снова.');
      throw error;
    }
  }, []);

  // Logout function
  const logout = useCallback(() => {
    // Clear the cookie by setting an expired cookie
    document.cookie = "Authorization=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; secure; samesite=none";
    setUser(null);
    toast.info('Вы вышли из системы');
  }, []);

  // Memoize the context value
  const value = useMemo(() => ({
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    checkAuth
  }), [user, isLoading, login, register, logout, checkAuth]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};