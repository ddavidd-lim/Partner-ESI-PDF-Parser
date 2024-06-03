import React, { useState } from 'react';
import Login from '../Login/Login';
import Signup from '../Signup/Signup'
import Header from '../../Components/Header/Header';
import './Authpage.css';

function AuthPage() {
  const [activeTab, setActiveTab] = useState('login');

  return (
    <>
        <Header />
        <div className="auth-container">
        <div className="tab">
            <button 
            className={`tablinks ${activeTab === 'login' ? 'active' : ''}`} 
            onClick={() => setActiveTab('login')}
            >
            Login
            </button>
            {/* <button 
            className={`tablinks ${activeTab === 'signup' ? 'active' : ''}`} 
            onClick={() => setActiveTab('signup')}
            >
            Sign up
            </button> */}
        </div>
        {activeTab === 'login' && <Login />}
        {activeTab === 'signup' && <Signup />}
        </div>
    </>
  );
}

export default AuthPage;