import { SessionCreateResponse } from "@/models/api";
import { FormDto, StepDto } from "@/models/forms";

class FormApi {
  async createForm(title: string, description: string): Promise<FormDto> {
    const response = await fetch("http://localhost:4500/api/forms", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, description }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch form");
    }

    return response.json();
  }

  async createSession(formId: string): Promise<SessionCreateResponse> {
    const response = await fetch(
      `http://localhost:4500/api/forms/${formId}/session`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    return response.json();
  }

  async submitValues(
    formId: string,
    sessionId: string,
    values: Record<string, any>
  ): Promise<StepDto> {
    const response = await fetch(
      `http://localhost:4500/api/forms/${formId}/session/${sessionId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ values }),
      }
    );

    return response.json();
  }

  async getForms(): Promise<FormDto[]> {
    const response = await fetch("http://localhost:4500/api/forms");
    return response.json();
  }
}

export default new FormApi();
