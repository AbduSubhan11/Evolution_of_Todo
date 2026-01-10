import { betterAuth } from 'better-auth';
import { jwt } from 'better-auth/plugins';

// Initialize Better Auth with proper configuration
export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || process.env.SECRET_KEY || 'your-better-auth-secret-change-this-in-production',
  trustHost: process.env.BETTER_AUTH_TRUST_HOST === 'true',
  database: {
    provider: 'sqlite',
    url: process.env.DATABASE_URL || './todo_app.db',
  },
  // Add JWT plugin for token generation
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET || process.env.SECRET_KEY || 'your-better-auth-secret-change-this-in-production',
    }),
  ],
  // Define user model
  user: {
    data: {
      email: 'email',
      name: 'string',
    },
  },
  // Session configuration
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
  // Account verification
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  // Social providers (optional)
  socialProviders: {
    // google: {
    //   clientId: process.env.GOOGLE_CLIENT_ID!,
    //   clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    // },
  },
});