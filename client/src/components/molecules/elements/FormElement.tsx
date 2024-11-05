import { BaseElementDto } from "@/models/elements/BaseElementDto";
import { DropdownElement } from "./DropdownElement";
import {
  BooleanElementDto,
  DropdownElementDto,
  ElementType,
  InputElementDto,
  TextElementDto,
} from "@/models/elements";
import { InputElement } from "./InputElement";
import { TextElement } from "./TextElement";
import { BooleanElement } from "./BooleanElement";
import { useMemo } from "react";
import StarRatingElement from "./StarRatingElement";
import { StarRatingElementDto } from "@/models/elements/StarRatingElementDto";

interface FormElementProps extends BaseElementDto {
  required?: boolean;
}

export const FormElement = ({
  element_type,
  id,
  label,
  required,
  ...props
}: FormElementProps) => {
  const elementToRender = useMemo(() => {
    const baseProps = { id, label };

    const element = (() => {
      switch (element_type) {
        case ElementType.TEXT:
          return <TextElement {...baseProps} {...(props as TextElementDto)} />;
        case ElementType.INPUT:
          return (
            <InputElement {...baseProps} {...(props as InputElementDto)} />
          );
        case ElementType.DROPDOWN:
          return (
            <DropdownElement
              {...baseProps}
              {...(props as DropdownElementDto)}
            />
          );
        case ElementType.BOOLEAN:
          return (
            <BooleanElement {...baseProps} {...(props as BooleanElementDto)} />
          );
        case ElementType.STAR_RATING:
          return (
            <StarRatingElement
              {...baseProps}
              {...(props as StarRatingElementDto)}
            />
          );
        default:
          return null;
      }
    })();

    // Boolean elements handle their own label
    if (element_type === ElementType.BOOLEAN) {
      return element;
    }

    // Wrap other elements with a label
    return (
      <div
        className="form-element"
        style={{ display: "flex", flexDirection: "column", gap: "8px" }}
      >
        <label htmlFor={id}>
          {label} {required && <span style={{ color: "red" }}>*</span>}
        </label>
        {element}
      </div>
    );
  }, [element_type, id, label, props]);

  return elementToRender;
};
