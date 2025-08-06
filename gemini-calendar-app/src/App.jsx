import React, { useState, useEffect } from 'react';

function App() {
  const [calendars, setCalendars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/calendars.json')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setCalendars(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-gray-700 text-lg">Loading calendars...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-red-500 text-lg">Error: {error.message}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Academic Calendars
          </h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            {calendars.length > 0 ? (
              <ul className="space-y-4">
                {calendars.map((calendar) => (
                  <li key={calendar.file} className="bg-white shadow overflow-hidden rounded-md px-6 py-4 flex items-center justify-between">
                    <span className="text-lg font-medium text-gray-900">{calendar.name}</span>
                    <a href={`/${calendar.file}`} download className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                      Download
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-700 text-lg">No calendars found.</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;