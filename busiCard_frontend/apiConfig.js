let API_ENDPOINT = '';

if (process.env.NODE_ENV === 'production') {
  API_ENDPOINT = 'https://polls-service-n62funkaba-de.a.run.app';
} else {
  API_ENDPOINT = 'https://polls-service-n62funkaba-de.a.run.app';
}

export const apiConfig = {
  API_ENDPOINT,
};