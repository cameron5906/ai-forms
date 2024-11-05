import { useForm } from "@/hooks/session/useForm";
import { BooleanElementDto } from "@/models/elements";

interface BooleanElementProps extends BooleanElementDto {}

export const BooleanElement = ({
  default_checked,
  ...props
}: BooleanElementProps) => {
  const { setValue } = useForm();

  return (
    <div className="form-element checkbox-element">
      <input
        type="checkbox"
        id={props.id}
        defaultChecked={default_checked}
        onChange={(e) => setValue(props.id, e.target.checked)}
      />
      <label htmlFor={props.id}>{props.label}</label>
    </div>
  );
};
