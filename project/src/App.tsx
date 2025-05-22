import React from 'react';
import ChatBot from './components/ChatBot';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-green-50 p-4 sm:p-6 md:p-8 flex items-center justify-center">
      <div className="w-full max-w-4xl h-[80vh] flex flex-col rounded-xl overflow-hidden shadow-2xl">
        <ChatBot />
      </div>
    </div>
  );
}

export default App;