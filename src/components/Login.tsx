import { useState } from 'react';
import { Mail, Lock, UserCircle, ArrowLeft, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import { User, UserRole } from '../App';

interface LoginProps {
  onLogin: (user: User) => void;
  onBack?: () => void;
}

const API_BASE = 'http://localhost:8000/api';

export function Login({ onLogin, onBack }: LoginProps) {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState<UserRole>('student');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userNotFound, setUserNotFound] = useState(false);

  const handleBack = () => {
    // Use browser history to go back
    if (window.history.length > 1) {
      window.history.back();
    } else if (onBack) {
      onBack();
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setUserNotFound(false);
    setIsLoading(true);

    try {
      // Try to get authentication token from backend
      const response = await fetch(`${API_BASE}/auth/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_or_username: email, password }),
      });

      if (!response.ok) {
        // Try to get error message from backend
        let errorMsg = 'Authentication failed. Please try again.';
        try {
          const errorData = await response.json();
          errorMsg = errorData.error || errorMsg;
        } catch (e) {
          // If we can't parse JSON, use status-based message
          if (response.status === 401) {
            errorMsg = 'Invalid email or password';
          }
        }
        
        if (response.status === 401) {
          setUserNotFound(true);
        }
        setError(errorMsg);
        setIsLoading(false);
        console.error('Login error:', response.status, errorMsg);
        return;
      }

      const data = await response.json();
      const token = data.token;

      // Save token to localStorage
      localStorage.setItem('authToken', token);

      // Get user profile details
      const profileResponse = await fetch(`${API_BASE}/users/me/`, {
        headers: { 'Authorization': `Token ${token}` },
      });

      if (profileResponse.ok) {
        const userProfile = await profileResponse.json();
        
        const user: User = {
          id: String(userProfile.id),
          email: userProfile.email,
          name: userProfile.first_name && userProfile.last_name 
            ? `${userProfile.first_name} ${userProfile.last_name}`
            : userProfile.username,
          role: userProfile.profile?.role || 'student',
        };

        onLogin(user);
      } else {
        setError('Failed to load user profile');
        localStorage.removeItem('authToken');
        console.error('Profile load failed:', profileResponse.status);
      }
    } catch (err) {
      setError('Network error. Please check if backend is running on http://localhost:8000. Error: ' + String(err));
      console.error('Login error:', err);
    }

    setIsLoading(false);
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    try {
      // First, create the user via Django
      const createResponse = await fetch(`${API_BASE}/users/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: email,
          email: email,
          password: password,
          first_name: name.split(' ')[0],
          last_name: name.split(' ').slice(1).join(' ') || '',
        }),
      });

      if (!createResponse.ok) {
        const errorData = await createResponse.json();
        setError(
          errorData.email?.[0] || 
          errorData.username?.[0] || 
          'Failed to create account. Email might already be registered.'
        );
        setIsLoading(false);
        return;
      }

      // Now set the user role in profile
      const userData = await createResponse.json();
      const profileUpdateResponse = await fetch(`${API_BASE}/profiles/${userData.id}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: role }),
      });

      if (!profileUpdateResponse.ok) {
        console.error('Failed to update profile role');
      }

      setSuccess('Account created successfully! Please log in with your new account.');
      setIsSignup(false);
      setEmail('');
      setPassword('');
      setName('');
      setIsLoading(false);
    } catch (err) {
      setError('Network error. Please check if backend is running.');
      console.error('Signup error:', err);
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    if (isSignup) {
      handleSignup(e);
    } else {
      handleLogin(e);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Back Button */}
        <button
          onClick={handleBack}
          className="flex items-center gap-2 text-white/80 hover:text-white mb-6 font-medium transition"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Home
        </button>

        {/* Logo/Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-500 rounded-2xl mb-4">
            <UserCircle className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">PRIME</h1>
          <p className="text-slate-300">College-First Code & Project Collaboration Platform</p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-slate-800 mb-2">
              {isSignup ? 'Create Account' : 'Welcome Back'}
            </h2>
            <p className="text-slate-600">
              {isSignup ? 'Sign up to get started' : 'Sign in to continue'}
            </p>
          </div>

          {/* Success Message */}
          {success && (
            <div className="mb-4 bg-green-50 border border-green-200 rounded-lg p-4 flex gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-green-800 text-sm">{success}</p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-red-800 text-sm font-medium">{error}</p>
                  
                  {/* Show signup suggestion if user not found */}
                  {userNotFound && !isSignup && (
                    <button
                      onClick={() => {
                        setIsSignup(true);
                        setError('');
                        setUserNotFound(false);
                        setPassword('');
                        setName('');
                      }}
                      className="mt-2 text-red-700 hover:text-red-800 underline text-sm font-medium"
                    >
                      Create a new account instead
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {isSignup && (
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Full Name
                </label>
                <div className="relative">
                  <UserCircle className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                    placeholder="John Doe"
                    required={isSignup}
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                  placeholder="you@university.edu"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                I am a
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setRole('student')}
                  className={`py-3 px-4 rounded-lg border-2 font-medium transition ${
                    role === 'student'
                      ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                      : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400'
                  }`}
                >
                  Student
                </button>
                <button
                  type="button"
                  onClick={() => setRole('faculty')}
                  className={`py-3 px-4 rounded-lg border-2 font-medium transition ${
                    role === 'faculty'
                      ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                      : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400'
                  }`}
                >
                  Faculty
                </button>
              </div>
              
              {/* Hidden admin access - type 'admin' in email to enable */}
              {email.toLowerCase().includes('admin') && (
                <button
                  type="button"
                  onClick={() => setRole('admin')}
                  className={`mt-3 w-full py-3 px-4 rounded-lg border-2 font-medium transition ${
                    role === 'admin'
                      ? 'border-purple-500 bg-purple-50 text-purple-700'
                      : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400'
                  }`}
                >
                  Admin Access
                </button>
              )}
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 transition shadow-lg shadow-indigo-500/30 disabled:bg-indigo-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isLoading && <Loader className="w-5 h-5 animate-spin" />}
              {isSignup ? 'Sign Up' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => {
                setIsSignup(!isSignup);
                setError('');
                setSuccess('');
                setUserNotFound(false);
              }}
              className="text-indigo-600 hover:text-indigo-700 font-medium"
            >
              {isSignup
                ? 'Already have an account? Sign In'
                : "Don't have an account? Sign Up"}
            </button>
          </div>
        </div>

        <p className="text-center text-slate-400 mt-6 text-sm">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}