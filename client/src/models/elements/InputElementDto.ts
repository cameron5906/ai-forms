import { BaseElementDto } from "./BaseElementDto";
import { ElementType, InputType } from "./ElementType";

/**
 * Interface representing an input field on the UI
 */
export interface InputElementDto extends BaseElementDto {
  element_type: ElementType.INPUT;
  input_type: InputType;
  multiline: boolean;
  placeholder?: string;
  value?: string;
  is_sensitive: boolean;
}
