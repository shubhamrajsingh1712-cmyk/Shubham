import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Phone, Mail, CheckCircle, TrendingUp, Users, Award, BookOpen } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export default function LandingPage() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [openFaq, setOpenFaq] = useState(null);

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      navigate('/register');
    }
  };

  const faqs = [
    {
      q: "What is psychometric assessment?",
      a: "A scientific evaluation of your cognitive abilities, personality traits, interests, and emotional intelligence to provide personalized career guidance."
    },
    {
      q: "How long does the assessment take?",
      a: "The complete assessment typically takes 60-90 minutes. You can complete it in multiple sessions."
    },
    {
      q: "Is this suitable for my child's class?",
      a: "Yes! Our assessment is designed for students from Class VII to XII, with age-appropriate questions."
    },
    {
      q: "How do I book counselling?",
      a: "After completing your assessment and receiving your report, you can book a one-on-one counselling session directly from your dashboard."
    },
    {
      q: "What happens after payment?",
      a: "After payment verification (usually within 24 hours), you'll get access to the complete assessment and your personalized dashboard."
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="bg-white border-b border-black/5 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white" size={24} />
              </div>
              <span className="text-xl font-heading font-bold text-primary">BoatMyCareer</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#how-it-works" className="text-sm font-medium hover:text-primary transition-colors">How It Works</a>
              <a href="#pricing" className="text-sm font-medium hover:text-primary transition-colors">Pricing</a>
              <a href="#career-library" className="text-sm font-medium hover:text-primary transition-colors">Career Library</a>
              <a href="#sample-report" className="text-sm font-medium hover:text-primary transition-colors">Sample Report</a>
              <a href="#faq" className="text-sm font-medium hover:text-primary transition-colors">FAQ</a>
              {!isAuthenticated ? (
                <Link to="/login">
                  <Button variant="outline" size="sm" data-testid="nav-login-btn">Login</Button>
                </Link>
              ) : (
                <Link to="/dashboard">
                  <Button size="sm" data-testid="nav-dashboard-btn">Dashboard</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 hero-gradient"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-12 items-center">
            <div className="md:col-span-7 space-y-6">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-heading font-bold text-primary leading-tight">
                Navigate Your Future with Scientific Precision
              </h1>
              <p className="text-lg md:text-xl text-gray-600 leading-relaxed">
                A comprehensive psychometric assessment platform designed for students of Class VII-XII. 
                Discover your strengths, understand your potential, and make informed career decisions.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Button 
                  size="lg" 
                  className="bg-accent hover:bg-accent/90 text-white font-semibold px-8 py-6 text-lg"
                  onClick={handleGetStarted}
                  data-testid="hero-get-started-btn"
                >
                  Start Career Discovery
                </Button>
                <a href="#how-it-works">
                  <Button size="lg" variant="outline" className="px-8 py-6 text-lg" data-testid="hero-learn-more-btn">
                    Learn More
                  </Button>
                </a>
              </div>
              <div className="flex items-center space-x-6 pt-4">
                <div className="flex items-center space-x-2">
                  <Phone className="text-primary" size={20} />
                  <span className="text-sm font-medium">6200488068</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Mail className="text-primary" size={20} />
                  <span className="text-sm font-medium">shubhamrajsingh1712@gmail.com</span>
                </div>
              </div>
            </div>
            <div className="md:col-span-5">
              <img 
                src="https://images.pexels.com/photos/3231359/pexels-photo-3231359.jpeg" 
                alt="Students studying together" 
                className="rounded-2xl shadow-float w-full h-auto"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Why Students Feel Confused */}
      <section className="py-16 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
              Why Students Feel Career Confusion
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Most students choose careers based on marks, peer pressure, or parental expectations. 
              This leads to dissatisfaction, course changes, and wasted years.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="card-base p-8 text-center">
              <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="text-accent" size={32} />
              </div>
              <h3 className="text-xl font-heading font-semibold mb-3">Peer Pressure</h3>
              <p className="text-gray-600">Following what friends choose, not what suits your personality and strengths.</p>
            </Card>
            <Card className="card-base p-8 text-center">
              <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpen className="text-secondary" size={32} />
              </div>
              <h3 className="text-xl font-heading font-semibold mb-3">Marks-Only Focus</h3>
              <p className="text-gray-600">Believing good marks automatically mean career success, ignoring aptitude.</p>
            </Card>
            <Card className="card-base p-8 text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="text-primary" size={32} />
              </div>
              <h3 className="text-xl font-heading font-semibold mb-3">Lack of Awareness</h3>
              <p className="text-gray-600">Limited knowledge about diverse career options and what they truly require.</p>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-16 md:py-24 bg-subtle">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
              How Our Scientific Assessment Works
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              A structured 5-stage process designed to provide deep insights into your career potential
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
            <div className="md:col-span-6">
              <Card className="card-base p-8 h-full">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-white font-bold text-xl">1</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-heading font-semibold mb-2">Career Orientation Session</h3>
                    <p className="text-gray-600">Understanding what career counselling means and why it matters for your future.</p>
                  </div>
                </div>
              </Card>
            </div>
            <div className="md:col-span-6">
              <Card className="card-base p-8 h-full">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-secondary rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-white font-bold text-xl">2</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-heading font-semibold mb-2">5-Dimensional Assessment</h3>
                    <p className="text-gray-600">Work orientation, interests, personality, aptitude, and emotional intelligence evaluation.</p>
                  </div>
                </div>
              </Card>
            </div>
            <div className="md:col-span-4">
              <Card className="card-base p-8 h-full">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-white font-bold text-xl">3</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-heading font-semibold mb-2">Detailed Report</h3>
                    <p className="text-gray-600">Comprehensive PDF with charts, analysis, and career recommendations.</p>
                  </div>
                </div>
              </Card>
            </div>
            <div className="md:col-span-4">
              <Card className="card-base p-8 h-full">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-white font-bold text-xl">4</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-heading font-semibold mb-2">Expert Counselling</h3>
                    <p className="text-gray-600">One-on-one session with career expert and parents involvement.</p>
                  </div>
                </div>
              </Card>
            </div>
            <div className="md:col-span-4">
              <Card className="card-base p-8 h-full">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-secondary rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-white font-bold text-xl">5</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-heading font-semibold mb-2">Ongoing Support</h3>
                    <p className="text-gray-600">1-year extended program for continuous career guidance and mentorship.</p>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Founder Section */}
      <section className="py-16 md:py-24 bg-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="card-base p-8 md:p-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
              <div className="md:col-span-1">
                <div className="w-48 h-48 mx-auto bg-primary/10 rounded-full flex items-center justify-center">
                  <Award className="text-primary" size={80} />
                </div>
              </div>
              <div className="md:col-span-2">
                <h2 className="text-3xl font-heading font-bold text-primary mb-4">Meet Your Career Guide</h2>
                <h3 className="text-2xl font-semibold mb-2">Shubham Raj Singh</h3>
                <p className="text-lg text-secondary font-medium mb-4">Practicing Advocate, Delhi High Court & Supreme Court of India</p>
                <p className="text-gray-600 mb-4 leading-relaxed">
                  With extensive experience in law and education, I understand the critical importance of making informed career decisions. 
                  This platform combines scientific assessment methods with personalized guidance to help students discover their true potential.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <a href="tel:6200488068" className="flex items-center space-x-2 text-primary hover:text-primary/80">
                    <Phone size={20} />
                    <span className="font-medium">6200488068</span>
                  </a>
                  <a href="mailto:shubhamrajsingh1712@gmail.com" className="flex items-center space-x-2 text-primary hover:text-primary/80">
                    <Mail size={20} />
                    <span className="font-medium">shubhamrajsingh1712@gmail.com</span>
                  </a>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-16 md:py-24 bg-subtle">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
              Clear, Affordable Pricing
            </h2>
            <p className="text-lg text-gray-600">Invest in your future with our scientifically-backed programs</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            <Card className="card-base p-8 border-2 border-primary/20">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-heading font-bold mb-2">Psychometric Assessment</h3>
                <div className="text-5xl font-bold text-primary mb-2">₹999</div>
                <p className="text-gray-600">Complete career discovery package</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>5-Dimensional Scientific Assessment</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Detailed PDF Report with Charts</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Career Recommendations</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Strengths & Development Areas</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>One-on-One Counselling Session</span>
                </li>
              </ul>
              <Button 
                className="w-full bg-primary hover:bg-primary/90 py-6 text-lg"
                onClick={handleGetStarted}
                data-testid="pricing-test-btn"
              >
                Get Started
              </Button>
            </Card>
            <Card className="card-base p-8 border-2 border-accent">
              <div className="text-center mb-6">
                <div className="inline-block bg-accent text-white px-3 py-1 rounded-full text-sm font-semibold mb-2">RECOMMENDED</div>
                <h3 className="text-2xl font-heading font-bold mb-2">Extended Guidance Program</h3>
                <div className="text-5xl font-bold text-accent mb-2">₹1,000</div>
                <p className="text-gray-600">1-year continuous support</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Everything in Assessment Package</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>12 Months Career Guidance</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Entrance Exam Awareness</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Course & College Guidance</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Ongoing Mentorship Access</span>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                  <span>Regular Opportunity Alerts</span>
                </li>
              </ul>
              <Button 
                className="w-full bg-accent hover:bg-accent/90 py-6 text-lg"
                onClick={handleGetStarted}
                data-testid="pricing-extended-btn"
              >
                Start Extended Program
              </Button>
            </Card>
          </div>
        </div>
      </section>

      {/* Career Library Section */}
      <section id="career-library" className="py-16 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
              Explore 460+ Career Paths
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Browse our comprehensive career library - discover detailed information about diverse career options, 
              educational pathways, entrance exams, and top institutions across 14 major domains.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {[
              { name: 'Engineering & Technology', count: '50+', icon: '⚙️', color: 'bg-blue-50 border-blue-200' },
              { name: 'Medical & Healthcare', count: '45+', icon: '🏥', color: 'bg-green-50 border-green-200' },
              { name: 'Business & Commerce', count: '50+', icon: '💼', color: 'bg-purple-50 border-purple-200' },
              { name: 'Arts & Design', count: '45+', icon: '🎨', color: 'bg-pink-50 border-pink-200' },
              { name: 'Science & Research', count: '35+', icon: '🔬', color: 'bg-teal-50 border-teal-200' },
              { name: 'Law & Legal Services', count: '20+', icon: '⚖️', color: 'bg-amber-50 border-amber-200' },
              { name: 'Education & Training', count: '25+', icon: '📚', color: 'bg-indigo-50 border-indigo-200' },
              { name: 'Government Services', count: '30+', icon: '🏛️', color: 'bg-red-50 border-red-200' }
            ].map((domain, index) => (
              <Card key={index} className={`card-base ${domain.color} border-2 hover:shadow-lg transition-all cursor-pointer`}>
                <div className="p-6 text-center">
                  <div className="text-4xl mb-3">{domain.icon}</div>
                  <h3 className="font-heading font-semibold text-base mb-2 text-primary">
                    {domain.name}
                  </h3>
                  <p className="text-2xl font-bold text-secondary">{domain.count}</p>
                  <p className="text-xs text-gray-600 mt-1">Careers</p>
                </div>
              </Card>
            ))}
          </div>

          <div className="bg-subtle rounded-2xl p-8 md:p-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <h3 className="text-2xl font-heading font-bold text-primary mb-4">
                  Each Career Includes:
                </h3>
                <ul className="space-y-3">
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                    <span>Detailed overview & nature of work</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                    <span>Required skills & qualifications</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                    <span>Educational pathways (Class 9-12 → UG → PG)</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                    <span>Entrance exams & preparation tips</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                    <span>Top 15 institutions in India</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                    <span>Career progression & salary insights</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <CheckCircle className="text-secondary flex-shrink-0 mt-1" size={20} />
                    <span>Pros, challenges & related careers</span>
                  </li>
                </ul>
              </div>
              <div className="relative">
                <div className="bg-white rounded-xl shadow-lg p-6 border border-primary/20">
                  <div className="text-sm text-gray-500 mb-2">Sample Career</div>
                  <h4 className="text-xl font-heading font-bold text-primary mb-3">Software Engineer</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between py-2 border-b">
                      <span className="text-gray-600">Education</span>
                      <span className="font-medium">B.Tech/B.E. in CS</span>
                    </div>
                    <div className="flex justify-between py-2 border-b">
                      <span className="text-gray-600">Avg. Starting Salary</span>
                      <span className="font-medium">₹4-8 LPA</span>
                    </div>
                    <div className="flex justify-between py-2 border-b">
                      <span className="text-gray-600">Top Exam</span>
                      <span className="font-medium">JEE Main/Advanced</span>
                    </div>
                    <div className="flex justify-between py-2">
                      <span className="text-gray-600">Growth Rate</span>
                      <span className="font-medium text-green-600">Excellent ↑</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="text-center mt-8">
              <Button 
                size="lg" 
                className="bg-secondary hover:bg-secondary/90 text-white px-8"
                onClick={handleGetStarted}
                data-testid="explore-careers-btn"
              >
                Explore All Careers
              </Button>
              <p className="text-sm text-gray-600 mt-3">
                Browse independently or get personalized recommendations after taking the assessment
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Sample Report Section */}
      <section id="sample-report" className="py-16 md:py-24 bg-subtle">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
              Detailed Assessment Report
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              After completing your assessment, receive a comprehensive 20-25 page report with 
              in-depth analysis, visual charts, and personalized career recommendations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Report Preview */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-primary/20">
              <div className="mb-6">
                <div className="text-sm text-gray-500 mb-2">Sample Report Sections</div>
                <h3 className="text-2xl font-heading font-bold text-primary">What You'll Receive</h3>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-start space-x-3 p-3 bg-subtle rounded-lg">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">1</div>
                  <div>
                    <h4 className="font-semibold text-primary">Executive Summary</h4>
                    <p className="text-sm text-gray-600">Overall profile with radar charts showing your strengths across 5 dimensions</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-3 bg-subtle rounded-lg">
                  <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">2</div>
                  <div>
                    <h4 className="font-semibold text-primary">Work Orientation Analysis</h4>
                    <p className="text-sm text-gray-600">Detailed 3-4 page analysis of your work style preferences and environment fit</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-3 bg-subtle rounded-lg">
                  <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">3</div>
                  <div>
                    <h4 className="font-semibold text-primary">Interest Mapping</h4>
                    <p className="text-sm text-gray-600">Your interests across STEM, Arts, Business, Healthcare, and Social domains</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-3 bg-subtle rounded-lg">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">4</div>
                  <div>
                    <h4 className="font-semibold text-primary">Personality Profile</h4>
                    <p className="text-sm text-gray-600">8 key personality traits with behavioral insights and leadership potential</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-3 bg-subtle rounded-lg">
                  <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">5</div>
                  <div>
                    <h4 className="font-semibold text-primary">Aptitude & EQ Analysis</h4>
                    <p className="text-sm text-gray-600">Cognitive abilities and emotional intelligence assessment with learning style insights</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-3 bg-subtle rounded-lg">
                  <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">6</div>
                  <div>
                    <h4 className="font-semibold text-primary">Career Recommendations</h4>
                    <p className="text-sm text-gray-600">Top 10-15 personalized career paths with subject selection guidance</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Report Features */}
            <div className="space-y-6">
              <Card className="card-base p-6 bg-white border-2 border-secondary/20">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Award className="text-secondary" size={24} />
                  </div>
                  <div>
                    <h4 className="font-heading font-semibold text-lg mb-2">Visual Analysis</h4>
                    <p className="text-gray-600">
                      Radar charts, bar graphs, and color-coded interpretive bands (Low/Moderate/High) 
                      make complex data easy to understand for both students and parents.
                    </p>
                  </div>
                </div>
              </Card>

              <Card className="card-base p-6 bg-white border-2 border-primary/20">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <BookOpen className="text-primary" size={24} />
                  </div>
                  <div>
                    <h4 className="font-heading font-semibold text-lg mb-2">Expert Interpretation</h4>
                    <p className="text-gray-600">
                      500-700 word detailed interpretation for each dimension, written in simple yet 
                      expert language understandable by students, parents, and counselors.
                    </p>
                  </div>
                </div>
              </Card>

              <Card className="card-base p-6 bg-white border-2 border-accent/20">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <TrendingUp className="text-accent" size={24} />
                  </div>
                  <div>
                    <h4 className="font-heading font-semibold text-lg mb-2">Actionable Roadmap</h4>
                    <p className="text-gray-600">
                      Strengths & development areas with specific recommendations, skill development 
                      strategies, and career pathways showing Class 9-12 → UG → PG progression.
                    </p>
                  </div>
                </div>
              </Card>

              <div className="bg-primary text-white rounded-xl p-6">
                <h4 className="font-heading font-bold text-xl mb-2">20-25 Pages</h4>
                <p className="text-sm opacity-90">
                  Comprehensive analysis across all dimensions with professional formatting, 
                  charts, tables, and counselor-ready insights. Downloaded as a PDF for easy sharing.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-16 md:py-24 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
              Frequently Asked Questions
            </h2>
          </div>
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <Card key={index} className="card-base">
                <button
                  className="w-full text-left p-6 flex justify-between items-start"
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                  data-testid={`faq-question-${index}`}
                >
                  <h3 className="text-lg font-semibold pr-4">{faq.q}</h3>
                  <span className="text-2xl text-primary flex-shrink-0">{openFaq === index ? '−' : '+'}</span>
                </button>
                {openFaq === index && (
                  <div className="px-6 pb-6 text-gray-600" data-testid={`faq-answer-${index}`}>
                    {faq.a}
                  </div>
                )}
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-16 md:py-24 bg-primary text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-heading font-bold mb-4">
            Ready to Discover Your Career Path?
          </h2>
          <p className="text-lg mb-8 opacity-90">
            Join hundreds of students who have found clarity and direction through our scientific assessment
          </p>
          <Button 
            size="lg" 
            className="bg-accent hover:bg-accent/90 text-white font-semibold px-12 py-6 text-lg"
            onClick={handleGetStarted}
            data-testid="final-cta-btn"
          >
            Start Your Journey Today
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-black/5 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                  <TrendingUp className="text-white" size={24} />
                </div>
                <span className="text-xl font-heading font-bold text-primary">BoatMyCareer</span>
              </div>
              <p className="text-sm text-gray-600">Navigate your future with scientific precision</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <div className="space-y-2 text-sm text-gray-600">
                <p>📞 6200488068</p>
                <p>📧 shubhamrajsingh1712@gmail.com</p>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Quick Links</h4>
              <div className="space-y-2 text-sm">
                <a href="#how-it-works" className="block text-gray-600 hover:text-primary">How It Works</a>
                <a href="#pricing" className="block text-gray-600 hover:text-primary">Pricing</a>
                <a href="#faq" className="block text-gray-600 hover:text-primary">FAQ</a>
              </div>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-black/5 text-center text-sm text-gray-600">
            <p>&copy; 2024 BoatMyCareer.com. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
