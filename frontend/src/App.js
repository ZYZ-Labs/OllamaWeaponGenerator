import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';
import WeaponGenerator from './components/WeaponGenerator';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = (token) => {
    setToken(token);
    localStorage.setItem('token', token);
  };

  const toggleRegister = () => {
    setShowRegister(!showRegister);
  };

  return (
    <div className="container mx-auto p-4">
      {!token ? (
        showRegister ? (
          <div>
            <RegistrationForm onRegister={handleLogin} />
            <p className="mt-2 text-center">
              已有帐号？{' '}
              <button onClick={toggleRegister} className="text-blue-500">
                去登录
              </button>
            </p>
          </div>
        ) : (
          <div>
            <LoginForm onLogin={handleLogin} />
            <p className="mt-2 text-center">
              没有帐号？{' '}
              <button onClick={toggleRegister} className="text-blue-500">
                去注册
              </button>
            </p>
          </div>
        )
      ) : (
        <WeaponGenerator token={token} />
      )}
    </div>
  );
}

export default App;
