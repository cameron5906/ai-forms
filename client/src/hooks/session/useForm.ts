import { FormSessionContext } from "@/context/FormSessionProvider";
import { useContext } from "react";

export const useForm = () => {
  const { step, canSubmit, isLoading, setValue, submit } =
    useContext(FormSessionContext);

  return { step, canSubmit, isLoading, setValue, submit };
};
