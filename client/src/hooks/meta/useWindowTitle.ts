import { useEffect } from "react";

export const useWindowTitle = (title: string) => {
  useEffect(() => {
    document.title = title;
  }, [title]);
};
