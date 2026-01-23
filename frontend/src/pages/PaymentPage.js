import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';
import axios from 'axios';
import { TrendingUp, CheckCircle, Copy, Loader2 } from 'lucide-react';

const API_URL = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function PaymentPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [programType, setProgramType] = useState('psychometric_test');
  const [utrNumber, setUtrNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const upiId = 'shubhamrajsingh1712-1@okaxis';

  const amount = programType === 'psychometric_test' ? 999 : 1000;

  const handleCopyUPI = () => {
    navigator.clipboard.writeText(upiId);
    toast.success('UPI ID copied to clipboard!');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!utrNumber.trim()) {
      toast.error('Please enter the UTR/Transaction ID');
      return;
    }

    setLoading(true);

    try {
      await axios.post(`${API_URL}/payments`, {
        user_id: user.id,
        program_type: programType,
        amount: amount,
        utr_number: utrNumber
      });

      toast.success('Payment details submitted! We will verify and activate your account within 24 hours.');
      navigate('/dashboard');
    } catch (error) {
      console.error('Payment submission error:', error);
      toast.error('Failed to submit payment details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <nav className="bg-white border-b border-black/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white" size={24} />
              </div>
              <span className="text-xl font-heading font-bold text-primary">BoatMyCareer</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
            Complete Your Payment
          </h1>
          <p className="text-lg text-gray-600">Choose your program and make payment via UPI</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Payment Options */}
          <Card className="card-base p-8">
            <h2 className="text-xl font-heading font-semibold mb-6">Select Program</h2>
            
            <RadioGroup value={programType} onValueChange={setProgramType} className="space-y-4">
              <div className="flex items-start space-x-3 p-4 border-2 border-primary rounded-lg cursor-pointer">
                <RadioGroupItem value="psychometric_test" id="test" data-testid="program-test-radio" />
                <div className="flex-1">
                  <Label htmlFor="test" className="cursor-pointer font-semibold text-lg">Psychometric Assessment</Label>
                  <p className="text-sm text-gray-600 mt-1">Complete career discovery with report & counselling</p>
                  <p className="text-2xl font-bold text-primary mt-2">₹999</p>
                </div>
              </div>

              <div className="flex items-start space-x-3 p-4 border-2 border-accent rounded-lg cursor-pointer">
                <RadioGroupItem value="extended_program" id="extended" data-testid="program-extended-radio" />
                <div className="flex-1">
                  <Label htmlFor="extended" className="cursor-pointer font-semibold text-lg">Extended Guidance Program</Label>
                  <p className="text-sm text-gray-600 mt-1">1-year continuous career support & mentorship</p>
                  <p className="text-2xl font-bold text-accent mt-2">₹1,000</p>
                </div>
              </div>
            </RadioGroup>
          </Card>

          {/* Payment Instructions */}
          <Card className="card-base p-8">
            <h2 className="text-xl font-heading font-semibold mb-6">Payment Instructions</h2>
            
            <div className="space-y-6">
              <div>
                <Label className="text-sm font-medium mb-2 block">1. UPI ID</Label>
                <div className="flex items-center space-x-2">
                  <Input 
                    value={upiId} 
                    readOnly 
                    className="flex-1 bg-subtle" 
                    data-testid="upi-id-display"
                  />
                  <Button 
                    type="button" 
                    variant="outline" 
                    size="icon"
                    onClick={handleCopyUPI}
                    data-testid="copy-upi-btn"
                  >
                    <Copy size={18} />
                  </Button>
                </div>
              </div>

              <div>
                <Label className="text-sm font-medium mb-2 block">2. Amount to Pay</Label>
                <div className="text-3xl font-bold text-primary">₹{amount}</div>
              </div>

              <div className="bg-subtle rounded-lg p-4 space-y-2 text-sm">
                <p className="flex items-start space-x-2">
                  <CheckCircle size={18} className="text-secondary flex-shrink-0 mt-0.5" />
                  <span>Open any UPI app (Google Pay, PhonePe, Paytm, etc.)</span>
                </p>
                <p className="flex items-start space-x-2">
                  <CheckCircle size={18} className="text-secondary flex-shrink-0 mt-0.5" />
                  <span>Enter the UPI ID and amount</span>
                </p>
                <p className="flex items-start space-x-2">
                  <CheckCircle size={18} className="text-secondary flex-shrink-0 mt-0.5" />
                  <span>Complete the payment</span>
                </p>
                <p className="flex items-start space-x-2">
                  <CheckCircle size={18} className="text-secondary flex-shrink-0 mt-0.5" />
                  <span>Copy the UTR/Transaction ID from your payment app</span>
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4 pt-4">
                <div className="space-y-2">
                  <Label htmlFor="utr">3. Enter UTR/Transaction ID *</Label>
                  <Input
                    id="utr"
                    type="text"
                    placeholder="Enter 12-digit UTR number"
                    value={utrNumber}
                    onChange={(e) => setUtrNumber(e.target.value)}
                    required
                    data-testid="utr-input"
                  />
                  <p className="text-xs text-gray-500">You'll find this in your payment confirmation</p>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-accent hover:bg-accent/90 py-6 text-lg"
                  disabled={loading}
                  data-testid="submit-payment-btn"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Submitting...
                    </>
                  ) : (
                    'Submit Payment Details'
                  )}
                </Button>
              </form>

              <p className="text-xs text-gray-500 text-center">
                Your access will be activated within 24 hours of payment verification
              </p>
            </div>
          </Card>
        </div>

        {/* Contact Support */}
        <Card className="card-base p-6 mt-8 text-center">
          <p className="text-sm text-gray-600">
            Having trouble with payment? Contact us:
            <br />
            <span className="font-semibold text-primary">6200488068</span> | <span className="font-semibold text-primary">shubhamrajsingh1712@gmail.com</span>
          </p>
        </Card>
      </div>
    </div>
  );
}
