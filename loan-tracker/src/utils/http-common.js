import axios from "axios";



// const token = sessionStorage.getItem('token');
const createApiClient = () => {
  

  const apiClient = axios.create({
    baseURL: 'https://loan-tracker-two.vercel.app/api/',

  });

  apiClient.interceptors.request.use(
    config => {
      const token = sessionStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    error => {
      return Promise.reject(error);
    }
  );
  
  // Response interceptor to handle token refresh
  apiClient.interceptors.response.use(
    response => {
      return response;
    },
    async error => {
      const originalRequest = error.config;
      
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        
        try {
          const refreshToken = sessionStorage.getItem('refreshToken');
          const response = await axios.post('http://127.0.0.1:8000/api/users/refresh/', { refresh: refreshToken });

  
          const access  = response.data.access;
          const  refresh  = response.data.refresh;
          sessionStorage.setItem('token', access);
          sessionStorage.setItem('refreshToken', refresh);
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          originalRequest.headers['Authorization'] = `Bearer ${access}`;
  
          return apiClient(originalRequest);
        } catch (refreshError) {
          // Handle refresh token failure, like redirecting to login
          return Promise.reject(refreshError);
        }
      }
      
      return Promise.reject(error);
    }
  );
  

  // apiClient.interceptors.response.use(
  //   (response) => response,
  //   async (error) => {
  //     const originalRequest = error.config;
  //     if (error.response.statusText === "Unauthorized" && !originalRequest._retry) {
  //       originalRequest._retry = true;
  //       try {
  //         const { accessToken } = await refreshToken();
  //         apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
  //         originalRequest.headers['Authorization'] = `Bearer ${accessToken}`;
  //         return apiClient(originalRequest);
  //       } catch (refreshError) {
  //         console.error('Token refresh failed:', refreshError);
  //         // Handle failed refresh (e.g., redirect to login)
  //         throw refreshError;
  //       }
  //     }
  //     return Promise.reject(error);
  //   }
  // );

  return apiClient;
};

export default createApiClient();
