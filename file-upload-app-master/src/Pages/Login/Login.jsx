import React, { useState } from 'react';
import './Login.css';
import Header from '../../Components/Header/Header';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // 로그인 처리 로직을 여기에 추가.
  };

  return (
      <div className="login-container">
        <h2 className='login-container_title'>Welcome to Partner</h2>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-container_input-group">
            <label>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="login-container_input-group">
            <label>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <button type="submit" className="login-container_btn-signin">Sign in</button>
          <div className="login-container_forgot-password">
            <a href="/forgot-password">Forgot your Password?</a>
          </div>
        </form>
      </div>
  );
}

export default Login;