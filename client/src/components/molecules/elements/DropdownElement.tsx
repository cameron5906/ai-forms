import { useForm } from "@/hooks/session/useForm";
import { DropdownElementDto } from "@/models/elements";

interface DropdownElementProps extends DropdownElementDto {}

export const DropdownElement = ({
  id,
  label,
  options,
}: DropdownElementProps) => {
  const { setValue } = useForm();

  return (
    <div className="form-element">
      <select id={id} onChange={(e) => setValue(id, e.target.value)}>
        <option value="">Select an option</option>
        {options.map((option, index) => (
          <option key={index} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
};
