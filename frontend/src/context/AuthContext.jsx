import React, { createContext, useState, useEffect } from 'react';
import { getCurrentUser, login, logout, register } from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        const userData = await getCurrentUser();
        setUser(userData);
      }
      setLoading(false);
    };

    fetchUser();
  }, []);

  const handleLogin = async (email, password) => {
    await login(email, password);
    const userData = await getCurrentUser();
    setUser(userData);
  };

  const handleRegister = async (name, email, password) => {
    await register(name, email, password);
    const userData = await getCurrentUser();
    setUser(userData);
  };

  const handleLogout = () => {
    logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, handleLogin, handleRegister, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};
