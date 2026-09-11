import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { predictDisease } from '../services/predictionService';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  Heart, Activity, Droplet, Stethoscope, Home, Info, HeartHandshake, Contact,
  CheckCircle2, AlertTriangle, ShieldCheck, Sparkles
} from 'lucide-react';

const diseaseConfigs = {
  heart: {
    id: 'heart',
    name: 'Heart Disease Prediction',
    brand: 'HeartCare AI',
    tagline: 'Predict Today For a Healthier Tomorrow',
    subtitle: 'Check your heart health with AI',
    quote: '"A healthy heart leads to a brighter future."',
    accuracy: '92%',
    icon: Heart,
    colorScheme: {
      sidebarBg: 'bg-gradient-to-b from-red-800 via-red-900 to-red-950 text-white',
      sidebarActive: 'bg-red-700/80 text-white shadow-inner',
      headerTitle: 'text-gray-900',
      headerIconBg: 'bg-red-100 text-red-600',
      btnBg: 'bg-red-600 hover:bg-red-700 text-white shadow-lg shadow-red-200',
      badgeSuccess: 'bg-emerald-100 text-emerald-800 border-emerald-300',
      badgeDanger: 'bg-red-100 text-red-800 border-red-300',
      cardBorder: 'border-red-100',
      adviceBg: 'bg-red-50/70 border-red-200',
      bulletColor: 'text-red-600',
      barColor: '#dc2626',
      accentText: 'text-red-600'
    },
    advice: [
      'Maintain a balanced, low-sodium diet',
      'Exercise regularly (at least 30 mins a day)',
      'Keep your blood pressure & cholesterol in check',
      'Do regular cardiovascular health checkups'
    ],
    fields: [
      { name: 'age', label: 'Age', type: 'number', unit: 'years', defaultValue: 45 },
      { name: 'sex', label: 'Sex', type: 'select', options: [{ value: 1, label: 'Male' }, { value: 0, label: 'Female' }], defaultValue: 1 },
      { name: 'cp', label: 'Chest Pain Type', type: 'select', options: [
        { value: 1, label: 'Typical Angina' },
        { value: 2, label: 'Atypical Angina' },
        { value: 3, label: 'Non-anginal Pain' },
        { value: 4, label: 'Asymptomatic' }
      ], defaultValue: 1 },
      { name: 'trestbps', label: 'Resting Blood Pressure', type: 'number', unit: 'mm Hg', defaultValue: 120 },
      { name: 'chol', label: 'Cholesterol', type: 'number', unit: 'mg/dl', defaultValue: 200 },
      { name: 'fbs', label: 'Fasting Blood Sugar > 120', type: 'select', options: [{ value: 1, label: 'True (>120 mg/dl)' }, { value: 0, label: 'False (<=120 mg/dl)' }], defaultValue: 0 },
      { name: 'restecg', label: 'Resting ECG', type: 'select', options: [
        { value: 0, label: 'Normal' },
        { value: 1, label: 'ST-T Wave Abnormality' },
        { value: 2, label: 'Left Ventricular Hypertrophy' }
      ], defaultValue: 0 },
      { name: 'thalach', label: 'Max Heart Rate', type: 'number', unit: 'bpm', defaultValue: 150 },
      { name: 'exang', label: 'Exercise Induced Angina', type: 'select', options: [{ value: 1, label: 'Yes' }, { value: 0, label: 'No' }], defaultValue: 0 },
      { name: 'oldpeak', label: 'ST Depression', type: 'number', step: '0.1', defaultValue: 1.0 },
      { name: 'slope', label: 'Slope of Peak Exercise ST', type: 'select', options: [
        { value: 1, label: 'Upsloping' },
        { value: 2, label: 'Flat' },
        { value: 3, label: 'Downsloping' }
      ], defaultValue: 1 },
      { name: 'ca', label: 'Number of Major Vessels', type: 'number', defaultValue: 0 },
      { name: 'thal', label: 'Thalassemia', type: 'select', options: [
        { value: 3, label: 'Normal' },
        { value: 6, label: 'Fixed Defect' },
        { value: 7, label: 'Reversable Defect' }
      ], defaultValue: 3 }
    ]
  },
  kidney: {
    id: 'kidney',
    name: 'Kidney Disease Prediction',
    brand: 'KidneyCare AI',
    tagline: 'Early Detection Better Tomorrow',
    subtitle: 'Detect kidney disease risk using machine learning',
    quote: '"Healthy kidneys, healthy you."',
    accuracy: '95%',
    icon: Droplet,
    colorScheme: {
      sidebarBg: 'bg-gradient-to-b from-blue-800 via-blue-900 to-blue-950 text-white',
      sidebarActive: 'bg-blue-700/80 text-white shadow-inner',
      headerTitle: 'text-gray-900',
      headerIconBg: 'bg-blue-100 text-blue-600',
      btnBg: 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-200',
      badgeSuccess: 'bg-emerald-100 text-emerald-800 border-emerald-300',
      badgeDanger: 'bg-red-100 text-red-800 border-red-300',
      cardBorder: 'border-blue-100',
      adviceBg: 'bg-blue-50/70 border-blue-200',
      bulletColor: 'text-blue-600',
      barColor: '#2563eb',
      accentText: 'text-blue-600'
    },
    advice: [
      'Stay well hydrated throughout the day',
      'Maintain healthy blood pressure levels',
      'Avoid excessive salt and protein intake',
      'Get regular kidney function screening'
    ],
    fields: [
      { name: 'age', label: 'Age', type: 'number', unit: 'years', defaultValue: 50 },
      { name: 'bp', label: 'Blood Pressure', type: 'number', unit: 'mm Hg', defaultValue: 80 },
      { name: 'sg', label: 'Specific Gravity', type: 'select', options: [
        { value: 1.005, label: '1.005' },
        { value: 1.010, label: '1.010' },
        { value: 1.015, label: '1.015' },
        { value: 1.020, label: '1.020' },
        { value: 1.025, label: '1.025' }
      ], defaultValue: 1.020 },
      { name: 'al', label: 'Albumin', type: 'select', options: [
        { value: 0, label: '0 (Normal)' }, { value: 1, label: '1' }, { value: 2, label: '2' }, { value: 3, label: '3' }, { value: 4, label: '4' }
      ], defaultValue: 1 },
      { name: 'su', label: 'Sugar', type: 'select', options: [
        { value: 0, label: '0 (Normal)' }, { value: 1, label: '1' }, { value: 2, label: '2' }, { value: 3, label: '3' }
      ], defaultValue: 0 },
      { name: 'rbc', label: 'Red Blood Cells', type: 'select', options: [{ value: 'normal', label: 'Normal' }, { value: 'abnormal', label: 'Abnormal' }], defaultValue: 'normal' },
      { name: 'pc', label: 'Pus Cells', type: 'select', options: [{ value: 'normal', label: 'Normal' }, { value: 'abnormal', label: 'Abnormal' }], defaultValue: 'normal' },
      { name: 'pcc', label: 'Pus Cell Clumps', type: 'select', options: [{ value: 'notpresent', label: 'Not Present' }, { value: 'present', label: 'Present' }], defaultValue: 'notpresent' },
      { name: 'ba', label: 'Bacteria', type: 'select', options: [{ value: 'notpresent', label: 'Not Present' }, { value: 'present', label: 'Present' }], defaultValue: 'notpresent' },
      { name: 'bgr', label: 'Blood Glucose Random', type: 'number', unit: 'mg/dl', defaultValue: 100 },
      { name: 'bu', label: 'Blood Urea', type: 'number', unit: 'mg/dl', defaultValue: 40 },
      { name: 'sc', label: 'Serum Creatinine', type: 'number', step: '0.1', unit: 'mg/dl', defaultValue: 1.2 },
      { name: 'sod', label: 'Sodium', type: 'number', unit: 'mEq/L', defaultValue: 135 },
      { name: 'pot', label: 'Potassium', type: 'number', step: '0.1', unit: 'mEq/L', defaultValue: 4.5 },
      { name: 'hemo', label: 'Hemoglobin', type: 'number', step: '0.1', unit: 'g/dl', defaultValue: 13.5 },
      { name: 'pcv', label: 'Packed Cell Volume', type: 'number', defaultValue: 40 },
      { name: 'wbcc', label: 'White Blood Cell Count', type: 'number', defaultValue: 8000 },
      { name: 'rbcc', label: 'Red Blood Cell Count', type: 'number', step: '0.1', defaultValue: 5.2 },
      { name: 'htn', label: 'Hypertension', type: 'select', options: [{ value: 'no', label: 'No' }, { value: 'yes', label: 'Yes' }], defaultValue: 'no' },
      { name: 'dm', label: 'Diabetes Mellitus', type: 'select', options: [{ value: 'no', label: 'No' }, { value: 'yes', label: 'Yes' }], defaultValue: 'no' },
      { name: 'cad', label: 'Coronary Artery Disease', type: 'select', options: [{ value: 'no', label: 'No' }, { value: 'yes', label: 'Yes' }], defaultValue: 'no' },
      { name: 'appet', label: 'Appetite', type: 'select', options: [{ value: 'good', label: 'Good' }, { value: 'poor', label: 'Poor' }], defaultValue: 'good' },
      { name: 'pe', label: 'Pedal Edema', type: 'select', options: [{ value: 'no', label: 'No' }, { value: 'yes', label: 'Yes' }], defaultValue: 'no' },
      { name: 'ane', label: 'Anemia', type: 'select', options: [{ value: 'no', label: 'No' }, { value: 'yes', label: 'Yes' }], defaultValue: 'no' }
    ]
  },
  diabetes: {
    id: 'diabetes',
    name: 'Diabetes Prediction',
    brand: 'DiaCare AI',
    tagline: 'Know Early Live Better',
    subtitle: 'Check your risk of diabetes using machine learning',
    quote: '"Small steps today for a healthier tomorrow."',
    accuracy: '88%',
    icon: Activity,
    colorScheme: {
      sidebarBg: 'bg-gradient-to-b from-purple-800 via-purple-900 to-purple-950 text-white',
      sidebarActive: 'bg-purple-700/80 text-white shadow-inner',
      headerTitle: 'text-gray-900',
      headerIconBg: 'bg-purple-100 text-purple-600',
      btnBg: 'bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-200',
      badgeSuccess: 'bg-emerald-100 text-emerald-800 border-emerald-300',
      badgeDanger: 'bg-red-100 text-red-800 border-red-300',
      cardBorder: 'border-purple-100',
      adviceBg: 'bg-purple-50/70 border-purple-200',
      bulletColor: 'text-purple-600',
      barColor: '#7c3aed',
      accentText: 'text-purple-600'
    },
    advice: [
      'Maintain a healthy, low-sugar diet',
      'Exercise regularly (30 mins a day)',
      'Keep your body weight in a healthy range',
      'Monitor your blood glucose levels'
    ],
    fields: [
      { name: 'preg', label: 'Pregnancies', type: 'number', defaultValue: 1 },
      { name: 'plas', label: 'Glucose Level', type: 'number', unit: 'mg/dl', defaultValue: 120 },
      { name: 'pres', label: 'Blood Pressure', type: 'number', unit: 'mm Hg', defaultValue: 70 },
      { name: 'skin', label: 'Skin Thickness', type: 'number', unit: 'mm', defaultValue: 20 },
      { name: 'insu', label: 'Insulin', type: 'number', unit: 'mu U/ml', defaultValue: 85 },
      { name: 'mass', label: 'BMI', type: 'number', step: '0.1', unit: 'kg/m²', defaultValue: 25.0 },
      { name: 'pedi', label: 'Diabetes Pedigree Function', type: 'number', step: '0.001', defaultValue: 0.5 },
      { name: 'age', label: 'Age', type: 'number', unit: 'years', defaultValue: 30 }
    ]
  },
  liver: {
    id: 'liver',
    name: 'Liver Disease Prediction',
    brand: 'LiverCare AI',
    tagline: 'Healthy Liver Happier Life',
    subtitle: 'Predict the risk of liver disease using machine learning',
    quote: '"Care for your liver, care for your life."',
    accuracy: '90%',
    icon: Stethoscope,
    colorScheme: {
      sidebarBg: 'bg-gradient-to-b from-emerald-800 via-emerald-900 to-emerald-950 text-white',
      sidebarActive: 'bg-emerald-700/80 text-white shadow-inner',
      headerTitle: 'text-gray-900',
      headerIconBg: 'bg-emerald-100 text-emerald-600',
      btnBg: 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-200',
      badgeSuccess: 'bg-emerald-100 text-emerald-800 border-emerald-300',
      badgeDanger: 'bg-red-100 text-red-800 border-red-300',
      cardBorder: 'border-emerald-100',
      adviceBg: 'bg-emerald-50/70 border-emerald-200',
      bulletColor: 'text-emerald-600',
      barColor: '#059669',
      accentText: 'text-emerald-600'
    },
    advice: [
      'Avoid alcohol consumption',
      'Eat a balanced nutrient-rich diet',
      'Maintain a healthy body weight',
      'Get regular liver function tests'
    ],
    fields: [
      { name: 'Age', label: 'Age', type: 'number', unit: 'years', defaultValue: 45 },
      { name: 'Gender', label: 'Gender', type: 'select', options: [{ value: 'Male', label: 'Male' }, { value: 'Female', label: 'Female' }], defaultValue: 'Male' },
      { name: 'TB', label: 'Total Bilirubin', type: 'number', step: '0.1', unit: 'mg/dl', defaultValue: 1.2 },
      { name: 'DB', label: 'Direct Bilirubin', type: 'number', step: '0.1', unit: 'mg/dl', defaultValue: 0.4 },
      { name: 'Alkphos', label: 'Alkaline Phosphatase', type: 'number', unit: 'U/L', defaultValue: 180 },
      { name: 'Sgpt', label: 'Alanine Aminotransferase (ALT)', type: 'number', unit: 'U/L', defaultValue: 45 },
      { name: 'Sgot', label: 'Aspartate Aminotransferase (AST)', type: 'number', unit: 'U/L', defaultValue: 40 },
      { name: 'TP', label: 'Total Proteins', type: 'number', step: '0.1', unit: 'g/dl', defaultValue: 6.8 },
      { name: 'ALB', label: 'Albumin', type: 'number', step: '0.1', unit: 'g/dl', defaultValue: 3.5 },
      { name: 'A/G Ratio', label: 'Albumin and Globulin Ratio', type: 'number', step: '0.01', defaultValue: 1.1 }
    ]
  }
};

const Prediction = () => {
  const { id } = useParams();
  const config = diseaseConfigs[id] || diseaseConfigs['diabetes'];

  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [predictionResult, setPredictionResult] = useState(null);

  useEffect(() => {
    // Pre-populate default values
    const defaults = {};
    config.fields.forEach(f => {
      defaults[f.name] = f.defaultValue !== undefined ? f.defaultValue : '';
    });
    setFormData(defaults);
    setPredictionResult(null);
    setError('');
  }, [id, config]);

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
    setError('');
    try {
      const result = await predictDisease(config.id, formData);
      setPredictionResult(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction request failed. Please check inputs.');
    } finally {
      setLoading(false);
    }
  };

  const DiseaseIcon = config.icon;
  const theme = config.colorScheme;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col lg:flex-row font-sans">
      {/* LEFT SIDEBAR - Tailored per disease */}
      <aside className={`w-full lg:w-64 p-6 flex flex-col justify-between ${theme.sidebarBg} transition-all duration-300`}>
        <div>
          {/* Brand Header */}
          <div className="flex items-center space-x-3 mb-8">
            <div className="p-2.5 bg-white/15 rounded-xl backdrop-blur-sm border border-white/20">
              <DiseaseIcon className="h-7 w-7 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold tracking-wide">{config.brand}</h2>
              <p className="text-xs text-white/70">{config.tagline}</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-2">
            <Link to="/dashboard" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white/80 hover:bg-white/10 hover:text-white transition">
              <Home className="h-5 w-5" />
              <span className="font-medium text-sm">Dashboard</span>
            </Link>
            <div className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-medium text-sm ${theme.sidebarActive}`}>
              <Activity className="h-5 w-5" />
              <span>Prediction</span>
            </div>
            <Link to="/history" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white/80 hover:bg-white/10 hover:text-white transition">
              <Info className="h-5 w-5" />
              <span>History</span>
            </Link>
            <Link to="/profile" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white/80 hover:bg-white/10 hover:text-white transition">
              <HeartHandshake className="h-5 w-5" />
              <span>Profile</span>
            </Link>
          </nav>
        </div>

        {/* Bottom Quote */}
        <div className="mt-8 pt-6 border-t border-white/15">
          <p className="text-xs italic text-white/75 leading-relaxed text-center">
            {config.quote}
          </p>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 p-6 lg:p-8 max-w-7xl mx-auto w-full">
        {/* Header Banner */}
        <div className="flex items-center justify-between bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-8">
          <div className="flex items-center space-x-4">
            <div className={`p-4 rounded-2xl ${theme.headerIconBg}`}>
              <DiseaseIcon className="h-9 w-9" />
            </div>
            <div>
              <h1 className={`text-2xl lg:text-3xl font-extrabold ${theme.headerTitle}`}>
                {config.name}
              </h1>
              <p className="text-sm text-gray-500 mt-1">{config.subtitle}</p>
            </div>
          </div>
          <div className="hidden sm:flex items-center space-x-2 bg-gray-50 px-4 py-2 rounded-xl border border-gray-200/80">
            <Sparkles className={`h-5 w-5 ${theme.accentText}`} />
            <span className="text-xs font-semibold text-gray-700">XGBoost + SHAP Explainable AI</span>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center space-x-3">
            <AlertTriangle className="h-5 w-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Split Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* LEFT FORM COLUMN (7 cols) */}
          <div className="lg:col-span-7 bg-white rounded-2xl p-6 lg:p-8 shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center space-x-2">
              <span>Enter Your Details</span>
            </h3>

            <form onSubmit={onSubmit} className="space-y-5">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {config.fields.map((field) => (
                  <div key={field.name} className="flex flex-col">
                    <label className="text-xs font-semibold text-gray-600 mb-1.5 flex justify-between">
                      <span>{field.label}</span>
                      {field.unit && <span className="text-gray-400 font-normal">{field.unit}</span>}
                    </label>

                    {field.type === 'select' ? (
                      <select
                        name={field.name}
                        value={formData[field.name] !== undefined ? formData[field.name] : field.defaultValue}
                        onChange={handleChange}
                        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3.5 py-2.5 text-sm text-gray-900 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                      >
                        {field.options.map(opt => (
                          <option key={opt.value} value={opt.value}>{opt.label}</option>
                        ))}
                      </select>
                    ) : (
                      <input
                        type={field.type}
                        name={field.name}
                        step={field.step || 'any'}
                        value={formData[field.name] !== undefined ? formData[field.name] : ''}
                        onChange={handleChange}
                        required
                        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3.5 py-2.5 text-sm text-gray-900 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                      />
                    )}
                  </div>
                ))}
              </div>

              <div className="pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full py-3.5 px-6 rounded-xl font-bold text-sm transition transform active:scale-98 flex items-center justify-center space-x-2 ${theme.btnBg} disabled:opacity-50`}
                >
                  {loading ? (
                    <span>Processing with AI...</span>
                  ) : (
                    <>
                      <span>Predict Risk</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* RIGHT PREDICTION RESULT COLUMN (5 cols) */}
          <div className="lg:col-span-5 flex flex-col space-y-6">
            
            {/* Prediction Output Card */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex-1 flex flex-col justify-between">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Prediction Result</h3>

              {predictionResult ? (
                <div className="space-y-6">
                  {/* Status Banner */}
                  <div className={`p-5 rounded-2xl border flex items-start space-x-4 ${
                    predictionResult.risk_level === 'High' ? theme.badgeDanger : theme.badgeSuccess
                  }`}>
                    <div className="p-2 rounded-xl bg-white/80 shadow-sm">
                      {predictionResult.risk_level === 'High' ? (
                        <AlertTriangle className="h-7 w-7 text-red-600" />
                      ) : (
                        <ShieldCheck className="h-7 w-7 text-emerald-600" />
                      )}
                    </div>
                    <div>
                      <h4 className="text-xl font-black">{predictionResult.prediction}</h4>
                      <p className="text-xs mt-1 leading-relaxed opacity-90">
                        {predictionResult.risk_level === 'High'
                          ? `Significant signs detected for ${config.name}. Consult a clinician.`
                          : `No significant health risks detected for ${config.name}.`}
                      </p>
                    </div>
                  </div>

                  {/* 3 Metric Pills */}
                  <div className="grid grid-cols-3 gap-3 text-center">
                    <div className="bg-gray-50 rounded-xl p-3 border border-gray-100">
                      <p className="text-xs font-semibold text-gray-600">Model Accuracy</p>
                      <p className="text-lg font-black text-gray-900 mt-1">{config.accuracy}</p>
                    </div>
                    <div className="bg-gray-50 rounded-xl p-3 border border-gray-100">
                      <p className="text-xs font-semibold text-gray-600">Status</p>
                      <p className={`text-base font-bold mt-1 ${predictionResult.risk_level === 'High' ? 'text-red-600' : 'text-emerald-600'}`}>
                        {predictionResult.risk_level === 'High' ? 'At Risk' : 'Healthy'}
                      </p>
                    </div>
                    <div className="bg-gray-50 rounded-xl p-3 border border-gray-100">
                      <p className="text-xs font-semibold text-gray-600">Risk Level</p>
                      <p className={`text-base font-bold mt-1 ${predictionResult.risk_level === 'High' ? 'text-red-600' : 'text-emerald-600'}`}>
                        {predictionResult.risk_level}
                      </p>
                    </div>
                  </div>

                  {/* Health Advice List */}
                  <div className={`p-4 rounded-xl border ${theme.adviceBg}`}>
                    <h5 className="text-xs font-bold text-gray-800 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <CheckCircle2 className={`h-4 w-4 ${theme.bulletColor}`} />
                      <span>Health Advice</span>
                    </h5>
                    <ul className="space-y-1.5">
                      {config.advice.map((item, idx) => (
                        <li key={idx} className="text-xs text-gray-700 flex items-start space-x-2">
                          <span className={`font-bold ${theme.bulletColor}`}>•</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* SHAP Explanation Graph */}
                  {predictionResult.explanation && predictionResult.explanation.length > 0 && (
                    <div className="pt-2 border-t border-gray-100">
                      <h5 className="text-xs font-bold text-gray-800 uppercase tracking-wider mb-3">
                        Top SHAP Contributing Factors
                      </h5>
                      <div className="h-44 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={predictionResult.explanation.slice(0, 5)}
                            layout="vertical"
                            margin={{ top: 0, right: 10, left: 10, bottom: 0 }}
                          >
                            <XAxis type="number" hide />
                            <YAxis dataKey="feature" type="category" width={110} tick={{ fontSize: 11 }} />
                            <Tooltip formatter={(val) => val.toFixed(4)} />
                            <Bar dataKey="contribution" fill={theme.barColor} radius={[0, 4, 4, 0]} />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                /* Default empty state matching the UI mockup */
                <div className="py-12 px-4 text-center flex flex-col items-center justify-center space-y-4 my-auto">
                  <div className={`p-4 rounded-full ${theme.headerIconBg}`}>
                    <DiseaseIcon className="h-10 w-10" />
                  </div>
                  <h4 className="text-base font-bold text-gray-800">Ready for Health Assessment</h4>
                  <p className="text-xs text-gray-500 max-w-xs leading-relaxed">
                    Fill out your health details on the left and click <strong className={theme.accentText}>Predict Risk</strong> to receive an instant machine learning risk evaluation.
                  </p>
                  
                  {/* Default Static Health Advice preview */}
                  <div className={`w-full p-4 rounded-xl border text-left mt-4 ${theme.adviceBg}`}>
                    <h5 className="text-xs font-bold text-gray-800 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <CheckCircle2 className={`h-4 w-4 ${theme.bulletColor}`} />
                      <span>General Health Advice</span>
                    </h5>
                    <ul className="space-y-1">
                      {config.advice.map((item, idx) => (
                        <li key={idx} className="text-xs text-gray-600 flex items-start space-x-2">
                          <span className={`font-bold ${theme.bulletColor}`}>•</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>

          </div>

        </div>
      </main>
    </div>
  );
};

export default Prediction;
