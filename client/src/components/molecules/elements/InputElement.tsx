import { useForm } from "@/hooks/session/useForm";
import { InputElementDto } from "@/models/elements";

interface InputElementProps extends InputElementDto {}

export const InputElement = ({
  id,
  placeholder,
  multiline,
  input_type,
  is_sensitive,
}: InputElementProps) => {
  const { setValue } = useForm();

  return (
    <div className="form-element">
      {!multiline && (
        <input
          type={is_sensitive ? "password" : input_type}
          id={id}
          placeholder={placeholder}
          onChange={(e) => setValue(id, e.target.value)}
        />
      )}
      {multiline && (
        <textarea
          id={id}
          placeholder={placeholder}
          onChange={(e) => setValue(id, e.target.value)}
        />
      )}
    </div>
  );
};
