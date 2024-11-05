import FormApi from "@/api/FormApi";
import { FormDto } from "@/models/forms";
import { createContext, useEffect, useState } from "react";

type Context = {
  forms: FormDto[];
  reload: () => void;
};

const defaultContext: Context = {
  forms: [],
  reload: () => {},
};

export const FormsContext = createContext<Context>(defaultContext);

interface ProviderProps {
  children: React.ReactNode;
}

export const FormsProvider: React.FC<ProviderProps> = ({ children }) => {
  const [forms, setForms] = useState<FormDto[]>([]);

  useEffect(() => {
    handleLoadForms();
  }, []);

  const handleLoadForms = async () => {
    const forms = await FormApi.getForms();
    setForms(forms);
  };

  return (
    <FormsContext.Provider value={{ forms, reload: handleLoadForms }}>
      {children}
    </FormsContext.Provider>
  );
};
