import { FormElement } from "@/components/molecules/elements/FormElement";
import { ElementGroup } from "./ElementGroup";
import { StepDto } from "@/models/forms";
import { useForm } from "@/hooks/session/useForm";
import { memo } from "react";
import { LoadingButton } from "@/components/atoms/inputs/LoadingButton";

interface FormStepProps extends StepDto {
  canSubmit: boolean;
}

export const FormStep = memo(
  ({
    title,
    description,
    elements,
    groups = [],
    canSubmit,
    is_final_step,
    ...props
  }: FormStepProps) => {
    const { submit, isLoading } = useForm();

    // Get IDs of all elements that are part of groups
    const groupedElementIds = groups.flatMap((group) => group.element_ids);

    // Filter out elements that are not in any group
    const ungroupedElements = elements.filter(
      (element) => !groupedElementIds.includes(element.id)
    );

    return (
      <div className="form-step" style={{ position: "relative" }}>
        <h2 className="step-title">{title}</h2>
        <p className="step-description">{description}</p>
        {/* Render grouped elements */}
        {groups
          .sort((a, b) => a.order - b.order)
          .map((group) => (
            <ElementGroup
              key={group.element_ids.join("-")}
              {...group}
              step={{
                title,
                description,
                elements,
                groups,
                is_final_step,
                ...props,
              }}
            />
          ))}

        {/* Render ungrouped elements */}
        {ungroupedElements.map((element) => (
          <FormElement key={element.id} {...element} />
        ))}

        {!is_final_step && (
          <div className="submit-button-container">
            <LoadingButton
              className="submit-button"
              disabled={!canSubmit || isLoading}
              onClick={submit}
              loading={isLoading}
            >
              Continue
            </LoadingButton>
          </div>
        )}
      </div>
    );
  }
);
