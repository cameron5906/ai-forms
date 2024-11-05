import { BaseElementDto } from "./BaseElementDto";
import { ElementType } from "./ElementType";

/**
 * Interface representing a dropdown menu on the UI
 */
export interface DropdownElementDto extends BaseElementDto {
  element_type: ElementType.DROPDOWN;
  options: string[];
  placeholder?: string;
  allow_multiple: boolean;
  values?: string[];
}
