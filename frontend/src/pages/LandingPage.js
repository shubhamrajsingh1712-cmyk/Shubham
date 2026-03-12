import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Phone, Mail, CheckCircle, TrendingUp, Users, Award, BookOpen, FileText, ArrowRight } from 'lucide-react';
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

      {/* Sample Report Section */}
      <section id="sample-report" className="py-16 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-primary mb-4">
              Sample Assessment Report
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Below is a sample of the comprehensive 20-25 page career discovery report that students receive 
              after completing their psychometric assessment.
            </p>
          </div>

          {/* Sample Report Preview */}
          <div className="max-w-5xl mx-auto">
            <Card className="card-base p-8 md:p-12 border-2 border-primary/20">
              {/* Report Header */}
              <div className="text-center mb-8 pb-6 border-b-2 border-primary/10">
                <div className="inline-block bg-primary/10 px-4 py-1 rounded-full mb-3">
                  <span className="text-xs font-semibold text-primary uppercase tracking-wide">Sample Report</span>
                </div>
                <h3 className="text-3xl font-heading font-bold text-primary mb-2">
                  Career Discovery Report
                </h3>
                <p className="text-gray-600">Comprehensive Psychometric Assessment</p>
              </div>

              {/* Student Profile Card */}
              <div className="bg-subtle rounded-xl p-6 mb-8">
                <h4 className="font-heading font-semibold text-lg text-primary mb-4">Student Profile</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Student Name</p>
                    <p className="font-semibold">Prashant Shivam</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Class</p>
                    <p className="font-semibold">10th Standard</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 mb-1">School</p>
                    <p className="font-semibold">DAV Public School</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Location</p>
                    <p className="font-semibold">Patna, Bihar</p>
                  </div>
                </div>
              </div>

              {/* Executive Summary */}
              <div className="mb-8">
                <h4 className="font-heading font-semibold text-xl text-primary mb-4 flex items-center">
                  <span className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm mr-3">1</span>
                  Executive Summary
                </h4>
                <div className="pl-11">
                  <p className="text-gray-700 mb-4 leading-relaxed">
                    Prashant demonstrates a strong analytical orientation combined with high technological aptitude. 
                    His assessment reveals excellent problem-solving abilities and a natural inclination towards 
                    STEM fields. The results indicate strong potential in engineering, technology, and research-oriented careers.
                  </p>
                  
                  {/* Top Strengths */}
                  <div className="bg-white rounded-lg border border-secondary/20 p-4 mb-4">
                    <h5 className="font-semibold text-sm text-secondary mb-3">Top 5 Strengths Identified:</h5>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="text-secondary" size={16} />
                        <span className="text-sm">Analytical Thinking (86%)</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="text-secondary" size={16} />
                        <span className="text-sm">Technological Understanding (84%)</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="text-secondary" size={16} />
                        <span className="text-sm">Logical Reasoning (82%)</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="text-secondary" size={16} />
                        <span className="text-sm">STEM Interest (81%)</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="text-secondary" size={16} />
                        <span className="text-sm">Perseverance (79%)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Dimension Scores Overview */}
              <div className="mb-8">
                <h4 className="font-heading font-semibold text-xl text-primary mb-4 flex items-center">
                  <span className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center text-white text-sm mr-3">2</span>
                  5-Dimensional Assessment Scores
                </h4>
                <div className="pl-11 space-y-4">
                  {/* Orientation Score */}
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">Work Orientation</span>
                      <span className="text-sm font-bold text-primary">Analytical: 86%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-primary h-2 rounded-full" style={{width: '86%'}}></div>
                    </div>
                    <p className="text-xs text-gray-600 mt-2">Strong analytical orientation with systematic problem-solving approach</p>
                  </div>

                  {/* Interest Score */}
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">Interest Mapping</span>
                      <span className="text-sm font-bold text-secondary">STEM: 81%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-secondary h-2 rounded-full" style={{width: '81%'}}></div>
                    </div>
                    <p className="text-xs text-gray-600 mt-2">High interest in Science, Technology, Engineering & Mathematics</p>
                  </div>

                  {/* Personality Score */}
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">Personality Profile</span>
                      <span className="text-sm font-bold text-accent">Self-Discipline: 79%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-accent h-2 rounded-full" style={{width: '79%'}}></div>
                    </div>
                    <p className="text-xs text-gray-600 mt-2">Strong perseverance, self-discipline, and decision-making abilities</p>
                  </div>

                  {/* Aptitude Score */}
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">Cognitive Aptitude</span>
                      <span className="text-sm font-bold text-primary">Tech Understanding: 84%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-primary h-2 rounded-full" style={{width: '84%'}}></div>
                    </div>
                    <p className="text-xs text-gray-600 mt-2">Excellent technological aptitude and numerical problem-solving skills</p>
                  </div>

                  {/* EQ Score */}
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">Emotional Intelligence</span>
                      <span className="text-sm font-bold text-secondary">Motivation: 76%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-secondary h-2 rounded-full" style={{width: '76%'}}></div>
                    </div>
                    <p className="text-xs text-gray-600 mt-2">Good emotional awareness and strong internal motivation</p>
                  </div>
                </div>
              </div>

              {/* Career Recommendations */}
              <div className="mb-8">
                <h4 className="font-heading font-semibold text-xl text-primary mb-4 flex items-center">
                  <span className="w-8 h-8 bg-accent rounded-full flex items-center justify-center text-white text-sm mr-3">3</span>
                  Top Career Recommendations
                </h4>
                <div className="pl-11">
                  <p className="text-gray-700 mb-4">
                    Based on Prashant's assessment results, the following career paths align strongly with his 
                    orientation, interests, aptitude, and personality profile:
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[
                      { name: 'Software Engineer', match: '94%', stream: 'Science (PCM)' },
                      { name: 'Data Scientist', match: '91%', stream: 'Science (PCM)' },
                      { name: 'Computer Systems Analyst', match: '89%', stream: 'Science (PCM)' },
                      { name: 'Mechanical Engineer', match: '87%', stream: 'Science (PCM)' },
                      { name: 'Research Scientist', match: '85%', stream: 'Science (PCB/PCM)' },
                      { name: 'Robotics Engineer', match: '84%', stream: 'Science (PCM)' }
                    ].map((career, idx) => (
                      <div key={idx} className="bg-white border-2 border-primary/10 rounded-lg p-4 hover:border-primary/30 transition-all">
                        <div className="flex items-start justify-between mb-2">
                          <h5 className="font-semibold text-primary">{career.name}</h5>
                          <span className="text-xs font-bold bg-secondary/20 text-secondary px-2 py-1 rounded">
                            {career.match} Match
                          </span>
                        </div>
                        <p className="text-xs text-gray-600">Recommended Stream: {career.stream}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Stream Recommendation */}
              <div className="mb-8">
                <h4 className="font-heading font-semibold text-xl text-primary mb-4 flex items-center">
                  <span className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-sm mr-3">4</span>
                  Stream & Subject Recommendation
                </h4>
                <div className="pl-11">
                  <div className="bg-primary/5 border-l-4 border-primary rounded-r-lg p-6">
                    <h5 className="font-bold text-lg text-primary mb-3">Recommended Stream: Science (PCM)</h5>
                    <p className="text-gray-700 mb-4">
                      Based on strong analytical orientation, STEM interest, and technological aptitude, 
                      Science stream with Physics, Chemistry, and Mathematics is highly recommended for Class 11-12.
                    </p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="bg-white rounded-lg p-3 text-center border border-primary/20">
                        <p className="text-xs text-gray-600 mb-1">Core Subject</p>
                        <p className="font-semibold text-primary">Physics</p>
                      </div>
                      <div className="bg-white rounded-lg p-3 text-center border border-primary/20">
                        <p className="text-xs text-gray-600 mb-1">Core Subject</p>
                        <p className="font-semibold text-primary">Chemistry</p>
                      </div>
                      <div className="bg-white rounded-lg p-3 text-center border border-primary/20">
                        <p className="text-xs text-gray-600 mb-1">Core Subject</p>
                        <p className="font-semibold text-primary">Mathematics</p>
                      </div>
                      <div className="bg-white rounded-lg p-3 text-center border border-secondary/20">
                        <p className="text-xs text-gray-600 mb-1">Optional</p>
                        <p className="font-semibold text-secondary">Computer Sc.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Report Footer */}
              <div className="border-t-2 border-gray-200 pt-6 mt-8">
                <div className="bg-subtle rounded-lg p-6">
                  <div className="flex items-start space-x-4">
                    <FileText className="text-primary flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h5 className="font-heading font-semibold mb-2">Complete Report Includes:</h5>
                      <ul className="text-sm text-gray-700 space-y-1">
                        <li>• Detailed 3-4 page analysis for each of the 5 dimensions</li>
                        <li>• Radar charts and bar graphs for visual understanding</li>
                        <li>• 10-15 career recommendations with detailed pathways</li>
                        <li>• Entrance exam guidance and top institution recommendations</li>
                        <li>• Personality insights and behavioral analysis</li>
                        <li>• Development roadmap with actionable recommendations</li>
                        <li>• Career progression timelines (Class 9-12 → UG → PG → Career)</li>
                      </ul>
                      <p className="text-sm text-primary font-semibold mt-4">
                        Total Pages: 20-25 | Format: PDF | Downloadable & Printable
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </Card>

            {/* CTA */}
            <div className="text-center mt-8">
              <p className="text-gray-600 mb-4">
                Get your own personalized 20-25 page career discovery report
              </p>
              <Button 
                size="lg" 
                className="bg-accent hover:bg-accent/90 text-white px-8"
                onClick={handleGetStarted}
                data-testid="get-report-btn"
              >
                Start Your Assessment
              </Button>
            </div>
          </div>
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
              { name: 'Engineering & Technology', count: '50+', id: 'eng', color: 'bg-blue-50 border-blue-200' },
              { name: 'Medical & Healthcare', count: '45+', id: 'med', color: 'bg-green-50 border-green-200' },
              { name: 'Business & Commerce', count: '50+', id: 'biz', color: 'bg-purple-50 border-purple-200' },
              { name: 'Arts & Design', count: '35+', id: 'art', color: 'bg-pink-50 border-pink-200' },
              { name: 'Science & Research', count: '35+', id: 'sci', color: 'bg-teal-50 border-teal-200' },
              { name: 'Law & Legal Services', count: '20+', id: 'law', color: 'bg-amber-50 border-amber-200' },
              { name: 'Education & Training', count: '20+', id: 'edu', color: 'bg-indigo-50 border-indigo-200' },
              { name: 'Government Services', count: '20+', id: 'gov', color: 'bg-red-50 border-red-200' }
            ].map((domain, index) => (
              <Link key={index} to={`/careers?category=${domain.id}`}>
                <Card className={`card-base ${domain.color} border-2 hover:shadow-lg transition-all cursor-pointer h-full`}>
                  <div className="p-6 text-center">
                    <h3 className="font-heading font-semibold text-base mb-2 text-primary">
                      {domain.name}
                    </h3>
                    <p className="text-2xl font-bold text-secondary">{domain.count}</p>
                    <p className="text-xs text-gray-600 mt-1">Careers</p>
                  </div>
                </Card>
              </Link>
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
              <Link to="/careers">
                <Button 
                  size="lg" 
                  className="bg-secondary hover:bg-secondary/90 text-white px-8"
                  data-testid="explore-careers-btn"
                >
                  Explore All Careers <ArrowRight className="ml-2" size={18} />
                </Button>
              </Link>
              <p className="text-sm text-gray-600 mt-3">
                Browse independently or get personalized recommendations after taking the assessment
              </p>
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
