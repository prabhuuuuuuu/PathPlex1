import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import useQuizStore from "../store/quizStore";
import { careerData } from "../career/careerData";

const Results = () => {
  const { resetQuiz } = useQuizStore();
  const { state } = useLocation();
  const navigate = useNavigate();
  const result = state?.result;

  if (!result) {
    return <div>No results found.</div>;
  }

  const handleReset = () => {
    resetQuiz();
    navigate("/");
  };

  const careerInfo = careerData[result.prediction.career] || {};
  const parsedDate = new Date(result.timestamp);
  parsedDate.setTime(parsedDate.getTime() + 5.5 * 60 * 60 * 1000);
  return (
    <div className="results-page min-h-screen bg-gradient-to-b from-green-100 to-green-200 flex items-center justify-center p-4">
      <div className="grid grid-cols-5 gap-4 w-full max-w-5xl">
        {/* Left Sidebar */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 col-span-1">
          <h3 className="text-xl font-bold text-gray-800 dark:text-white">Career Details</h3>
          <p className="text-gray-700 dark:text-gray-300 mt-2">{careerInfo.details}</p>
        </div>

        {/* Main Content */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 col-span-3 text-center">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">Quiz Results</h2>
          <h1 className="text-5xl font-extrabold text-green-600">{result.prediction.career}</h1>
          <p className="text-xl text-gray-700 dark:text-white mt-2">{result.prediction.description}</p>
          <p className="text-sm text-gray-600 dark:text-yellow-400 mt-4">
            <strong>Timestamp:</strong> {parsedDate.toLocaleString()}
          </p>
          <Button onClick={handleReset} className="mt-4 bg-blue-500 text-white hover:bg-blue-600">
            Reset Quiz
          </Button>
        </div>

        {/* Right Sidebar */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 col-span-1">
          <h3 className="text-xl font-bold text-gray-800 dark:text-white">Skills Needed</h3>
          <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mt-2">
            {careerInfo.skills?.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Results;
