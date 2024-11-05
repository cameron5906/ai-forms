import { StepDto } from "../forms";

export interface SessionCreateResponse {
  session_id: string;
  step: StepDto;
}
