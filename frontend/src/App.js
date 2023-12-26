import React, { useState } from 'react';
import { uploadFile, saveFile } from './api'; // Импортируем функцию сохранения файла
import './style.css';
import axios from "axios";

function App() {
  const [fileUploadMessage, setFileUploadMessage] = useState('');
  const [predictionResult, setPredictionResult] = useState({});
  const [uploadedImage, setUploadedImage] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [showConfirmation2, setShowConfirmation2] = useState(false);
  const [fileToSave, setFileToSave] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        setUploadedImage(reader.result);
      };

      uploadFile(file)
        .then((response) => {
          const predictions = response.data;
          setPredictionResult(predictions);
          setFileToSave(file);
          setShowConfirmation(true);
        })
        .catch((error) => {
          console.error('Error uploading file:', error);
          setFileUploadMessage('Error uploading file.');
        });
    }
  };

  const handleConfirmation = (shouldSave) => {
    if (shouldSave) {

        setShowConfirmation2(true);
    }
    else{
        setShowConfirmation(false);
        saveFile(fileToSave, "None")
        .then((response) => {
          console.log('File saved:', response.data);
        })
        .catch((error) => {
          console.error('Error saving file:', error);
        });
    }
    setShowConfirmation(false);
  };
  const handleConfirmation2 = (shouldSave) => {
    if (shouldSave) {
    saveFile(fileToSave, Object.keys(predictionResult)[0])
        .then((response) => {
          console.log('File saved:', response.data);
        })
        .catch((error) => {
          console.error('Error saving file:', error);
        });
    }
    else{

        saveFile(fileToSave, "None")
        .then((response) => {
          console.log('File saved:', response.data);
        })
        .catch((error) => {
          console.error('Error saving file:', error);
        });
    }
    setShowConfirmation2(false);
  };



  return (
    <div className="App">
      <h1>Welcome to DermAI</h1>
      <div className="container">
        <label className="customFileInput">
          Choose File
          <input type="file" onChange={handleFileChange} style={{ display: 'none' }} />
        </label>
        {Object.keys(predictionResult).length > 0 && (
          <div>
            <h2>Prediction Results</h2>
            <ul className="resultList">
              {Object.entries(predictionResult).map(([key, value]) => (
                <li key={key}>
                  {key}: {value}
                </li>
              ))}
              {uploadedImage && <img src={uploadedImage} alt="Uploaded" style={{ maxWidth: '300px' }} />}
            </ul>
          </div>
        )}
      </div>
      <p>{fileUploadMessage}</p>
        <div className="container">
      {showConfirmation && (
        <div>
          <p>Вы знаете свою проблему ?</p>
            <label className="customButton" onClick={() => handleConfirmation(true)}>
                 Да
             <input type="button" style={{ display: 'none' }} />
            </label>
                     <label className="customButton" onClick={() => handleConfirmation(false)}>
                 Нет
             <input type="button" style={{ display: 'none' }} />
            </label>
        </div>
      )}
</div>
        <div className="container">
        {showConfirmation2 && (
        <div>
          <p>Правильно ли былы предсказано, что это {Object.keys(predictionResult)[0]}?</p>
            <label className="customButton" onClick={() => handleConfirmation2(true)}>
                 Да
             <input type="button" style={{ display: 'none' }} />
            </label>
                     <label className="customButton" onClick={() => handleConfirmation2(false)}>
                 Нет
             <input type="button" style={{ display: 'none' }} />
            </label>
        </div>
      )}
             </div>
        <div className="container">Вы также можете скачать себе приложение на компьютер и пользоваться без доступа к интернету!
        <a href="https://disk.yandex.ru/d/Fz3rG91McNvA_A" download>Скачать приложение</a></div>
    </div>

  );

}

export default App;