import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getJobs, applyForJob } from "../api";

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await getJobs();
        setJobs(response.data);
      } catch (error) {
        console.error("Failed to fetch jobs:", error);
      }
    };
    fetchJobs();
  }, []);

  const handleApply = async (jobId, file) => {
    try {
      const response = await applyForJob(jobId, file);
      alert(response.message);
    } catch (error) {
      console.error("Failed to apply for job:", error);
    }
  };

  return (
    <div>
      <h1>Dashboard</h1>
      {jobs.map((job) => (
        <div key={job.id}>
          <h2>{job.title}</h2>
          <p>{job.description}</p>
          <input
            type="file"
            onChange={(e) => handleApply(job.id, e.target.files[0])}
          />
        </div>
      ))}
    </div>
  );
};

export default Dashboard;