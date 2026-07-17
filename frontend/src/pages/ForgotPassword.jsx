import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { forgotPassword, resetPassword } from '../api';
import './ForgotPassword.css';

export default function ForgotPassword() {
  const navigate = useNavigate();

  // Step 1: Request token
  const [email, setEmail] = useState('');
  const [requestError, setRequestError] = useState(null);
  const [tokenReceived, setTokenReceived] = useState('');
  const [requesting, setRequesting] = useState(false);

  // Step 2: Reset password
  const [token, setToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [resetError, setResetError] = useState(null);
  const [resetSuccess, setResetSuccess] = useState('');
  const [resetting, setResetting] = useState(false);

  const handleRequestToken = async (e) => {
    e.preventDefault();
    setRequestError(null);
    setTokenReceived('');
    setRequesting(true);

    try {
      const result = await forgotPassword(email.trim());

      // Extract the token from the message
      const msg = result.message || '';
      const tokenMatch = msg.match(/([A-Za-z0-9_-]{30,})/);
      const extractedToken = tokenMatch ? tokenMatch[1] : '';

      setTokenReceived(extractedToken);
      // Auto-fill step 2
      setToken(extractedToken);
    } catch (err) {
      setRequestError(err.message);
    } finally {
      setRequesting(false);
    }
  };

  const copyToken = () => {
    navigator.clipboard.writeText(tokenReceived);
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setResetError(null);
    setResetSuccess('');

    if (!token.trim()) {
      setResetError('Please request a reset token first (Step 1)');
      return;
    }
    if (newPassword !== confirmPassword) {
      setResetError('Passwords do not match');
      return;
    }
    if (newPassword.length < 4) {
      setResetError('Password must be at least 4 characters');
      return;
    }

    setResetting(true);

    try {
      const result = await resetPassword(token.trim(), newPassword);
      setResetSuccess(result.message);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setResetError(err.message);
    } finally {
      setResetting(false);
    }
  };

  return (
    <div className="forgot-password-page">
      <div className="forgot-password-card">
        <div className="forgot-password-header">
          <h1>Forgot Password</h1>
          <p>Reset your password in two simple steps</p>
        </div>

        {/* Dev mode notice */}
        <div className="dev-notice">
          <strong>&#9432; Dev Mode:</strong> Tokens are displayed on-screen instead of being emailed.
        </div>

        {/* Step 1: Request reset token */}
        <div className="reset-step">
          <div className="step-badge">1</div>
          <h3>Enter your registered email</h3>
          <form className="reset-form" onSubmit={handleRequestToken}>
            {requestError && <div className="reset-error">{requestError}</div>}

            <div className="form-group">
              <label htmlFor="forgot-email">Email</label>
              <input
                id="forgot-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                autoFocus
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={requesting}
            >
              {requesting ? 'Sending...' : 'Send Reset Token'}
            </button>
          </form>

          {/* Token display area */}
          {tokenReceived && (
            <div className="token-display">
              <div className="token-label">Your Reset Token:</div>
              <div className="token-value">{tokenReceived}</div>
              <button type="button" className="btn btn-copy" onClick={copyToken}>
                Copy Token
              </button>
            </div>
          )}
        </div>

        <div className="step-divider">
          <span>then</span>
        </div>

        {/* Step 2: Enter token and new password */}
        <div className="reset-step">
          <div className="step-badge">2</div>
          <h3>Enter token & new password</h3>
          <form className="reset-form" onSubmit={handleResetPassword}>
            {resetError && <div className="reset-error">{resetError}</div>}
            {resetSuccess && <div className="reset-success">{resetSuccess}</div>}

            <div className="form-group">
              <label htmlFor="reset-token">Reset Token</label>
              <input
                id="reset-token"
                type="text"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder={tokenReceived ? 'Auto-filled from Step 1' : 'Paste the reset token here'}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="new-password">New Password</label>
              <input
                id="new-password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Min 4 characters"
                required
                minLength={4}
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirm-password">Confirm New Password</label>
              <input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter your new password"
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={resetting}
            >
              {resetting ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        </div>

        <div className="forgot-password-footer">
          <Link to="/login" className="back-link">&larr; Back to Login</Link>
        </div>
      </div>
    </div>
  );
}
