import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { predictDisease } from '../services/predictionService';

const diseaseForms = {
  diabetes: [
    { name: 'preg', label: 'Pregnancies', type: 'number' },
    { name: 'plas', label: 'Glucose', type: 'number' },
    { name: 'pres', label: 'Blood Pressure', type: 'number' },
    { name: 'skin', label: 'Skin Thickness', type: 'number' },
    { name: 'insu', label: 'Insulin', type: 'number' },
    { name: 'mass', label: 'BMI', type: 'number', step: '0.1' },
    { name: 'pedi', label: 'Diabetes Pedigree Function', type: 'number', step: '0.001' },
    { name: 'age', label: 'Age', type: 'number' }
  ],
  heart: [
    { name: 'age', label: 'Age', type: 'number' },
    { name: 'sex', label: 'Sex (1=Male, 0=Female)', type: 'number' },
    { name: 'cp', label: 'Chest Pain Type (1-4)', type: 'number' },
    { name: 'trestbps', label: 'Resting Blood Pressure', type: 'number' },
    { name: 'chol', label: 'Cholesterol', type: 'number' },
    { name: 'fbs', label: 'Fasting Blood Sugar > 120 (1=True, 0=False)', type: 'number' },
    { name: 'restecg', label: 'Resting ECG', type: 'number' },
    { name: 'thalach', label: 'Max Heart Rate', type: 'number' },
    { name: 'exang', label: 'Exercise Induced Angina (1=Yes, 0=No)', type: 'number' },
    { name: 'oldpeak', label: 'ST Depression', type: 'number', step: '0.1' },
    { name: 'slope', label: 'Slope of peak exercise ST', type: 'number' },
    { name: 'ca', label: 'Number of major vessels (0-3)', type: 'number' },
    { name: 'thal', label: 'Thal (3=normal, 6=fixed, 7=reversable)', type: 'number' }
  ],
  liver: [
    { name: 'Age', label: 'Age', type: 'number' },
    { name: 'Gender', label: 'Gender (Male/Female)', type: 'text' },
    { name: 'TB', label: 'Total Bilirubin', type: 'number', step: '0.1' },
    { name: 'DB', label: 'Direct Bilirubin', type: 'number', step: '0.1' },
    { name: 'Alkphos', label: 'Alkaline Phosphotase', type: 'number' },
    { name: 'Sgpt', label: 'Alamine Aminotransferase', type: 'number' },
    { name: 'Sgot', label: 'Aspartate Aminotransferase', type: 'number' },
    { name: 'TP', label: 'Total Proteins', type: 'number', step: '0.1' },
    { name: 'ALB', label: 'Albumin', type: 'number', step: '0.1' },
    { name: 'A/G Ratio', label: 'Albumin and Globulin Ratio', type: 'number', step: '0.01' }
  ],
  kidney: [
    { name: 'age', label: 'Age', type: 'number' },
    { name: 'bp', label: 'Blood Pressure', type: 'number' },
    { name: 'sg', label: 'Specific Gravity', type: 'number', step: '0.001' },
    { name: 'al', label: 'Albumin', type: 'number' },
    { name: 'su', label: 'Sugar', type: 'number' },
    { name: 'rbc', label: 'Red Blood Cells (normal/abnormal)', type: 'text' },
    { name: 'pc', label: 'Pus Cell (normal/abnormal)', type: 'text' },
    { name: 'pcc', label: 'Pus Cell clumps (present/notpresent)', type: 'text' },
    { name: 'ba', label: 'Bacteria (present/notpresent)', type: 'text' },
    { name: 'bgr', label: 'Blood Glucose Random', type: 'number' },
    { name: 'bu', label: 'Blood Urea', type: 'number' },
    { name: 'sc', label: 'Serum Creatinine', type: 'number', step: '0.1' },
    { name: 'sod', label: 'Sodium', type: 'number' },
    { name: 'pot', label: 'Potassium', type: 'number', step: '0.1' },
    { name: 'hemo', label: 'Hemoglobin', type: 'number', step: '0.1' },
    { name: 'pcv', label: 'Packed Cell Volume', type: 'number' },
    { name: 'wbcc', label: 'White Blood Cell Count', type: 'number' },
    { name: 'rbcc', label: 'Red Blood Cell Count', type: 'number', step: '0.1' },
    { name: 'htn', label: 'Hypertension (yes/no)', type: 'text' },
    { name: 'dm', label: 'Diabetes Mellitus (yes/no)', type: 'text' },
    { name: 'cad', label: 'Coronary Artery Disease (yes/no)', type: 'text' },
    { name: 'appet', label: 'Appetite (good/poor)', type: 'text' },
    { name: 'pe', label: 'Pedal Edema (yes/no)', type: 'text' },
    { name: 'ane', label: 'Anemia (yes/no)', type: 'text' }
  ]
};

const Prediction = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fields = diseaseForms[id];

  if (!fields) {
    return <div className="text-center mt-10">Invalid disease selected</div>;
  }

  const handleChange = (e) => {
    let value = e.target.value;
    if (e.target.type === 'number') {
      value = value === '' ? '' : Number(value);
    }
    setFormData({ ...formData, [e.target.name]: value });
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await predictDisease(id, formData);
      navigate('/results', { state: { result, disease: id } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-6 capitalize text-center">{id} Disease Prediction</h2>
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
        <form onSubmit={onSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {fields.map((field) => (
            <div key={field.name}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
              <input
                type={field.type}
                name={field.name}
                step={field.step}
                required
                className="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                onChange={handleChange}
              />
            </div>
          ))}
          <div className="col-span-1 md:col-span-2 text-center mt-6">
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-8 py-3 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Processing...' : 'Get Prediction'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Prediction;
