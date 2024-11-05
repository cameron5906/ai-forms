import { useForm } from "@/hooks/session/useForm";
import { StarRatingElementDto } from "@/models/elements/StarRatingElementDto";
import { useEffect, useState } from "react";

interface StarRatingElementProps extends StarRatingElementDto {}

/**
 * StarRatingElement Component
 * Displays an interactive or readonly star rating system
 */
const StarRatingElement = ({ id, max_rating = 5 }: StarRatingElementProps) => {
  const { setValue } = useForm();
  const [rating, setRating] = useState<number>(0);
  const [hover, setHover] = useState<number>(0);

  const handleClick = (value: number) => {
    setRating(value);
  };

  useEffect(() => {
    if (rating === 0) return;

    setValue(id, rating);
  }, [rating]);

  return (
    <div className="star-rating">
      {[...Array(max_rating)].map((_, index) => {
        const starValue = index + 1;
        return (
          <span
            key={index}
            className={`star ${starValue <= (hover || rating) ? "filled" : ""}`}
            onClick={() => handleClick(starValue)}
            onMouseEnter={() => setHover(starValue)}
            onMouseLeave={() => setHover(0)}
            role="presentation"
          >
            {/* Add your star icon here */}
          </span>
        );
      })}
    </div>
  );
};

export default StarRatingElement;
