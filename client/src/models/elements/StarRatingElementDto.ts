import { BaseElementDto } from "./BaseElementDto";

export interface StarRatingElementDto extends BaseElementDto {
  min_rating: number;
  max_rating: number;
}
