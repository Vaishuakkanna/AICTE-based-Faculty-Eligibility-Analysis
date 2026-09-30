import { useState, useRef, useEffect } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  
  // Fun loading messages
  const loadingMessages = [
    "Uploading PDF to secure server...",
    "Extracting dense text from resume pages...",
    "Semantic search on AICTE knowledge base...",
    "Reranking top guidelines with CrossEncoder...",
    "Cross-referencing candidate experience...",
    "LLM evaluating final eligibility verdict...",
    "Almost there, wrapping up..."
  ];
  const [msgIdx, setMsgIdx] = useState(0);

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setMsgIdx((prev) => (prev + 1) % loadingMessages.length);
      }, 3000); // cycle every 3 seconds
    } else {
      setMsgIdx(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !question) {
      setError('Please provide both a PDF resume and a question.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('question', question);

    try {
      // Connects to the FastAPI backend
      const response = await fetch('http://localhost:8000/api/evaluate', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Server Error: ${response.statusText}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="background-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
      </div>



      <main>
        <div className="glass-panel">
          <form onSubmit={handleSubmit}>
            <div 
              className="drop-zone"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              {file ? (
                <div className="file-selected">
                  <span className="file-icon">📄</span>
                  <p>{file.name}</p>
                  <small>Click to change file</small>
                </div>
              ) : (
                <div className="drop-content">
                  <span className="upload-icon">☁️</span>
                  <p>Drag & Drop your PDF here</p>
                  <small>or click to browse</small>
                </div>
              )}
              <input 
                type="file" 
                ref={fileInputRef}
                onChange={(e) => setFile(e.target.files[0])}
                accept=".pdf"
                hidden
              />
            </div>

            <div className="input-group">
              <input 
                type="text" 
                placeholder="E.g., Is this professor eligible for HOD in IS?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
            </div>

            <button type="submit" disabled={loading} className={loading ? 'loading-btn' : ''}>
              {loading ? (
                <div className="loading-content">
                  <div className="cube-loader">
                    <div className="cube"></div>
                    <div className="cube"></div>
                    <div className="cube"></div>
                    <div className="cube"></div>
                  </div>
                  <span className="loading-text animate-pulse">{loadingMessages[msgIdx]}</span>
                </div>
              ) : (
                'Evaluate Candidate ✨'
              )}
            </button>
            
            {error && <div className="error-message">{error}</div>}
          </form>
        </div>

        {result && (
          <div className="result-container fade-in">
            <div className="evaluation-card glass-panel">
              <h2>Evaluation Verdict</h2>
              <div className={`verdict ${result.evaluation.includes('NOT ELIGIBLE') ? 'rejected' : 'approved'}`}>
                {result.evaluation}
              </div>
            </div>

            <div className="details-grid">
              <div className="glass-panel detail-card">
                <h3><span className="icon">📚</span> Retrieved AICTE Guidelines</h3>
                <ul className="guideline-list">
                  {result.retrieved_chunks.map((chunk, i) => (
                    <li key={i}>
                      <div className="guideline-badge">Rule {i+1}</div>
                      <div className="guideline-text">{chunk.text.substring(0, 150)}...</div>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="glass-panel detail-card json-card">
                <h3><span className="icon">⚡</span> Extracted Details</h3>
                <div className="mac-window">
                  <div className="mac-header">
                    <div className="mac-buttons">
                      <span className="mac-dot red"></span>
                      <span className="mac-dot yellow"></span>
                      <span className="mac-dot green"></span>
                    </div>
                    <div className="mac-title">resume_data.json</div>
                  </div>
                  <pre className="json-display">
                    {JSON.stringify(result.resume_kv, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
