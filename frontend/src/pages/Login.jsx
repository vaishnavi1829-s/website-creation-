import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login, register } from '../api';
import './Login.css';

export default function Login() {
  const navigate = useNavigate();
  const [mode, setMode] = useState('login'); // 'login' | 'register'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      if (mode === 'register') {
        await register({
          username: username.trim(),
          password,
          full_name: fullName.trim() || undefined,
          email: email.trim() || undefined,
        });
        // Auto-login after register
        await login({ username: username.trim(), password });
      } else {
        await login({ username: username.trim(), password });
      }
      navigate('/my-bookings');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <h1>{mode === 'login' ? 'Welcome Back' : 'Create Account'}</h1>
          <p>{mode === 'login' ? 'Sign in to view your bookings' : 'Join to save your bookings'}</p>
        </div>

        <div className="login-tabs">
          <button
            className={`login-tab ${mode === 'login' ? 'active' : ''}`}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            className={`login-tab ${mode === 'register' ? 'active' : ''}`}
            onClick={() => setMode('register')}
          >
            Register
          </button>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          {error && <div className="login-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
              autoFocus
            />
          </div>

          {mode === 'register' && (
            <>
              <div className="form-group">
                <label htmlFor="fullName">Full Name (optional)</label>
                <input
                  id="fullName"
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="John Doe"
                />
              </div>
              <div className="form-group">
                <label htmlFor="email">Email (optional)</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="john@example.com"
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-block"
            disabled={submitting}
          >
            {submitting
              ? (mode === 'login' ? 'Signing in...' : 'Creating account...')
              : (mode === 'login' ? 'Sign In' : 'Create Account')}
          </button>

          {mode === 'login' && (
            <div className="forgot-password-link">
              <Link to="/forgot-password">Forgot your password?</Link>
            </div>
          )}
        </form>

        <div className="login-footer">
          <Link to="/" className="back-link">&larr; Back to Movies</Link>
        </div>
      </div>

      {/* Test accounts info */}
      <div className="test-accounts">
        <h3>Sample Test Accounts</h3>
        <div className="test-accounts-grid">
          <div className="test-account">
            <strong>john</strong> / password123
          </div>
          <div className="test-account">
            <strong>jane</strong> / password123
          </div>
          <div className="test-account">
            <strong>alice</strong> / password123
          </div>
          <div className="test-account">
            <strong>bob</strong> / password123
          </div>
          <div className="test-account">
            <strong>test</strong> / test
          </div>
        </div>
      </div>
    </div>
  );
}
