// src/components/SignupPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignupPage = () => {
 const [signupSuccess, setSignupSuccess] = useState(false);
 const [formData, setFormData] = useState({
   username: '',
   email: '',
   password: '',
   confirmPassword: '',
 });
 const navigate = useNavigate();

 const handleInputChange = (e) => {
   setFormData({
     ...formData,
     [e.target.name]: e.target.value,
   });
 };

 const handleSignup = (e) => {
   e.preventDefault();
   // Basic validation
   if (formData.password !== formData.confirmPassword) {
     alert('Passwords do not match');
     return;
   }
   // Simulate signup logic here
   // If signup is successful, set signupSuccess to true
   setSignupSuccess(true);
 };

 const handleLoginRedirect = () => {
   navigate('/');
 };

 return (
   <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
     <div className="max-w-md w-full space-y-8">
       {signupSuccess ? (
         <div className="bg-white p-4 rounded shadow">
           <p className="text-center text-lg font-bold">Account successfully created!</p>
           <button
             onClick={handleLoginRedirect}
             className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
           >
             Login
           </button>
         </div>
       ) : (
         <>
           <div>
             <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
               Create your account
             </h2>
           </div>
           <form className="mt-8 space-y-6" onSubmit={handleSignup}>
             <input
               type="text"
               name="username"
               value={formData.username}
               onChange={handleInputChange}
               className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
               placeholder="Username"
               required
             />
             <input
               type="email"
               name="email"
               value={formData.email}
               onChange={handleInputChange}
               className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
               placeholder="Email"
               required
             />
             <input
               type="password"
               name="password"
               value={formData.password}
               onChange={handleInputChange}
               className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
               placeholder="Password"
               required
             />
             <input
               type="password"
               name="confirmPassword"
               value={formData.confirmPassword}
               onChange={handleInputChange}
               className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
               placeholder="Confirm Password"
               required
             />
             <div>
               <button
                 type="submit"
                 className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
               >
                 Sign up
               </button>
             </div>
           </form>
         </>
       )}
     </div>
   </div>
 );
};

export default SignupPage;
