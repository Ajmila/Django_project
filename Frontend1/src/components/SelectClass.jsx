// src/components/SelectClass.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SelectClass = () => {
 const navigate = useNavigate();
 const [selectedClass, setSelectedClass] = useState('');

 const handleClassChange = (e) => {
    setSelectedClass(e.target.value);
 };

 const handleSubmit = async () => {
    try {
        const response = await fetch('http://localhost:8000/view_class/', {
            method: 'POST',
            headers: {
                'Content-Type': 'json'
            },
            body: JSON.stringify({ class_name: selectedClass })
        });
        if (response.ok) {
            // If the request is successful, navigate to the class details page
            navigate(`/class?class_name=${selectedClass}`);
        } else {
            throw new Error('Failed to submit class selection');
        }
    } catch (error) {
        console.error('Error submitting class selection:', error);
    }
 };

 return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <h2 className="text-center text-3xl font-extrabold text-gray-900">
        Select Class
      </h2>
      <select
        value={selectedClass}
        onChange={handleClassChange}
        className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      >
        <option value="">Select a class</option>
        <option value="cse_2k20">CSE 2K20</option>
        <option value="me2k20">ME 2K20</option>
        <option value="eca2k20">ECA 2K20</option>
        <option value="ce2k20">CE 2K20</option>
        <option value="cse2k21">CSE 2K21</option>
      </select>
      <button
        onClick={handleSubmit}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Submit
      </button>
    </div>
 );
};

export default SelectClass;
