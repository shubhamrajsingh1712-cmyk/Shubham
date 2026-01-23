import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';
import axios from 'axios';
import { TrendingUp, LogOut, FileText, Calendar, Award, Download, PlayCircle } from 'lucide-react';

const API_URL = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function StudentDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [tests, setTests] = useState([]);
  const [reports, setReports] = useState([]);
  const [counsellingSessions, setCounsellingSessions] = useState([]);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      const [testsRes, reportsRes, counsellingRes, paymentsRes] = await Promise.all([
        axios.get(`${API_URL}/tests/user/${user.id}`),
        axios.get(`${API_URL}/reports/user/${user.id}`),
        axios.get(`${API_URL}/counselling/user/${user.id}`),
        axios.get(`${API_URL}/payments/user/${user.id}`)
      ]);

      setTests(testsRes.data);
      setReports(reportsRes.data);
      setCounsellingSessions(counsellingRes.data);
      setPayments(paymentsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
    toast.success('Logged out successfully');
  };

  const testTypes = [
    { id: 'orientation', name: 'Work Orientation', description: 'Discover your work style preferences' },
    { id: 'personality', name: 'Personality Profile', description: 'Understand your personality traits' },
    { id: 'aptitude', name: 'Aptitude Assessment', description: 'Test your cognitive abilities' },
    { id: 'eq', name: 'Emotional Intelligence', description: 'Measure your EQ factors' }
  ];

  const isTestCompleted = (testType) => {
    return tests.some(test => test.test_type === testType);
  };

  const getCompletionPercentage = () => {
    const completedTests = testTypes.filter(t => isTestCompleted(t.id)).length;
    return (completedTests / testTypes.length) * 100;
  };

  const handleDownloadReport = async (reportId) => {
    try {
      const response = await axios.get(`${API_URL}/reports/download/${reportId}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `career_report_${reportId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Report downloaded successfully');
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download report');
    }
  };

  const handleGenerateReport = async () => {
    try {
      const response = await axios.post(`${API_URL}/reports/generate/${user.id}`);
      toast.success('Report generated successfully!');
      fetchDashboardData();
    } catch (error) {
      console.error('Report generation error:', error);
      toast.error(error.response?.data?.detail || 'Failed to generate report');
    }
  };

  const handleBookCounselling = async () => {
    try {
      await axios.post(`${API_URL}/counselling/book?user_id=${user.id}`);
      toast.success('Counselling session booked! We will contact you soon.');
      fetchDashboardData();
    } catch (error) {
      console.error('Booking error:', error);
      toast.error('Failed to book counselling session');
    }
  };

  const hasVerifiedPayment = payments.some(p => p.status === 'completed');
  const allTestsCompleted = getCompletionPercentage() === 100;

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="bg-white border-b border-black/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white" size={24} />
              </div>
              <span className="text-xl font-heading font-bold text-primary">BoatMyCareer</span>
            </div>
            <Button variant="outline" onClick={handleLogout} data-testid="logout-btn">
              <LogOut size={18} className="mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-heading font-bold text-primary mb-2" data-testid="dashboard-welcome">
            Welcome back, {user?.full_name}!
          </h1>
          <p className="text-gray-600">Track your progress and continue your career discovery journey</p>
        </div>

        {/* Payment Status Alert */}
        {!hasVerifiedPayment && (
          <Card className="card-base p-6 mb-8 border-l-4 border-accent">
            <div className="flex items-start space-x-4">
              <FileText className="text-accent flex-shrink-0 mt-1" size={24} />
              <div>
                <h3 className="font-semibold mb-2">Payment Verification Pending</h3>
                <p className="text-sm text-gray-600">
                  Your payment is being verified. You'll be able to access the assessment once verification is complete (within 24 hours).
                </p>
              </div>
            </div>
          </Card>
        )}

        {/* Progress Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="card-base p-6" data-testid="tests-completed-card">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <PlayCircle className="text-primary" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Tests Completed</p>
                <p className="text-2xl font-bold text-primary">{tests.length}/{testTypes.length}</p>
              </div>
            </div>
          </Card>

          <Card className="card-base p-6" data-testid="reports-card">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center">
                <FileText className="text-secondary" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Reports</p>
                <p className="text-2xl font-bold text-secondary">{reports.length}</p>
              </div>
            </div>
          </Card>

          <Card className="card-base p-6" data-testid="counselling-card">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center">
                <Calendar className="text-accent" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Counselling Sessions</p>
                <p className="text-2xl font-bold text-accent">{counsellingSessions.length}</p>
              </div>
            </div>
          </Card>

          <Card className="card-base p-6" data-testid="progress-card">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Award className="text-primary" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Overall Progress</p>
                <p className="text-2xl font-bold text-primary">{Math.round(getCompletionPercentage())}%</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Assessment Progress */}
        <Card className="card-base p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-heading font-bold text-primary">Assessment Progress</h2>
            <span className="text-sm text-gray-600">{Math.round(getCompletionPercentage())}% Complete</span>
          </div>
          <Progress value={getCompletionPercentage()} className="mb-6 h-3" />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {testTypes.map(test => {
              const completed = isTestCompleted(test.id);
              return (
                <div 
                  key={test.id} 
                  className={`p-4 rounded-lg border-2 ${completed ? 'border-secondary bg-secondary/5' : 'border-gray-200'}`}
                  data-testid={`test-${test.id}-status`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold mb-1">{test.name}</h3>
                      <p className="text-sm text-gray-600">{test.description}</p>
                    </div>
                    {completed ? (
                      <div className="flex items-center text-secondary font-medium">
                        <Award size={20} className="mr-2" />
                        Done
                      </div>
                    ) : (
                      <Link to={`/assessment/${test.id}`}>
                        <Button 
                          size="sm" 
                          disabled={!hasVerifiedPayment}
                          data-testid={`start-${test.id}-btn`}
                        >
                          Start
                        </Button>
                      </Link>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {allTestsCompleted && reports.length === 0 && (
            <div className="mt-6 text-center">
              <Button 
                className="bg-accent hover:bg-accent/90" 
                onClick={handleGenerateReport}
                data-testid="generate-report-btn"
              >
                <FileText className="mr-2" size={18} />
                Generate Your Career Report
              </Button>
            </div>
          )}
        </Card>

        {/* Reports Section */}
        {reports.length > 0 && (
          <Card className="card-base p-8 mb-8">
            <h2 className="text-2xl font-heading font-bold text-primary mb-6">Your Reports</h2>
            <div className="space-y-4">
              {reports.map(report => (
                <div key={report.id} className="flex items-center justify-between p-4 bg-subtle rounded-lg" data-testid={`report-${report.id}`}>
                  <div>
                    <h3 className="font-semibold">Career Discovery Report</h3>
                    <p className="text-sm text-gray-600">
                      Generated on {new Date(report.generated_at).toLocaleDateString()}
                    </p>
                  </div>
                  <Button 
                    variant="outline"
                    onClick={() => handleDownloadReport(report.id)}
                    data-testid={`download-report-${report.id}-btn`}
                  >
                    <Download size={18} className="mr-2" />
                    Download PDF
                  </Button>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Counselling Section */}
        <Card className="card-base p-8">
          <h2 className="text-2xl font-heading font-bold text-primary mb-6">Counselling Sessions</h2>
          
          {counsellingSessions.length === 0 ? (
            <div className="text-center py-8">
              <Calendar className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600 mb-4">No counselling sessions booked yet</p>
              <Button 
                className="bg-accent hover:bg-accent/90"
                onClick={handleBookCounselling}
                disabled={!allTestsCompleted}
                data-testid="book-counselling-btn"
              >
                <Calendar className="mr-2" size={18} />
                Book Counselling Session
              </Button>
              {!allTestsCompleted && (
                <p className="text-sm text-gray-500 mt-2">Complete all tests to book counselling</p>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {counsellingSessions.map(session => (
                <div key={session.id} className="p-4 bg-subtle rounded-lg" data-testid={`session-${session.id}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold">Counselling with {session.counsellor_name}</h3>
                      <p className="text-sm text-gray-600">Status: {session.status}</p>
                      {session.scheduled_date && (
                        <p className="text-sm text-gray-600">
                          Scheduled: {new Date(session.scheduled_date).toLocaleDateString()}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
