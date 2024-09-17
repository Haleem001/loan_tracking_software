import axios from 'axios';

const refreshToken = async () => {
  const currentRefreshToken = sessionStorage.getItem('refreshToken');
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/users/refresh/', {
      refresh: currentRefreshToken
    });
    sessionStorage.setItem('token', response.data.access);
    sessionStorage.setItem('refreshToken', response.data.refresh);
    return {
      accessToken: response.data.access,
      refreshToken: response.data.refresh
    };
  } catch (error) {
    console.error('Error refreshing token:', error);
    throw error;
  }
};

export default refreshToken;
