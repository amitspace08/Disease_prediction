import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import { Activity, Heart, TestTube, FileText } from 'lucide-react';

const Dashboard = () => {
  const { user } = useContext(AuthContext);

  const diseases = [
    { id: 'diabetes', name: 'Diabetes', icon: Activity, desc: 'Analyze glucose and BMI to assess risk.', color: 'text-blue-500' },
    { id: 'heart', name: 'Heart Disease', icon: Heart, desc: 'Predict cardiovascular risks based on vitals.', color: 'text-red-500' },
    { id: 'liver', name: 'Liver Disease', icon: TestTube, desc: 'Evaluate enzymes and bilirubin levels.', color: 'text-yellow-500' },
    { id: 'kidney', name: 'Kidney Disease', icon: FileText, desc: 'Assess blood pressure and specific gravity.', color: 'text-purple-500' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Welcome, {user?.name}</h1>
      <p className="text-gray-600 mb-8">
        This system is intended for educational and decision-support purposes only and is not a substitute for professional medical diagnosis or treatment.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {diseases.map((d) => {
          const Icon = d.icon;
          return (
            <div key={d.id} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition duration-200">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-gray-50 mx-auto mb-4">
                <Icon className={`h-8 w-8 ${d.color}`} />
              </div>
              <h3 className="text-lg font-medium text-gray-900 text-center mb-2">{d.name}</h3>
              <p className="text-sm text-gray-500 text-center mb-4">{d.desc}</p>
              <div className="text-center">
                <Link
                  to={`/predict/${d.id}`}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Start Prediction
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Dashboard;
