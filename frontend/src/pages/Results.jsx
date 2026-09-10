import React from 'react';
import { useLocation, Link, Navigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const Results = () => {
  const location = useLocation();
  const { result, disease } = location.state || {};

  if (!result) {
    return <Navigate to="/dashboard" />;
  }

  const { prediction, probability, risk_level, explanation, model_version } = result;

  const getRiskColor = (level) => {
    if (level === 'High') return 'text-red-600';
    if (level === 'Moderate') return 'text-yellow-600';
    return 'text-green-600';
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="bg-blue-600 px-6 py-4">
          <h2 className="text-2xl font-bold text-white capitalize">{disease} Risk Prediction</h2>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-center">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-500 font-medium mb-1">Prediction</p>
              <p className={`text-2xl font-bold ${getRiskColor(risk_level)}`}>{prediction}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-500 font-medium mb-1">Probability</p>
              <p className="text-2xl font-bold text-gray-900">{(probability * 100).toFixed(1)}%</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-500 font-medium mb-1">Model Used</p>
              <p className="text-lg font-bold text-gray-900">{model_version}</p>
            </div>
          </div>

          {explanation && explanation.length > 0 && (
            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Why did the model predict this?</h3>
              <p className="text-sm text-gray-600 mb-4">
                The chart below shows the top features contributing to the model's prediction. 
                Positive values push the prediction towards higher risk, while negative values push it lower.
              </p>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={explanation}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <XAxis type="number" />
                    <YAxis dataKey="feature" type="category" width={150} />
                    <Tooltip formatter={(val) => val.toFixed(4)} />
                    <Bar dataKey="contribution" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
            <p className="text-sm text-yellow-700">
              <strong>Disclaimer:</strong> This system is intended for educational and decision-support purposes only and is not a substitute for professional medical diagnosis or treatment. The SHAP explanations describe the model's mathematical behavior, not necessarily a clinical causal relationship.
            </p>
          </div>

          <div className="text-center">
            <Link
              to="/dashboard"
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Return to Dashboard
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
