import { FormsContext } from "@/context/FormsProvider";
import { useContext } from "react";

export const useForms = () => {
  const { forms, reload } = useContext(FormsContext);
  return { forms, reload };
};
