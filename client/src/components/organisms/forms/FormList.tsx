import { useForms } from "@/hooks/data";

interface FormListProps {
  onFormSelected: (id: string) => void; // Callback prop to handle form selection
}

export const FormList: React.FC<FormListProps> = ({ onFormSelected }) => {
  const { forms } = useForms();

  return (
    <div>
      <h2>Form List</h2>
      <div>
        {forms.map(({ id, title }) => (
          <div
            key={id}
            className="form-list-item"
            onClick={() => onFormSelected(id)}
            style={{
              cursor: "pointer",
              padding: "10px",
              border: "1px solid #ccc",
              margin: "5px 0",
            }}
          >
            {title}
          </div>
        ))}
      </div>
    </div>
  );
};
