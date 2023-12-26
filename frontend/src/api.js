import axios from "axios";
const api = axios.create({
    baseURL: "http://localhost:8000"

});

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/uploadImage", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};


export const saveFile = (file, predictionKey) => {
  const formData = new FormData();
  formData.append("file", file);

  // Теперь predictionKey будет передан как параметр запроса
  const options = {
    params: {
      predictionKey: predictionKey
    }
  };

  return api.post("/saveToStorage/", formData, options);
};
export default api

