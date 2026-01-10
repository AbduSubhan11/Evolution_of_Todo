import { NextRequest, NextResponse } from 'next/server';

// Define protected routes that require authentication
const protectedRoutes = ['/', '/dashboard', '/tasks', '/profile', '/settings'];

export function middleware(request: NextRequest) {
  // Get the Better Auth session token from cookies
  // Better Auth stores the session in a cookie named '_session'
  const sessionCookie = request.cookies.get('_session')?.value;

  // Check if the current path is a protected route
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname === route
  );

  // Check if the user is trying to access auth pages while logged in
  const isAuthPage = request.nextUrl.pathname.startsWith('/login') ||
                     request.nextUrl.pathname.startsWith('/register');

  // If user is on a protected route but not authenticated
  if (isProtectedRoute && !sessionCookie) {
    // Redirect to login page
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // If user is already logged in but trying to access auth pages, redirect to home
  if (isAuthPage && sessionCookie) {
    return NextResponse.redirect(new URL('/', request.url));
  }

  // Allow the request to continue
  return NextResponse.next();
}

// Apply middleware to specific paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};