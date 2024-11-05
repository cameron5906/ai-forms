import "./App.css";
import { Builder } from "@views/builder";
import { FormsProvider } from "./context/FormsProvider";
import { useState } from "react";
import { FormSessionProvider } from "./context/FormSessionProvider";
import { Form } from "@views/form";

function App() {
  const [selectedFormId, setSelectedFormId] = useState<string | null>(null);

  if (selectedFormId) {
    return (
      <FormSessionProvider formId={selectedFormId}>
        <Form />
      </FormSessionProvider>
    );
  }

  return (
    <>
      <FormsProvider>
        <Builder onFormSelected={setSelectedFormId} />
      </FormsProvider>
    </>
  );
}

export default App;
