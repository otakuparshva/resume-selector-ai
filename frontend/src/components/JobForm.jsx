import React, { useState } from "react";
import { createJob } from "../api";

const JobForm = () => {
  const [title, setTitle] = useState("");
  const [department, setDepartment] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [skills, setSkills] = useState("");
  const [salaryMin, setSalaryMin] = useState(0);
  const [salaryMax, setSalaryMax] = useState(0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await createJob({
        title,
        department,
        location,
        description,
        skills,
        salary_min: salaryMin,
        salary_max: salaryMax,
        created_by: localStorage.getItem("email"),
      });
      alert(response.message);
    } catch (error) {
      console.error("Failed to create job:", error);
    }
  };

  return (
    <div>
      <h1>Post a Job</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Job Title"
        />
        <input
          type="text"
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
          placeholder="Department"
        />
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Location"
        />
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Job Description"
        />
        <textarea
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          placeholder="Required Skills (one per line)"
        />
        <input
          type="number"
          value={salaryMin}
          onChange={(e) => setSalaryMin(e.target.value)}
          placeholder="Minimum Salary"
        />
        <input
          type="number"
          value={salaryMax}
          onChange={(e) => setSalaryMax(e.target.value)}
          placeholder="Maximum Salary"
        />
        <button type="submit">Post Job</button>
      </form>
    </div>
  );
};

export default JobForm;