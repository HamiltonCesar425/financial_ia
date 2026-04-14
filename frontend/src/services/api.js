import axios from "axios";

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const calculateScore = async (payload) => {
  return instance.post("/score", payload);
};
