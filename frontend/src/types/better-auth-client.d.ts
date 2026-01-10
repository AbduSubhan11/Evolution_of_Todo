declare module '@better-auth/client' {
  export interface CreateAuthClientOptions {
    baseURL?: string;
    fetchOptions?: any;
  }

  export interface SignInResult {
    data?: any;
    error?: {
      message: string;
      code?: string;
    };
  }

  export interface SignUpResult {
    data?: any;
    error?: {
      message: string;
      code?: string;
    };
  }

  export interface SessionResult {
    data?: {
      user: any;
      session: any;
    } | null;
    error?: any;
  }

  export interface AuthClient {
    signIn: {
      email: (params: { email: string; password: string; callbackURL?: string }) => Promise<SignInResult>;
    };
    signUp: {
      email: (params: { email: string; password: string; name?: string }) => Promise<SignUpResult>;
    };
    signOut: () => Promise<{ error?: any }>;
    getSession: () => Promise<SessionResult>;
  }

  export function createAuthClient(opts?: CreateAuthClientOptions): AuthClient;
  export default createAuthClient;
}



