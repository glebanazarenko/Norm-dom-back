import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Users, Database } from 'lucide-react';

const AdminSidebar: React.FC = () => {
  const activeClassName = "bg-blue-700 text-white";
  const inactiveClassName = "text-gray-300 hover:bg-gray-700 hover:text-white transition-colors";
  
  const sidebarItems = [
    { to: '/admin', text: 'Главная', icon: <LayoutDashboard size={20} />, end: true },
    { to: '/admin/moderation', text: 'Модерация', icon: <MessageSquare size={20} /> },
    { to: '/admin/users', text: 'Пользователи', icon: <Users size={20} /> }
  ];

  return (
    <aside className="w-64 bg-gray-800 text-white">
      <nav className="p-4">
        <div className="py-2 px-4 text-xs uppercase text-gray-400 font-semibold">
          Управление
        </div>
        <ul className="space-y-2">
          {sidebarItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                end={item.end}
                className={({ isActive }) => 
                  `flex items-center space-x-3 px-4 py-3 rounded-md ${
                    isActive ? activeClassName : inactiveClassName
                  }`
                }
              >
                {item.icon}
                <span>{item.text}</span>
              </NavLink>
            </li>
          ))}
        </ul>
        
        <div className="mt-8 py-2 px-4 text-xs uppercase text-gray-400 font-semibold">
          Данные
        </div>
        <div className="mt-4 px-4 py-4 bg-gray-700 rounded-md">
          <div className="flex items-center space-x-2 mb-4">
            <Database size={18} />
            <span className="font-semibold">Обновление данных</span>
          </div>
          <div className="space-y-2">
            <button className="w-full text-left px-3 py-2 text-sm bg-blue-600 hover:bg-blue-700 rounded transition-colors">
              Загрузить данные
            </button>
            <button className="w-full text-left px-3 py-2 text-sm bg-green-600 hover:bg-green-700 rounded transition-colors">
              Выгрузить данные в БД
            </button>
            <button className="w-full text-left px-3 py-2 text-sm bg-purple-600 hover:bg-purple-700 rounded transition-colors">
              Обновить данные о домах
            </button>
          </div>
        </div>
      </nav>
    </aside>
  );
};

export default AdminSidebar;