import axios from 'axios';

// Download data
export const downloadData = async (formData: FormData) => {
  const response = await axios.post('/admin/download', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Upload data
export const uploadData = async () => {
  try {
    const response = await axios.post('/admin/upload');
    return response.data;
  } catch (error) {
    console.error('Error uploading data:', error);
    throw error;
  }
};

// Update houses
export const updateHouses = async () => {
  try {
    const response = await axios.post('/admin/update-houses');
    return response.data;
  } catch (error) {
    console.error('Error updating houses:', error);
    throw error;
  }
};

// Moderate review
export const moderateReview = async (reviewId: string, action: 'approve' | 'reject') => {
  try {
    const response = await axios.post('/review/moderate', {
      review_id: reviewId,
      action
    });
    return response.data;
  } catch (error) {
    console.error('Error moderating review:', error);
    throw error;
  }
};

export const getAdminStats = async () => {
  const response = await axios.get('/admin/stats');
  return response.data;
};