import { StepDto } from "@/models/forms";
import { ElementGroupDto } from "@/models/elements";
import { FormElement } from "@/components/molecules/elements/FormElement";

/**
 * Interface for ElementGroup props extending ElementGroupDto
 * and including the parent Step for context
 */
interface ElementGroupProps extends ElementGroupDto {
  step: StepDto;
}

/**
 * Component that renders a group of form elements in either vertical or horizontal layout
 */
export const ElementGroup = ({
  step,
  element_ids,
  grouping_type,
  order,
}: ElementGroupProps) => {
  // Find all elements that belong to this group
  const groupElements = element_ids
    .map((id) => step.elements.find((element) => element.id === id))
    .filter((element) => element !== undefined);

  // Find all required elements that belong to this group
  const requiredElements = groupElements.filter((element) =>
    step.required_element_ids.includes(element.id)
  );

  return (
    <div
      className={`element-group ${grouping_type}`}
      style={{
        display: "flex",
        flexDirection: grouping_type === "vertical" ? "column" : "row",
        gap: "1rem",
        width: "100%",
      }}
    >
      {groupElements.map(
        (element) =>
          element && (
            <FormElement
              key={element.id}
              {...element}
              required={requiredElements.some(
                (required) => required.id === element.id
              )}
            />
          )
      )}
    </div>
  );
};
