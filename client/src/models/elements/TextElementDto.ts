import { BaseElementDto } from "./BaseElementDto";
import { ElementType } from "./ElementType";

/**
 * Interface representing a paragraph of text on the UI
 */
export interface TextElementDto extends BaseElementDto {
  element_type: ElementType.TEXT;
  text: string;
  size: "sm" | "md" | "lg";
}
