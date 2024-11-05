import { ElementGroupDto } from "../elements";
import { DropdownElementDto } from "../elements/DropdownElementDto";
import { InputElementDto } from "../elements/InputElementDto";
import { TextElementDto } from "../elements/TextElementDto";

/**
 * Interface representing a form step containing various UI elements
 */
export interface StepDto {
  title: string;
  description: string;
  elements: Array<InputElementDto | TextElementDto | DropdownElementDto>;
  groups: Array<ElementGroupDto>;
  required_element_ids: Array<string>;
  is_final_step: boolean;
}
