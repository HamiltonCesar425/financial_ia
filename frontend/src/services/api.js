import axios from "axios";

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const calculateScore = async (payload) => {
  const response = await instance.post("/score", payload);
  return response.data;
};

export const generateDiagnosis = async (payload) => {
  const response = await instance.post("/diagnosis", payload);
  return response.data;
};
