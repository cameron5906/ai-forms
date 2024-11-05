import { TextElementDto } from "@/models/elements";
import React from "react"; // Import React to avoid UMD global error

interface TextElementProps extends TextElementDto {}

/**
 * TextElement component that displays text with line breaks.
 * This component replaces newline characters with <br /> elements.
 * @param {TextElementProps} props - The properties for the TextElement.
 * @returns {JSX.Element} The rendered TextElement component.
 */
export const TextElement = ({ id, label, text, size }: TextElementProps) => {
  // First replace literal '\n' with actual newlines, then split
  const processedText = text.replace(/\\n/g, "\n");

  return (
    <div className={`text-element ${size}`}>
      {processedText.split(/\r?\n/).map((line, index) => (
        <React.Fragment key={index}>
          {line}
          <br />
        </React.Fragment>
      ))}
    </div>
  );
};
