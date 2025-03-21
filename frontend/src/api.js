import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",
});

export const login = async (email, password) => {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
};

export const register = async (email, password, role) => {
  const response = await api.post("/auth/register", { email, password, role });
  return response.data;
};

export const getJobs = async () => {
  const response = await api.get("/jobs");
  return response.data;
};

export const createJob = async (jobData) => {
  const response = await api.post("/jobs", jobData);
  return response.data;
};

export const applyForJob = async (jobId, file) => {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("email", localStorage.getItem("email"));
  const response = await api.post(`/jobs/${jobId}/apply`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};