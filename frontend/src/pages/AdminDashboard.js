import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';
import axios from 'axios';
import { TrendingUp, LogOut, Users, FileText, Calendar, CreditCard, CheckCircle } from 'lucide-react';

const API_URL = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function AdminDashboard() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [payments, setPayments] = useState([]);
  const [reports, setReports] = useState([]);
  const [counselling, setCounselling] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const [usersRes, paymentsRes, reportsRes, counsellingRes] = await Promise.all([
        axios.get(`${API_URL}/admin/users`),
        axios.get(`${API_URL}/admin/payments`),
        axios.get(`${API_URL}/admin/reports`),
        axios.get(`${API_URL}/admin/counselling`)
      ]);

      setUsers(usersRes.data);
      setPayments(paymentsRes.data);
      setReports(reportsRes.data);
      setCounselling(counsellingRes.data);
    } catch (error) {
      console.error('Failed to fetch admin data:', error);
      toast.error('Failed to load admin data');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
    toast.success('Logged out successfully');
  };

  const handleVerifyPayment = async (paymentId) => {
    try {
      await axios.patch(`${API_URL}/payments/${paymentId}/verify`);
      toast.success('Payment verified successfully');
      fetchAdminData();
    } catch (error) {
      console.error('Verification error:', error);
      toast.error('Failed to verify payment');
    }
  };

  const getUserEmail = (userId) => {
    const user = users.find(u => u.id === userId);
    return user?.email || 'N/A';
  };

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
              <span className="text-xl font-heading font-bold text-primary">BoatMyCareer Admin</span>
            </div>
            <Button variant="outline" onClick={handleLogout} data-testid="admin-logout-btn">
              <LogOut size={18} className="mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="card-base p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Users className="text-primary" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Students</p>
                <p className="text-2xl font-bold text-primary">{users.length}</p>
              </div>
            </div>
          </Card>

          <Card className="card-base p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center">
                <CreditCard className="text-accent" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Payments</p>
                <p className="text-2xl font-bold text-accent">{payments.length}</p>
              </div>
            </div>
          </Card>

          <Card className="card-base p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center">
                <FileText className="text-secondary" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Reports Generated</p>
                <p className="text-2xl font-bold text-secondary">{reports.length}</p>
              </div>
            </div>
          </Card>

          <Card className="card-base p-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Calendar className="text-primary" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600">Counselling Sessions</p>
                <p className="text-2xl font-bold text-primary">{counselling.length}</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Tabs */}
        <Card className="card-base p-8">
          <Tabs defaultValue="users" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="users" data-testid="tab-users">Students</TabsTrigger>
              <TabsTrigger value="payments" data-testid="tab-payments">Payments</TabsTrigger>
              <TabsTrigger value="reports" data-testid="tab-reports">Reports</TabsTrigger>
              <TabsTrigger value="counselling" data-testid="tab-counselling">Counselling</TabsTrigger>
            </TabsList>

            {/* Users Tab */}
            <TabsContent value="users" className="mt-6">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Class</TableHead>
                      <TableHead>School</TableHead>
                      <TableHead>Joined</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {users.map(user => (
                      <TableRow key={user.id} data-testid={`user-row-${user.id}`}>
                        <TableCell className="font-medium">{user.full_name}</TableCell>
                        <TableCell>{user.email}</TableCell>
                        <TableCell>{user.class_level || 'N/A'}</TableCell>
                        <TableCell>{user.school_name || 'N/A'}</TableCell>
                        <TableCell>{new Date(user.created_at).toLocaleDateString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>

            {/* Payments Tab */}
            <TabsContent value="payments" className="mt-6">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>User Email</TableHead>
                      <TableHead>Program</TableHead>
                      <TableHead>Amount</TableHead>
                      <TableHead>UTR</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Action</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {payments.map(payment => (
                      <TableRow key={payment.id} data-testid={`payment-row-${payment.id}`}>
                        <TableCell>{getUserEmail(payment.user_id)}</TableCell>
                        <TableCell>{payment.program_type}</TableCell>
                        <TableCell>₹{payment.amount}</TableCell>
                        <TableCell>{payment.utr_number || 'N/A'}</TableCell>
                        <TableCell>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${payment.status === 'completed' ? 'bg-secondary/20 text-secondary' : 'bg-yellow-100 text-yellow-800'}`}>
                            {payment.status}
                          </span>
                        </TableCell>
                        <TableCell>{new Date(payment.created_at).toLocaleDateString()}</TableCell>
                        <TableCell>
                          {payment.status === 'pending' && (
                            <Button 
                              size="sm" 
                              variant="outline"
                              onClick={() => handleVerifyPayment(payment.id)}
                              data-testid={`verify-payment-${payment.id}-btn`}
                            >
                              <CheckCircle size={16} className="mr-1" />
                              Verify
                            </Button>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>

            {/* Reports Tab */}
            <TabsContent value="reports" className="mt-6">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>User Email</TableHead>
                      <TableHead>Generated Date</TableHead>
                      <TableHead>Career Recommendations</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {reports.map(report => (
                      <TableRow key={report.id} data-testid={`report-row-${report.id}`}>
                        <TableCell>{getUserEmail(report.user_id)}</TableCell>
                        <TableCell>{new Date(report.generated_at).toLocaleDateString()}</TableCell>
                        <TableCell>{report.career_recommendations?.length || 0} careers</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>

            {/* Counselling Tab */}
            <TabsContent value="counselling" className="mt-6">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>User Email</TableHead>
                      <TableHead>Counsellor</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Scheduled Date</TableHead>
                      <TableHead>Created</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {counselling.map(session => (
                      <TableRow key={session.id} data-testid={`counselling-row-${session.id}`}>
                        <TableCell>{getUserEmail(session.user_id)}</TableCell>
                        <TableCell>{session.counsellor_name}</TableCell>
                        <TableCell>
                          <span className="px-2 py-1 rounded text-xs font-medium bg-primary/20 text-primary">
                            {session.status}
                          </span>
                        </TableCell>
                        <TableCell>
                          {session.scheduled_date ? new Date(session.scheduled_date).toLocaleDateString() : 'Not scheduled'}
                        </TableCell>
                        <TableCell>{new Date(session.created_at).toLocaleDateString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>
          </Tabs>
        </Card>
      </div>
    </div>
  );
}
