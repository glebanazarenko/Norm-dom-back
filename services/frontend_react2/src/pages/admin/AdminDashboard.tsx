import React, { useState } from 'react';
import { Download, Upload, RefreshCw, Loader2 } from 'lucide-react';
import { downloadData, uploadData, updateHouses } from '../../api/admin';
import { toast } from 'react-toastify';

const AdminDashboard: React.FC = () => {
  const [isDownloading, setIsDownloading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleDownloadData = async () => {
    setIsDownloading(true);
    try {
      await downloadData();
      toast.success('Данные успешно загружены');
    } catch (error) {
      console.error('Error downloading data:', error);
      toast.error('Ошибка при загрузке данных');
    } finally {
      setIsDownloading(false);
    }
  };

  const handleUploadData = async () => {
    setIsUploading(true);
    try {
      await uploadData();
      toast.success('Данные успешно выгружены в базу данных');
    } catch (error) {
      console.error('Error uploading data:', error);
      toast.error('Ошибка при выгрузке данных в базу данных');
    } finally {
      setIsUploading(false);
    }
  };

  const handleUpdateHouses = async () => {
    setIsUpdating(true);
    try {
      await updateHouses();
      toast.success('Данные о домах успешно обновлены');
    } catch (error) {
      console.error('Error updating houses:', error);
      toast.error('Ошибка при обновлении данных о домах');
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Панель администратора</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <Download className="h-5 w-5 text-blue-500 mr-2" />
            Загрузка данных
          </h2>
          <p className="text-gray-600 mb-4">
            Загрузка актуальных данных из открытых источников Москвы
          </p>
          <button
            onClick={handleDownloadData}
            disabled={isDownloading}
            className={`w-full py-2 px-4 rounded-md flex items-center justify-center ${
              isDownloading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            {isDownloading ? (
              <>
                <Loader2 className="animate-spin mr-2" size={18} />
                <span>Загрузка...</span>
              </>
            ) : (
              <>
                <Download className="mr-2" size={18} />
                <span>Загрузить данные</span>
              </>
            )}
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <Upload className="h-5 w-5 text-green-500 mr-2" />
            Выгрузка данных в БД
          </h2>
          <p className="text-gray-600 mb-4">
            Выгрузка загруженных данных в базу данных системы
          </p>
          <button
            onClick={handleUploadData}
            disabled={isUploading}
            className={`w-full py-2 px-4 rounded-md flex items-center justify-center ${
              isUploading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700 text-white'
            }`}
          >
            {isUploading ? (
              <>
                <Loader2 className="animate-spin mr-2" size={18} />
                <span>Выгрузка...</span>
              </>
            ) : (
              <>
                <Upload className="mr-2" size={18} />
                <span>Выгрузить в БД</span>
              </>
            )}
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <RefreshCw className="h-5 w-5 text-purple-500 mr-2" />
            Обновление данных
          </h2>
          <p className="text-gray-600 mb-4">
            Обновление существующих данных о домах в системе
          </p>
          <button
            onClick={handleUpdateHouses}
            disabled={isUpdating}
            className={`w-full py-2 px-4 rounded-md flex items-center justify-center ${
              isUpdating
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-purple-600 hover:bg-purple-700 text-white'
            }`}
          >
            {isUpdating ? (
              <>
                <Loader2 className="animate-spin mr-2" size={18} />
                <span>Обновление...</span>
              </>
            ) : (
              <>
                <RefreshCw className="mr-2" size={18} />
                <span>Обновить данные</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">Системная информация</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-500">Последнее обновление данных</p>
            <p className="font-medium">15.05.2025 12:34</p>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-500">Количество домов в системе</p>
            <p className="font-medium">15,487</p>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-500">Количество пользователей</p>
            <p className="font-medium">823</p>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-500">Всего отзывов</p>
            <p className="font-medium">3,254</p>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-500">Отзывов на модерации</p>
            <p className="font-medium">12</p>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-500">Средний рейтинг домов</p>
            <p className="font-medium">3.7 / 5</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;