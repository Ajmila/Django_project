// src/components/ClassDetails.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const ClassDetails = () => {
  const { class_name } = useParams();
  const [classDetails, setClassDetails] = useState(null);

  useEffect(() => {
    // Fetch class details based on the class_name parameter
    const fetchClassDetails = async () => {
      try {
        const response = await fetch(`http://localhost:8000/view_class/?class_name=${class_name}`);
        if (response.ok) {
          const data = await response.json();
          setClassDetails(data);
        } else {
          throw new Error('Failed to fetch class details');
        }
      } catch (error) {
        console.error('Error fetching class details:', error);
      }
    };

    fetchClassDetails();
  }, [class_name]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <h2 className="text-center text-3xl font-extrabold text-gray-900">Class Details</h2>
      {classDetails ? (
        <div className="mt-4">
          <h3 className="text-lg font-bold">{classDetails.class}</h3>
          <p>Period: {classDetails.period}</p>
          <p>Present Students: {classDetails.present.join(', ')}</p>
          <p>Absent Students: {classDetails.absent.join(', ')}</p>
        </div>
      ) : (
        <p>Loading class details...</p>
      )}
    </div>
  );
};

export default ClassDetails;
