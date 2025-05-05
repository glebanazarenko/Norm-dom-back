import axios from 'axios';

// Get houses by search query
export const searchHouses = async (query: string) => {
  try {
    const response = await axios.get(`/houses/search?query=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    console.error('Error searching houses:', error);
    throw error;
  }
};

// Get house details by ID
export const getHouseById = async (id: string) => {
  try {
    const response = await axios.get(`/house/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching house details:', error);
    throw error;
  }
};

// Add review to house
export const addReviewToHouse = async (houseId: string, reviewText: string, rating: number) => {
  try {
    const response = await axios.post(`/house/${houseId}/reviews`, {
      review_text: reviewText,
      rating
    });
    return response.data;
  } catch (error) {
    console.error('Error adding review:', error);
    throw error;
  }
};

// Edit review (for super users)
export const editReview = async (reviewId: string, newRating: number, newReviewText: string) => {
  try {
    const response = await axios.post('/review/edit', {
      review_id: reviewId,
      new_rating: newRating,
      new_review_text: newReviewText
    });
    return response.data;
  } catch (error) {
    console.error('Error editing review:', error);
    throw error;
  }
};