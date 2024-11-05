import { FormStep } from "@/components/organisms/form/FormStep";
import { useForm } from "@/hooks/session/useForm";

export const Form = () => {
  const { step, canSubmit } = useForm();

  if (!step) {
    return <p>Loading...</p>;
  }

  return <FormStep {...step} canSubmit={canSubmit} />;
};
