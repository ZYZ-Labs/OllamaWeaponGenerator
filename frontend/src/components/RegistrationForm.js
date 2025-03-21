import React, { useState } from 'react';

function RegistrationForm({ onRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });
    if (response.ok) {
      const data = await response.json();
      onRegister(data.access_token);
    } else {
      alert('注册失败，请检查输入或该用户名是否已存在');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto">
      <h2 className="text-2xl mb-4">注册</h2>
      <input 
        type="text" 
        placeholder="用户名" 
        value={username} 
        onChange={(e) => setUsername(e.target.value)}
        className="border p-2 mb-4 w-full"
      />
      <input 
        type="password" 
        placeholder="密码" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)}
        className="border p-2 mb-4 w-full"
      />
      <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
        注册
      </button>
    </form>
  );
}

export default RegistrationForm;
