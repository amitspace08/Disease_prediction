import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Shield, Brain, Database } from 'lucide-react';

const Home = () => {
  return (
    <div className="bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center">
        <Activity className="h-16 w-16 text-blue-600 mx-auto mb-6" />
        <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
          <span className="block">Explainable AI-Based</span>
          <span className="block text-blue-600">Multi-Disease Prediction</span>
        </h1>
        <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
          An advanced healthcare decision support system powered by Machine Learning. Get risk predictions for Diabetes, Heart Disease, Liver Disease, and Kidney Disease with full SHAP-based transparency.
        </p>
        <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
          <div className="rounded-md shadow">
            <Link to="/register" className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10">
              Get Started
            </Link>
          </div>
          <div className="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
            <Link to="/login" className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10">
              Log In
            </Link>
          </div>
        </div>
      </div>

      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <Brain className="h-10 w-10 text-blue-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900">Explainable AI</h3>
              <p className="mt-2 text-gray-500 text-sm">Every prediction comes with SHAP feature contributions so you understand exactly why the model made its decision.</p>
            </div>
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <Shield className="h-10 w-10 text-blue-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900">Secure & Private</h3>
              <p className="mt-2 text-gray-500 text-sm">Industry standard JWT authentication and bcrypt password hashing to keep your data safe.</p>
            </div>
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <Database className="h-10 w-10 text-blue-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900">Robust Models</h3>
              <p className="mt-2 text-gray-500 text-sm">Trained using Scikit-learn and XGBoost, with comprehensive validation against data leakage.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
