import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import axios

const AttendancePage = () => {
    const navigate = useNavigate();
    const [selectedClass, setSelectedClass] = useState('');
    const [period, setPeriod] = useState('');
    const [photo, setPhoto] = useState(null);
    const [email,setEmail] = useState('ajmilashada@gmail.com')

    const handleClassChange = (e) => {
        setSelectedClass(e.target.value);
    };

    const handlePeriodChange = (e) => {
        setPeriod(e.target.value);
    };

    const handlePhotoUpload = (e) => {
        setPhoto(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('video', photo);
        formData.append('class_name', selectedClass);
        formData.append('period', period);
        formData.append('email',email);

        try {
            const response = await axios.post('http://localhost:8000/process_video/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            console.log('Response:', response);

            // Check if response is OK
            if (response.status === 200) {
                console.log('Video processed successfully:', response.data);
            } else {
                // If response is not OK, log the error message
                console.error('Video processing failed:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleHomeRedirect = () => {
        navigate('/dashboard');
    };

 return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="absolute top-0 right-0 m-4">
        <button
          onClick={handleHomeRedirect}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Home
        </button>
      </div>
      <div className="max-w-md w-full space-y-8">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">
          Take Attendance
        </h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="class" className="block text-sm font-medium text-gray-700">
              Class
            </label>
            <select
              id="class"
              name="class"
              value={selectedClass}
              onChange={handleClassChange}
              className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              <option value="">Select a class</option>
              <option value="cse_2k20">cse_2k20</option>
              <option value="me2k20">ME 2K20</option>
              <option value="eca2k20">ECA 2K20</option>
              <option value="ce2k20">CE 2K20</option>
              <option value="cse2k21">CSE 2K21</option>
            </select>
          </div>
          <div>
            <label htmlFor="period" className="block text-sm font-medium text-gray-700">
              Period
            </label>
            <input
              type="text"
              name="period"
              id="period"
              value={period}
              onChange={handlePeriodChange}
              className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <div>
            <label htmlFor="photo" className="block text-sm font-medium text-gray-700">
              Upload Video
            </label>
            <input
              type="file"
              name="photo"
              id="photo"
              onChange={handlePhotoUpload}
              className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
 );
};

export default AttendancePage;
