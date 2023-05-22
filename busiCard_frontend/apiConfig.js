let API_ENDPOINT = '';

if (process.env.NODE_ENV === 'production') {
  API_ENDPOINT = 'https://your-production-url.com';
} else {
  API_ENDPOINT = 'http://192.168.50.2:8000';
}

export const apiConfig = {
  API_ENDPOINT,
};