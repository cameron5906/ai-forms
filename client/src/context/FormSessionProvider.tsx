import { FormApi } from "@/api";
import { ElementType } from "@/models/elements";
import { StepDto } from "@/models/forms";
import { createContext, useEffect, useMemo, useState } from "react";
import { BaseElementDto } from "@/models/elements";
import { useWindowTitle } from "@/hooks/meta";

type Context = {
  step: StepDto | null;
  canSubmit: boolean;
  isLoading: boolean;
  setValue: (id: string, value: any) => void;
  submit: () => Promise<void>;
};

const defaultContext: Context = {
  step: null,
  canSubmit: false,
  isLoading: false,
  setValue: () => {},
  submit: async () => {},
};

export const FormSessionContext = createContext<Context>(defaultContext);

interface ProviderProps {
  formId: string;
  children: React.ReactNode;
}

export const FormSessionProvider: React.FC<ProviderProps> = ({
  formId,
  children,
}) => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [step, setStep] = useState<StepDto | null>(null);
  const [values, setValues] = useState<Record<string, any>>({});
  const [isLoading, setIsLoading] = useState(false);
  useWindowTitle(step?.title || "Loading...");

  const areRequiredFieldsSet = useMemo(() => {
    if (!step) {
      return false;
    }

    return step.elements
      .filter(
        (e) =>
          step.required_element_ids.includes(e.id) &&
          (e as BaseElementDto).element_type !== ElementType.BOOLEAN
      )
      .every((e) => typeof values[e.id] !== "undefined");
  }, [step, values]);

  useEffect(() => {
    FormApi.createSession(formId).then((res) => {
      setSessionId(res.session_id);
      setStep(res.step);
    });
  }, [formId]);

  const setValue = (id: string, value: any) => {
    setValues((prev) => ({ ...prev, [id]: value }));
  };

  const submit = async () => {
    if (!sessionId) {
      return;
    }

    setIsLoading(true);
    const newStep = await FormApi.submitValues(formId, sessionId, values);
    setStep(newStep);
    setIsLoading(false);
  };

  return (
    <FormSessionContext.Provider
      value={{
        step,
        canSubmit: areRequiredFieldsSet,
        isLoading,
        setValue,
        submit,
      }}
    >
      {children}
    </FormSessionContext.Provider>
  );
};
