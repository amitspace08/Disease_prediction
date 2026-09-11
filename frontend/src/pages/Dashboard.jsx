import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import { Heart, Activity, Droplet, Stethoscope, ArrowRight, ShieldCheck } from 'lucide-react';

const Dashboard = () => {
  const { user } = useContext(AuthContext);

  const diseases = [
    {
      id: 'heart',
      name: 'Heart Disease Prediction',
      brand: 'HeartCare AI',
      subtitle: 'Predict Today For a Healthier Tomorrow',
      desc: 'Evaluate cardiovascular risks using chest pain, cholesterol, ECG, and blood pressure vitals.',
      icon: Heart,
      accuracy: '92% Accuracy',
      theme: {
        cardBg: 'bg-gradient-to-br from-red-600 to-red-800 text-white',
        btnBg: 'bg-white text-red-700 hover:bg-red-50',
        badgeBg: 'bg-white/20 text-white',
        iconBg: 'bg-white/10 text-white'
      }
    },
    {
      id: 'kidney',
      name: 'Kidney Disease Prediction',
      brand: 'KidneyCare AI',
      subtitle: 'Early Detection Better Tomorrow',
      desc: 'Detect chronic kidney disease risk using blood urea, serum creatinine, and specific gravity.',
      icon: Droplet,
      accuracy: '95% Accuracy',
      theme: {
        cardBg: 'bg-gradient-to-br from-blue-600 to-blue-800 text-white',
        btnBg: 'bg-white text-blue-700 hover:bg-blue-50',
        badgeBg: 'bg-white/20 text-white',
        iconBg: 'bg-white/10 text-white'
      }
    },
    {
      id: 'diabetes',
      name: 'Diabetes Prediction',
      brand: 'DiaCare AI',
      subtitle: 'Know Early Live Better',
      desc: 'Analyze blood glucose levels, insulin, BMI, and pedigree function to assess diabetes risk.',
      icon: Activity,
      accuracy: '88% Accuracy',
      theme: {
        cardBg: 'bg-gradient-to-br from-purple-600 to-purple-800 text-white',
        btnBg: 'bg-white text-purple-700 hover:bg-purple-50',
        badgeBg: 'bg-white/20 text-white',
        iconBg: 'bg-white/10 text-white'
      }
    },
    {
      id: 'liver',
      name: 'Liver Disease Prediction',
      brand: 'LiverCare AI',
      subtitle: 'Healthy Liver Happier Life',
      desc: 'Evaluate total bilirubin, alkaline phosphatase, and protein enzymes for liver health assessment.',
      icon: Stethoscope,
      accuracy: '90% Accuracy',
      theme: {
        cardBg: 'bg-gradient-to-br from-emerald-600 to-emerald-800 text-white',
        btnBg: 'bg-white text-emerald-700 hover:bg-emerald-50',
        badgeBg: 'bg-white/20 text-white',
        iconBg: 'bg-white/10 text-white'
      }
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Top Banner */}
      <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 mb-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900">
            Welcome{user ? `, ${user.name}` : ''}
          </h1>
          <p className="text-gray-500 mt-2 text-sm max-w-2xl leading-relaxed">
            Select a specialized AI decision support model below to analyze medical parameters with full <strong>SHAP Explainable AI transparency</strong>.
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-blue-50 text-blue-700 px-4 py-2.5 rounded-2xl border border-blue-100 text-xs font-semibold">
          <ShieldCheck className="h-5 w-5" />
          <span>XGBoost + SHAP Decision Support</span>
        </div>
      </div>

      {/* Disclaimer Alert */}
      <div className="mb-10 p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-800 text-xs leading-relaxed">
        <strong>Medical Disclaimer:</strong> This system is intended for educational and decision-support purposes only and is not a substitute for professional medical diagnosis or treatment.
      </div>

      {/* Disease Cards Grid (Matching the 4 Mockup Themes) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {diseases.map((d) => {
          const Icon = d.icon;
          const theme = d.theme;
          return (
            <div key={d.id} className={`rounded-3xl p-8 shadow-md transition-all duration-300 hover:shadow-xl hover:-translate-y-1 flex flex-col justify-between ${theme.cardBg}`}>
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div className={`p-3.5 rounded-2xl ${theme.iconBg} backdrop-blur-sm`}>
                    <Icon className="h-8 w-8" />
                  </div>
                  <span className={`text-xs font-bold px-3 py-1.5 rounded-full ${theme.badgeBg}`}>
                    {d.accuracy}
                  </span>
                </div>

                <h2 className="text-xs uppercase font-bold tracking-widest opacity-80">{d.brand}</h2>
                <h3 className="text-2xl font-black mt-1 mb-2">{d.name}</h3>
                <p className="text-xs text-white/80 italic mb-4">{d.subtitle}</p>
                <p className="text-sm text-white/90 leading-relaxed mb-6">{d.desc}</p>
              </div>

              <Link
                to={`/predict/${d.id}`}
                className={`w-full py-3.5 px-6 rounded-2xl font-bold text-sm transition flex items-center justify-center space-x-2 shadow-md ${theme.btnBg}`}
              >
                <span>Start {d.name.split(' ')[0]} Assessment</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Dashboard;
