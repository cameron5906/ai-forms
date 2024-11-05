import { FormApi } from "@/api";
import { FormStep } from "@/components/organisms";
import { FormList } from "@/components/organisms/forms";
import { useForms } from "@/hooks/data";
import { StepDto } from "@/models/forms";
import { useEffect, useState } from "react";

interface BuilderProps {
  onFormSelected: (formId: string) => void;
}

export const Builder = ({ onFormSelected }: BuilderProps) => {
  const [title, setTitle] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const { reload } = useForms();

  const handleSubmission = async () => {
    await FormApi.createForm(title, description);
    localStorage.setItem("title", title);
    localStorage.setItem("description", description);
    reload();
  };

  useEffect(() => {
    const title = localStorage.getItem("title");
    if (title) {
      setTitle(title);
    }

    const description = localStorage.getItem("description");
    if (description) {
      setDescription(description);
    }
  }, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "10px",
        width: "100%",
      }}
    >
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
        style={{
          width: "500px",
          padding: "10px",
          backgroundColor: "#f0f0f0",
          borderRadius: "5px",
          border: "none",
          color: "#000",
        }}
      />

      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        rows={10}
        style={{
          width: "500px",
          padding: "10px",
        }}
      />
      <button onClick={handleSubmission}>Generate</button>

      <FormList onFormSelected={onFormSelected} />
    </div>
  );
};
