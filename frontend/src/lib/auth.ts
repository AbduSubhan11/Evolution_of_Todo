/**
 * Get access token for authenticated requests
 * This integrates with better-auth
 */

export const getAccessToken = async (): Promise<string> => {
  try {
    // With better-auth, we typically get the token from cookies or localStorage
    // depending on how it's configured. Usually, better-auth manages this automatically.

    // In a better-auth setup, we might check for the presence of auth cookies
    // or call an API to verify the session
    const response = await fetch('/api/auth/session'); // or wherever better-auth exposes session

    if (response.ok) {
      const session = await response.json();
      return session.token || session.accessToken || '';
    }

    return '';
  } catch (error) {
    console.error('Error getting access token:', error);
    return '';
  }
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = async (): Promise<boolean> => {
  try {
    const token = await getAccessToken();
    return token !== '' && token !== undefined && token !== null;
  } catch (error) {
    console.error('Error checking authentication:', error);
    return false;
  }
};