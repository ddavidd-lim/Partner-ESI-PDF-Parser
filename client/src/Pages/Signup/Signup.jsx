import React, { useState } from 'react';
import './Signup.css';

function Signup() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const { firstName, lastName, gender, email, password, confirmPassword } = formData;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // 회원가입 처리 로직
  };

  return (
    <div className="signup-container">
      <h2>Register to Join Us</h2>
      <form className="signup-form" onSubmit={handleSubmit}>
        <div className="input-row">
          <input 
            type="text" 
            placeholder="First Name"
            name="firstName"
            value={firstName}
            onChange={handleChange}
          />
          <input 
            type="text" 
            placeholder="Last Name"
            name="lastName"
            value={lastName}
            onChange={handleChange}
          />
        </div>
        <input 
          type="text" 
          placeholder="Gender"
          name="gender"
          value={gender}
          onChange={handleChange}
        />
        <input 
          type="email" 
          placeholder="Email"
          name="email"
          value={email}
          onChange={handleChange}
        />
        <input 
          type="password" 
          placeholder="Password"
          name="password"
          value={password}
          onChange={handleChange}
        />
        <input 
          type="password" 
          placeholder="Confirm Password"
          name="confirmPassword"
          value={confirmPassword}
          onChange={handleChange}
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup;