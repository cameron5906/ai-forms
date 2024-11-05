import { ElementType } from "./ElementType";

/**
 * Base interface for all UI elements
 */
export interface BaseElementDto {
  element_type: ElementType;
  id: string;
  label: string;
}
