import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';
import { TrendingUp, Loader2 } from 'lucide-react';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
    class_level: '',
    school_name: ''
  });
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleClassChange = (value) => {
    setFormData({
      ...formData,
      class_level: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await register(formData);
      toast.success('Registration successful! Welcome to BoatMyCareer.');
      navigate('/payment');
    } catch (error) {
      console.error('Registration error:', error);
      toast.error(error.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4 py-12">
      <Card className="card-base w-full max-w-2xl p-8">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center">
              <TrendingUp className="text-white" size={28} />
            </div>
            <span className="text-2xl font-heading font-bold text-primary">BoatMyCareer</span>
          </div>
          <h1 className="text-2xl font-heading font-bold text-primary mb-2">Start Your Career Journey</h1>
          <p className="text-gray-600">Create your account to access the assessment</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="full_name">Full Name *</Label>
              <Input
                id="full_name"
                name="full_name"
                type="text"
                placeholder="Enter your full name"
                value={formData.full_name}
                onChange={handleChange}
                required
                data-testid="register-name-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email Address *</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="your@email.com"
                value={formData.email}
                onChange={handleChange}
                required
                data-testid="register-email-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number *</Label>
              <Input
                id="phone"
                name="phone"
                type="tel"
                placeholder="10-digit mobile number"
                value={formData.phone}
                onChange={handleChange}
                required
                data-testid="register-phone-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password *</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="Create a strong password"
                value={formData.password}
                onChange={handleChange}
                required
                minLength={6}
                data-testid="register-password-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="class_level">Class/Grade *</Label>
              <Select value={formData.class_level} onValueChange={handleClassChange} required>
                <SelectTrigger data-testid="register-class-select">
                  <SelectValue placeholder="Select your class" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="VII">Class VII</SelectItem>
                  <SelectItem value="VIII">Class VIII</SelectItem>
                  <SelectItem value="IX">Class IX</SelectItem>
                  <SelectItem value="X">Class X</SelectItem>
                  <SelectItem value="XI">Class XI</SelectItem>
                  <SelectItem value="XII">Class XII</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="school_name">School Name *</Label>
              <Input
                id="school_name"
                name="school_name"
                type="text"
                placeholder="Your school name"
                value={formData.school_name}
                onChange={handleChange}
                required
                data-testid="register-school-input"
              />
            </div>
          </div>

          <Button
            type="submit"
            className="w-full bg-accent hover:bg-accent/90 py-6 text-lg"
            disabled={loading}
            data-testid="register-submit-btn"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Creating account...
              </>
            ) : (
              'Create Account & Proceed to Payment'
            )}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-primary font-semibold hover:underline" data-testid="login-link">
              Sign in here
            </Link>
          </p>
        </div>

        <div className="mt-8 pt-6 border-t border-black/5 text-center">
          <Link to="/" className="text-sm text-gray-600 hover:text-primary" data-testid="back-home-link">
            ← Back to Home
          </Link>
        </div>
      </Card>
    </div>
  );
}
