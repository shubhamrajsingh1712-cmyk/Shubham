import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import {
  TrendingUp, ArrowLeft, GraduationCap, Building, IndianRupee,
  ChevronRight, Lightbulb, AlertTriangle, BookOpen, Briefcase, Star
} from 'lucide-react';
import axios from 'axios';

const API_URL = `${process.env.REACT_APP_BACKEND_URL}/api`;

const GROWTH_STYLES = {
  Excellent: { bg: "bg-green-50 border-green-200", text: "text-green-700", dot: "bg-green-500" },
  Good: { bg: "bg-blue-50 border-blue-200", text: "text-blue-700", dot: "bg-blue-500" },
  Moderate: { bg: "bg-yellow-50 border-yellow-200", text: "text-yellow-700", dot: "bg-yellow-500" },
  Emerging: { bg: "bg-purple-50 border-purple-200", text: "text-purple-700", dot: "bg-purple-500" },
};

export default function CareerDetailPage() {
  const { slug } = useParams();
  const [career, setCareer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get(`${API_URL}/careers/${slug}`)
      .then(res => setCareer(res.data))
      .catch(() => setCareer(null))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
    </div>
  );

  if (!career) return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center">
      <h2 className="text-2xl font-heading font-bold text-primary mb-4">Career not found</h2>
      <Link to="/careers"><Button>Back to Career Library</Button></Link>
    </div>
  );

  const gs = GROWTH_STYLES[career.growth_outlook] || GROWTH_STYLES.Good;

  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="bg-white border-b border-black/5 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white" size={24} />
              </div>
              <span className="text-xl font-heading font-bold text-primary">BoatMyCareer</span>
            </Link>
            <Link to="/careers">
              <Button variant="ghost" size="sm" data-testid="back-to-library">
                <ArrowLeft size={16} className="mr-1" /> Career Library
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-6" data-testid="career-breadcrumb">
          <Link to="/careers" className="hover:text-primary transition-colors">Career Library</Link>
          <ChevronRight size={14} />
          <Link to={`/careers?category=${career.category}`} className="hover:text-primary transition-colors">{career.category_name}</Link>
          <ChevronRight size={14} />
          <span className="text-gray-900 font-medium">{career.name}</span>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-wrap items-start gap-3 mb-3">
            <h1 className="text-3xl sm:text-4xl font-heading font-bold text-primary" data-testid="career-name">
              {career.name}
            </h1>
            <span className={`text-sm font-semibold px-3 py-1 rounded-full border ${gs.bg} ${gs.text}`}>
              {career.growth_outlook} Growth
            </span>
          </div>
          <p className="text-lg text-gray-600 mb-2">{career.description}</p>
          <div className="flex flex-wrap gap-3 text-sm text-gray-500">
            <span className="flex items-center gap-1"><BookOpen size={14} /> {career.stream}</span>
            <span className="flex items-center gap-1"><Briefcase size={14} /> {career.category_name}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Nature of Work */}
            <Card className="card-base p-6" data-testid="nature-of-work-section">
              <h2 className="text-xl font-heading font-semibold text-primary mb-3 flex items-center gap-2">
                <Briefcase size={20} /> Nature of Work
              </h2>
              <p className="text-gray-700 leading-relaxed">{career.nature_of_work}</p>
            </Card>

            {/* Skills Required */}
            <Card className="card-base p-6" data-testid="skills-section">
              <h2 className="text-xl font-heading font-semibold text-primary mb-4 flex items-center gap-2">
                <Star size={20} /> Skills Required
              </h2>
              <div className="flex flex-wrap gap-2">
                {career.skills_required.map(skill => (
                  <span key={skill} className="bg-primary/5 text-primary border border-primary/10 px-3 py-1.5 rounded-lg text-sm font-medium">
                    {skill}
                  </span>
                ))}
              </div>
            </Card>

            {/* Educational Pathway */}
            <Card className="card-base p-6" data-testid="education-section">
              <h2 className="text-xl font-heading font-semibold text-primary mb-4 flex items-center gap-2">
                <GraduationCap size={20} /> Educational Pathway
              </h2>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">UG</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Undergraduate</h4>
                    <p className="text-gray-600 text-sm">{career.education.undergraduate}</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">PG</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Postgraduate</h4>
                    <p className="text-gray-600 text-sm">{career.education.postgraduate}</p>
                  </div>
                </div>
              </div>
            </Card>

            {/* Entrance Exams */}
            <Card className="card-base p-6" data-testid="exams-section">
              <h2 className="text-xl font-heading font-semibold text-primary mb-4 flex items-center gap-2">
                <BookOpen size={20} /> Entrance Exams
              </h2>
              <div className="flex flex-wrap gap-2">
                {career.entrance_exams.map(exam => (
                  <span key={exam} className="bg-accent/5 text-accent border border-accent/10 px-3 py-1.5 rounded-lg text-sm font-medium">
                    {exam}
                  </span>
                ))}
              </div>
            </Card>

            {/* Top Institutions */}
            <Card className="card-base p-6" data-testid="institutions-section">
              <h2 className="text-xl font-heading font-semibold text-primary mb-4 flex items-center gap-2">
                <Building size={20} /> Top Institutions
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {career.top_institutions.map((inst, i) => (
                  <div key={inst} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                    <span className="w-6 h-6 bg-primary/10 text-primary text-xs font-bold rounded-full flex items-center justify-center flex-shrink-0">
                      {i + 1}
                    </span>
                    <span className="text-sm font-medium text-gray-700">{inst}</span>
                  </div>
                ))}
              </div>
            </Card>

            {/* Pros & Challenges */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <Card className="card-base p-6 border-l-4 border-l-green-500" data-testid="pros-section">
                <h2 className="text-lg font-heading font-semibold text-green-700 mb-3 flex items-center gap-2">
                  <Lightbulb size={18} /> Advantages
                </h2>
                <ul className="space-y-2">
                  {career.pros.map(pro => (
                    <li key={pro} className="text-sm text-gray-700 flex items-start gap-2">
                      <span className="text-green-500 mt-1.5 flex-shrink-0">+</span>
                      {pro}
                    </li>
                  ))}
                </ul>
              </Card>
              <Card className="card-base p-6 border-l-4 border-l-amber-500" data-testid="challenges-section">
                <h2 className="text-lg font-heading font-semibold text-amber-700 mb-3 flex items-center gap-2">
                  <AlertTriangle size={18} /> Challenges
                </h2>
                <ul className="space-y-2">
                  {career.challenges.map(c => (
                    <li key={c} className="text-sm text-gray-700 flex items-start gap-2">
                      <span className="text-amber-500 mt-1.5 flex-shrink-0">!</span>
                      {c}
                    </li>
                  ))}
                </ul>
              </Card>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Salary Card */}
            <Card className="card-base p-6 border-2 border-primary/10" data-testid="salary-section">
              <h2 className="text-lg font-heading font-semibold text-primary mb-4 flex items-center gap-2">
                <IndianRupee size={18} /> Salary Range
              </h2>
              <div className="space-y-4">
                <div>
                  <p className="text-xs text-gray-500 mb-1">Starting (0-2 years)</p>
                  <p className="text-lg font-bold text-gray-900">{career.salary.starting}</p>
                </div>
                <div className="h-px bg-gray-100" />
                <div>
                  <p className="text-xs text-gray-500 mb-1">Mid-Career (5-8 years)</p>
                  <p className="text-lg font-bold text-primary">{career.salary.mid_career}</p>
                </div>
                <div className="h-px bg-gray-100" />
                <div>
                  <p className="text-xs text-gray-500 mb-1">Senior (10+ years)</p>
                  <p className="text-lg font-bold text-accent">{career.salary.senior}</p>
                </div>
              </div>
            </Card>

            {/* Growth Outlook */}
            <Card className={`card-base p-6 border-2 ${gs.bg}`} data-testid="growth-section">
              <h2 className="text-lg font-heading font-semibold mb-2">Growth Outlook</h2>
              <div className="flex items-center gap-2">
                <span className={`w-3 h-3 rounded-full ${gs.dot}`}></span>
                <span className={`text-xl font-bold ${gs.text}`}>{career.growth_outlook}</span>
              </div>
            </Card>

            {/* Recommended Stream */}
            <Card className="card-base p-6 bg-primary/5" data-testid="stream-section">
              <h2 className="text-lg font-heading font-semibold text-primary mb-2">Recommended Stream</h2>
              <p className="text-base font-bold text-gray-900">{career.stream}</p>
            </Card>

            {/* CTA */}
            <Card className="card-base p-6 bg-accent/5 border-2 border-accent/20">
              <h3 className="font-heading font-semibold text-accent mb-2">Find Your Career Match</h3>
              <p className="text-sm text-gray-600 mb-4">Take our scientific psychometric assessment to discover if this career aligns with your profile.</p>
              <Link to="/register">
                <Button className="w-full bg-accent hover:bg-accent/90 text-white" data-testid="take-assessment-cta">
                  Take Assessment
                </Button>
              </Link>
            </Card>

            {/* Related Careers */}
            {career.related_careers?.length > 0 && (
              <Card className="card-base p-6" data-testid="related-careers-section">
                <h2 className="text-lg font-heading font-semibold text-primary mb-3">Related Careers</h2>
                <div className="space-y-2">
                  {career.related_careers.map(rc => (
                    <Link
                      key={rc.slug}
                      to={`/careers/${rc.slug}`}
                      className="flex items-center justify-between p-2.5 rounded-lg hover:bg-gray-50 transition-colors group"
                      data-testid={`related-career-${rc.slug}`}
                    >
                      <span className="text-sm font-medium text-gray-700 group-hover:text-primary transition-colors">{rc.name}</span>
                      <ChevronRight size={14} className="text-gray-400" />
                    </Link>
                  ))}
                </div>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
