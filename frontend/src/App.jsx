import React, { useState, useRef, useEffect } from 'react';
import {
  Upload,
  Sparkles,
  RefreshCw,
  AlertTriangle,
  CheckCircle2,
  Bug,
  ChevronDown,
  Edit2
} from 'lucide-react';

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [debugMode, setDebugMode] = useState(false);
  const [availableDishes, setAvailableDishes] = useState([]);
  const fileInputRef = useRef(null);

  // Fetch available food classes for manual selection
  useEffect(() => {
    fetch('https://food-nutrition-analyzer-oy6z.onrender.com/api/food-classes')
      .then(res => res.json())
      .then(data => {
        if (data && data.options) setAvailableDishes(data.options);
      })
      .catch(err => console.log('Classes fetch note:', err));
  }, []);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
      setPreviewUrl(URL.createObjectURL(file));
      setResults(null);
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setError(null);
      setPreviewUrl(URL.createObjectURL(file));
      setResults(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please upload an image of a food plate.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('https://food-nutrition-analyzer-oy6z.onrender.com/api/, {
        method: 'POST',
        body: formData,
      });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || 'Food analysis failed.');
    }

    const data = await response.json();
    setResults(data);
  } catch (err) {
    setError(err.message || 'An error occurred during food analysis.');
  } finally {
    setLoading(false);
  }
};

const handleDishChange = async (dishIndex, newKey) => {
  if (!results) return;

  const updatedDishes = [...results.nutrition_per_dish];
  const currentItem = updatedDishes[dishIndex];

  // Build payload for live recalculation
  const itemsPayload = updatedDishes.map((item, idx) => ({
    id: item.id || `dish_${idx + 1}`,
    key: idx === dishIndex ? newKey : (item.key || item.raw_name || 'salad'),
    quantity_g: item.quantity_g
  }));

  try {
    const res = await fetch('https://food-nutrition-analyzer-oy6z.onrender.com/api/recalculate-nutrition', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: itemsPayload })
    });

    if (res.ok) {
      const data = await res.json();
      setResults(prev => ({
        ...prev,
        nutrition_per_dish: data.dishes_nutrition,
        total_nutrition: data.total_nutrition,
        detected_dishes: prev.detected_dishes.map((d, i) => {
          if (i === dishIndex) {
            const matched = data.dishes_nutrition[i];
            return {
              ...d,
              name: matched.dish,
              display_name: matched.dish,
              is_low_confidence: false,
              calories: matched.calories,
              protein: matched.protein,
              carbs: matched.carbs,
              fat: matched.fat,
              fiber: matched.fiber
            };
          }
          return d;
        })
      }));
    }
  } catch (e) {
    console.error('Recalculation note:', e);
  }
};

const handleQuantityChange = async (dishIndex, newQty) => {
  if (!results) return;
  const qty = Math.max(10, Math.min(800, parseFloat(newQty) || 0));

  const updatedDishes = [...results.nutrition_per_dish];
  updatedDishes[dishIndex].quantity_g = qty;

  const itemsPayload = updatedDishes.map((item) => ({
    id: item.id,
    key: item.key || 'salad',
    quantity_g: item.quantity_g
  }));

  try {
    const res = await fetch('https://food-nutrition-analyzer-oy6z.onrender.com/api/recalculate-nutrition', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: itemsPayload })
    });

    if (res.ok) {
      const data = await res.json();
      setResults(prev => ({
        ...prev,
        nutrition_per_dish: data.dishes_nutrition,
        total_nutrition: data.total_nutrition
      }));
    }
  } catch (e) {
    console.error('Quantity update note:', e);
  }
};

const handleReset = () => {
  setSelectedFile(null);
  setPreviewUrl(null);
  setResults(null);
  setError(null);
  if (fileInputRef.current) fileInputRef.current.value = '';
};

return (
  <div className="app-container">
    {/* Header */}
    <div className="header-simple">
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '12px' }}>
        <h1>Food Nutrition Detector</h1>
        <button
          className={`debug-toggle-btn ${debugMode ? 'active' : ''}`}
          onClick={() => setDebugMode(!debugMode)}
          title="Toggle Debug Mode"
        >
          <Bug size={14} /> Debug Mode
        </button>
      </div>
      <p>Upload a food plate image to detect multiple dishes and calculate accurate nutrition</p>
    </div>

    {/* 1. UPLOAD FOOD IMAGE */}
    <div className="card">
      <div className="card-header">
        <h2>UPLOAD FOOD IMAGE</h2>
        {(selectedFile || results) && (
          <button className="btn-secondary" onClick={handleReset}>
            <RefreshCw size={14} /> New Image
          </button>
        )}
      </div>

      <div
        className={`dropzone ${selectedFile ? 'has-file' : ''}`}
        onClick={() => fileInputRef.current?.click()}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept="image/*"
          style={{ display: 'none' }}
        />
        <Upload size={34} className="upload-icon" />
        <p className="dropzone-text">
          {selectedFile ? selectedFile.name : 'Click or Drag & Drop Food Plate Image'}
        </p>
        <span className="dropzone-sub">Supports clear photos containing one or multiple dishes</span>
      </div>

      {error && (
        <div className="error-alert">
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      <button
        className="btn-analyze"
        onClick={handleAnalyze}
        disabled={loading || !selectedFile}
      >
        {loading ? (
          <>
            <div className="spinner" />
            <span>Analyzing Food Regions & Classifying...</span>
          </>
        ) : (
          <>
            <Sparkles size={18} />
            <span>Analyze Food</span>
          </>
        )}
      </button>
    </div>

    {/* 2. RESULTS */}
    {results && (
      <div className="card results-card">
        <div className="card-header">
          <h2>RESULTS</h2>
          <span style={{ fontSize: '0.85rem', color: '#9CA3AF' }}>
            Detected {results.detected_dishes.length} separate food items
          </span>
        </div>

        <div className="results-top-grid">
          {/* Left: Uploaded Plate Image */}
          <div>
            <h3 className="section-title">Uploaded Plate Image</h3>
            <div className="image-box">
              <img
                src={results.annotated_image || results.original_image || previewUrl}
                alt="Uploaded Food Plate"
              />
            </div>
          </div>

          {/* Right: Detected Dishes with Top 3 Predictions & Confidence */}
          <div>
            <h3 className="section-title">Detected Food Items:</h3>
            <div className="detected-dishes-list">
              {results.detected_dishes.map((dish, i) => (
                <div
                  key={i}
                  className={`detected-dish-item ${dish.is_low_confidence ? 'low-conf-border' : ''}`}
                >
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span className="dish-idx">{i + 1}.</span>
                        <span className="dish-name-text">
                          {dish.is_low_confidence ? (
                            <span style={{ color: '#FCD34D', display: 'flex', alignItems: 'center', gap: '4px' }}>
                              <AlertTriangle size={14} /> Unable to confidently identify ({dish.name})
                            </span>
                          ) : (
                            dish.name
                          )}
                        </span>
                      </div>
                      <span className={`dish-conf-pill ${dish.is_low_confidence ? 'low-conf-pill' : ''}`}>
                        {dish.confidence}%
                      </span>
                    </div>

                    {/* Top 3 Predictions Pills */}
                    {dish.top3_predictions && dish.top3_predictions.length > 0 && (
                      <div className="top3-predictions-bar">
                        <span className="top3-label">Top Predictions:</span>
                        <div className="top3-pills">
                          {dish.top3_predictions.map((pred, pIdx) => (
                            <button
                              key={pIdx}
                              type="button"
                              className="top3-btn"
                              onClick={() => handleDishChange(i, pred.key)}
                              title={`Click to select ${pred.name}`}
                            >
                              {pred.name} ({pred.confidence}%)
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* NUTRITION PER DISH */}
        <div className="section-block">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <h3 className="section-title" style={{ margin: 0 }}>NUTRITION PER DISH</h3>
            <span style={{ fontSize: '0.8rem', color: '#9CA3AF' }}>Portion weights in grams are editable</span>
          </div>

          <div className="table-wrap">
            <table className="simple-table">
              <thead>
                <tr>
                  <th>Dish</th>
                  <th>Quantity (g)</th>
                  <th>Calories</th>
                  <th>Protein</th>
                  <th>Carbs</th>
                  <th>Fat</th>
                  <th>Fiber</th>
                </tr>
              </thead>
              <tbody>
                {results.nutrition_per_dish.map((dish, idx) => (
                  <tr key={idx}>
                    <td className="font-bold">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span>{dish.dish}</span>
                        {/* Manual Correction Selector */}
                        <select
                          className="dish-select-dropdown"
                          value={dish.key || ''}
                          onChange={(e) => handleDishChange(idx, e.target.value)}
                          title="Change dish"
                        >
                          <option value="" disabled>Change dish...</option>
                          {availableDishes.map(opt => (
                            <option key={opt.key} value={opt.key}>{opt.name}</option>
                          ))}
                        </select>
                      </div>
                    </td>
                    <td>
                      <input
                        type="number"
                        min="10"
                        max="800"
                        step="5"
                        value={dish.quantity_g}
                        onChange={(e) => handleQuantityChange(idx, e.target.value)}
                        className="portion-input"
                      /> g
                    </td>
                    <td className="cal-text">{dish.calories} kcal</td>
                    <td>{dish.protein} g</td>
                    <td>{dish.carbs} g</td>
                    <td>{dish.fat} g</td>
                    <td>{dish.fiber} g</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* TOTAL NUTRITION OF THE PLATE */}
        <div className="section-block">
          <h3 className="section-title">TOTAL NUTRITION OF THE PLATE</h3>
          <div className="totals-box-grid">
            <div className="total-box">
              <div className="total-title">Total Calories</div>
              <div className="total-num cal">{results.total_nutrition.total_calories}</div>
              <div className="total-unit">kcal</div>
            </div>
            <div className="total-box">
              <div className="total-title">Total Protein</div>
              <div className="total-num">{results.total_nutrition.total_protein}</div>
              <div className="total-unit">g</div>
            </div>
            <div className="total-box">
              <div className="total-title">Total Carbohydrates</div>
              <div className="total-num">{results.total_nutrition.total_carbs}</div>
              <div className="total-unit">g</div>
            </div>
            <div className="total-box">
              <div className="total-title">Total Fat</div>
              <div className="total-num">{results.total_nutrition.total_fat}</div>
              <div className="total-unit">g</div>
            </div>
            <div className="total-box">
              <div className="total-title">Total Fiber</div>
              <div className="total-num">{results.total_nutrition.total_fiber}</div>
              <div className="total-unit">g</div>
            </div>
          </div>
        </div>

        {/* DEBUG MODE SECTION */}
        {debugMode && results.debug_info && (
          <div className="debug-container">
            <div className="debug-header">
              <Bug size={16} />
              <span>AI Pipeline Debug Inspector</span>
            </div>
            <p style={{ fontSize: '0.82rem', color: '#9CA3AF', marginBottom: '14px' }}>
              Total Regions Detected: <strong>{results.debug_info.total_regions_detected}</strong> |
              Models: YOLO={results.debug_info.models_used.yolo ? 'ON' : 'OFF'},
              ViT={results.debug_info.models_used.vit ? 'ON' : 'OFF'},
              CLIP={results.debug_info.models_used.clip ? 'ON' : 'OFF'}
            </p>

            <div className="debug-crops-grid">
              {results.debug_info.crops.map((crop, cIdx) => (
                <div key={cIdx} className="debug-crop-card">
                  <div className="debug-crop-img-wrap">
                    <img src={crop.crop_image} alt={`Region ${crop.region_id}`} />
                  </div>
                  <div className="debug-crop-details">
                    <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#FFFFFF' }}>
                      Region #{crop.region_id} ({crop.area_percentage}% plate area)
                    </div>
                    <div style={{ fontSize: '0.78rem', color: '#9CA3AF', margin: '4px 0' }}>
                      Selected: <strong style={{ color: '#10B981' }}>{crop.selected}</strong> ({crop.confidence}%)
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#6B7280' }}>
                      Top 3 Predictions:
                      {crop.top3.map((p, pI) => (
                        <div key={pI}>• {p.name}: {p.confidence}%</div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="disclaimer-text">
          * Note: Portion sizes and nutritional values are approximate estimates based on computer vision plate analysis.
        </div>
      </div>
    )}
  </div>
);
}
