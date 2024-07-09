import axios from 'axios';

const API_BASE_URL = '/api'; // Adjust this based on your Django API endpoint

export async function fetchUserData() {
  try {
    const response = await axios.get(`${API_BASE_URL}/user/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user data:', error);
    throw error;
  }
}

export async function updateUserData(userData: any) {
  try {
    const response = await axios.post(`${API_BASE_URL}/user/update/`, userData);
    return response.data;
  } catch (error) {
    console.error('Error updating user data:', error);
    throw error;
  }
}
