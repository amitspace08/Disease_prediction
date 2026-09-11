import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { predictDisease } from '../services/predictionService';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  Heart, Activity, Droplet, Stethoscope, Home, Info, HeartHandshake,
  CheckCircle2, AlertTriangle, ShieldCheck, Sparkles, SlidersHorizontal
} from 'lucide-react';

const OrganIllustration = ({ disease }) => {
  if (disease === 'heart') {
    return (
      <div className="relative w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center bg-red-50 rounded-2xl border border-red-100 p-2 shadow-sm flex-shrink-0">
        <svg viewBox="0 0 100 100" className="w-full h-full text-red-500 fill-current drop-shadow-md">
          <path d="M50 88s-32-20-40-38c-8-18 2-34 18-34 10 0 18 6 22 13 4-7 12-13 22-13 16 0 26 16 18 34-8 18-40 38-40 38z" />
          <path d="M26 50h14l4-8 6 16 6-12 4 4h14" fill="none" stroke="#ffffff" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    );
  }
  if (disease === 'kidney') {
    return (
      <div className="relative w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center bg-blue-50 rounded-2xl border border-blue-100 p-2 shadow-sm flex-shrink-0">
        <svg viewBox="0 0 100 100" className="w-full h-full text-blue-500 fill-current drop-shadow-md">
          <path d="M30 25c-12 0-20 12-18 28 2 16 14 32 24 32 6 0 10-6 8-12-2-6-8-10-8-18s6-14 10-18c2-2-2-12-16-12z" />
          <path d="M70 25c12 0 20 12 18 28-2 16-14 32-24 32-6 0-10-6-8-12 2-6 8-10 8-18s-6-14-10-18c-2-2 2-12 16-12z" />
        </svg>
      </div>
    );
  }
  if (disease === 'diabetes') {
    return (
      <div className="relative w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center bg-purple-50 rounded-2xl border border-purple-100 p-2 shadow-sm flex-shrink-0">
        <div className="w-14 h-18 bg-purple-600 rounded-xl flex flex-col items-center justify-between p-2 shadow-md border-2 border-purple-300 text-white">
          <div className="w-full bg-purple-950 rounded py-1 text-center font-mono font-black text-xs text-emerald-300">
            98
          </div>
          <div className="w-2.5 h-2.5 rounded-full bg-purple-200"></div>
          <div className="text-[8px] font-extrabold tracking-widest text-purple-200">GLUCO</div>
        </div>
      </div>
    );
  }
  if (disease === 'liver') {
    return (
      <div className="relative w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center bg-emerald-50 rounded-2xl border border-emerald-100 p-2 shadow-sm flex-shrink-0">
        <svg viewBox="0 0 100 100" className="w-full h-full text-emerald-600 fill-current drop-shadow-md">
          <path d="M18 35c15-10 45-12 62-2 10 7 12 22 2 32-15 15-40 25-60 15-8-4-10-18-4-45z" />
        </svg>
      </div>
    );
  }
  return null;
};

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
      sidebarActive: 'bg-red-700/90 text-white shadow-inner',
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
      sidebarActive: 'bg-blue-700/90 text-white shadow-inner',
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
      sidebarActive: 'bg-purple-700/90 text-white shadow-inner',
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
      sidebarActive: 'bg-emerald-700/90 text-white shadow-inner',
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
    <div className="min-h-[calc(100vh-4rem)] bg-gray-100 flex flex-col lg:flex-row font-sans">
      {/* FIXED PINNED SIDEBAR UNDER TOP NAVBAR */}
      <aside className={`w-full lg:w-64 p-6 flex flex-col justify-between ${theme.sidebarBg} lg:sticky lg:top-16 lg:h-[calc(100vh-4rem)] z-30 transition-all duration-300 flex-shrink-0`}>
        <div>
          {/* Brand Header */}
          <div className="flex items-center space-x-3 mb-8">
            <div className="p-2.5 bg-white/15 rounded-xl backdrop-blur-sm border border-white/20 shadow-sm">
              <DiseaseIcon className="h-7 w-7 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-black tracking-wide leading-tight">{config.brand}</h2>
              <p className="text-[11px] text-white/70">{config.tagline}</p>
            </div>
          </div>

          {/* Sidebar Navigation */}
          <nav className="space-y-2">
            <Link to="/dashboard" className="flex items-center space-x-3 px-4 py-3 rounded-xl text-white/80 hover:bg-white/10 hover:text-white transition">
              <Home className="h-5 w-5" />
              <span className="font-medium text-sm">Dashboard</span>
            </Link>
            <div className={`flex items-center space-x-3 px-4 py-3 rounded-xl font-bold text-sm ${theme.sidebarActive}`}>
              <Activity className="h-5 w-5" />
              <span>Prediction</span>
            </div>
            <Link to="/history" className="flex items-center space-x-3 px-4 py-3 rounded-xl text-white/80 hover:bg-white/10 hover:text-white transition">
              <Info className="h-5 w-5" />
              <span className="font-medium text-sm">History</span>
            </Link>
            <Link to="/profile" className="flex items-center space-x-3 px-4 py-3 rounded-xl text-white/80 hover:bg-white/10 hover:text-white transition">
              <HeartHandshake className="h-5 w-5" />
              <span className="font-medium text-sm">Profile</span>
            </Link>
          </nav>
        </div>

        {/* Quote at bottom */}
        <div className="mt-8 pt-4 border-t border-white/15">
          <p className="text-xs italic text-white/75 leading-relaxed text-center">
            {config.quote}
          </p>
        </div>
      </aside>

      {/* SCROLLABLE MAIN CONTENT */}
      <main className="flex-1 p-6 lg:p-8 max-w-7xl mx-auto w-full">
        
        {/* TOP HEADER CARD WITH 3D ORGAN GRAPHIC */}
        <div className="flex items-center justify-between bg-white rounded-3xl p-6 shadow-sm border border-gray-100 mb-8 relative overflow-hidden">
          <div className="flex items-center space-x-4 z-10">
            <div className={`p-4 rounded-2xl ${theme.headerIconBg}`}>
              <DiseaseIcon className="h-8 w-8 sm:h-10 sm:w-10" />
            </div>
            <div>
              <h1 className={`text-2xl sm:text-3xl font-black ${theme.headerTitle}`}>
                {config.name}
              </h1>
              <p className="text-xs sm:text-sm text-gray-500 mt-1">{config.subtitle}</p>
            </div>
          </div>

          <div className="flex items-center space-x-6 z-10">
            <div className="hidden md:flex items-center space-x-2 bg-gray-50 px-4 py-2.5 rounded-2xl border border-gray-200/80">
              <Sparkles className={`h-4 w-4 ${theme.accentText}`} />
              <span className="text-xs font-bold text-gray-700">XGBoost + SHAP Explainable AI</span>
            </div>
            
            {/* Custom Organ Illustration */}
            <OrganIllustration disease={config.id} />
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center space-x-3">
            <AlertTriangle className="h-5 w-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Form and Results Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* LEFT FORM COLUMN (7 cols) */}
          <div className="lg:col-span-7 bg-white rounded-3xl p-6 lg:p-8 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-100">
              <h3 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
                <SlidersHorizontal className={`h-5 w-5 ${theme.accentText}`} />
                <span>Enter Your Details</span>
              </h3>
              <span className="text-xs text-gray-400 font-medium">All parameters required</span>
            </div>

            <form onSubmit={onSubmit} className="space-y-5">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {config.fields.map((field) => (
                  <div key={field.name} className="flex flex-col">
                    <label className="text-xs font-semibold text-gray-700 mb-1.5 flex justify-between">
                      <span>{field.label}</span>
                      {field.unit && <span className="text-gray-400 font-normal">{field.unit}</span>}
                    </label>

                    {field.type === 'select' ? (
                      <select
                        name={field.name}
                        value={formData[field.name] !== undefined ? formData[field.name] : field.defaultValue}
                        onChange={handleChange}
                        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3.5 py-2.5 text-sm text-gray-900 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition font-medium"
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
                        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3.5 py-2.5 text-sm text-gray-900 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition font-medium"
                      />
                    )}
                  </div>
                ))}
              </div>

              <div className="pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full py-3.5 px-6 rounded-2xl font-bold text-sm transition transform active:scale-98 flex items-center justify-center space-x-2 ${theme.btnBg} disabled:opacity-50`}
                >
                  {loading ? (
                    <span>Processing with Machine Learning...</span>
                  ) : (
                    <span>Predict Risk</span>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* RIGHT RESULT COLUMN (5 cols) */}
          <div className="lg:col-span-5 flex flex-col space-y-6">
            
            <div className="bg-white rounded-3xl p-6 lg:p-8 shadow-sm border border-gray-100 flex-1 flex flex-col justify-between">
              <h3 className="text-lg font-bold text-gray-900 mb-4 pb-3 border-b border-gray-100">
                Prediction Result
              </h3>

              {predictionResult ? (
                <div className="space-y-6">
                  {/* Status Banner */}
                  <div className={`p-5 rounded-2xl border flex items-start space-x-4 ${
                    predictionResult.risk_level === 'High' ? theme.badgeDanger : theme.badgeSuccess
                  }`}>
                    <div className="p-2.5 rounded-xl bg-white/90 shadow-sm">
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
                          ? `High risk indicators found for ${config.name}. Consult a doctor.`
                          : `No significant health risks detected for ${config.name}.`}
                      </p>
                    </div>
                  </div>

                  {/* 3 Metrics Pills */}
                  <div className="grid grid-cols-3 gap-3 text-center">
                    <div className="bg-gray-50 rounded-2xl p-3 border border-gray-100">
                      <p className="text-[11px] font-bold text-gray-500 uppercase">Model Accuracy</p>
                      <p className="text-base sm:text-lg font-black text-gray-900 mt-1">{config.accuracy}</p>
                    </div>
                    <div className="bg-gray-50 rounded-2xl p-3 border border-gray-100">
                      <p className="text-[11px] font-bold text-gray-500 uppercase">Status</p>
                      <p className={`text-sm sm:text-base font-bold mt-1 ${predictionResult.risk_level === 'High' ? 'text-red-600' : 'text-emerald-600'}`}>
                        {predictionResult.risk_level === 'High' ? 'At Risk' : 'Healthy'}
                      </p>
                    </div>
                    <div className="bg-gray-50 rounded-2xl p-3 border border-gray-100">
                      <p className="text-[11px] font-bold text-gray-500 uppercase">Risk Level</p>
                      <p className={`text-sm sm:text-base font-bold mt-1 ${predictionResult.risk_level === 'High' ? 'text-red-600' : 'text-emerald-600'}`}>
                        {predictionResult.risk_level}
                      </p>
                    </div>
                  </div>

                  {/* Health Advice List */}
                  <div className={`p-4 rounded-2xl border ${theme.adviceBg}`}>
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
                    <div className="pt-3 border-t border-gray-100">
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
                /* Default empty state */
                <div className="py-10 px-4 text-center flex flex-col items-center justify-center space-y-4 my-auto">
                  <div className={`p-4 rounded-2xl ${theme.headerIconBg}`}>
                    <DiseaseIcon className="h-10 w-10" />
                  </div>
                  <h4 className="text-base font-extrabold text-gray-900">Ready for Health Assessment</h4>
                  <p className="text-xs text-gray-500 max-w-xs leading-relaxed">
                    Fill out your parameters on the left and click <strong className={theme.accentText}>Predict Risk</strong> to receive an instant machine learning risk evaluation.
                  </p>
                  
                  <div className={`w-full p-4 rounded-2xl border text-left mt-4 ${theme.adviceBg}`}>
                    <h5 className="text-xs font-bold text-gray-800 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <CheckCircle2 className={`h-4 w-4 ${theme.bulletColor}`} />
                      <span>General Health Advice</span>
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
