import React, { useEffect, useState } from "react";
import { getApplications } from "../api";

const ApplicationList = ({ jobId }) => {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const response = await getApplications(jobId);
        setApplications(response.data);
      } catch (error) {
        console.error("Failed to fetch applications:", error);
      }
    };
    fetchApplications();
  }, [jobId]);

  return (
    <div>
      <h2>Applications</h2>
      {applications.map((app) => (
        <div key={app.id}>
          <h3>{app.candidate_id}</h3>
          <p>Match Score: {app.match_score}</p>
          <p>Applied At: {new Date(app.applied_at).toLocaleString()}</p>
          <textarea value={app.resume_text} readOnly />
        </div>
      ))}
    </div>
  );
};

export default ApplicationList;