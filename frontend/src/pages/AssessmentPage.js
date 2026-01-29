import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';
import axios from 'axios';
import { TrendingUp, ArrowLeft, ArrowRight, Loader2 } from 'lucide-react';

const API_URL = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function AssessmentPage() {
  const { testType } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchQuestions();
  }, [testType]);

  const fetchQuestions = async () => {
    try {
      const response = await axios.get(`${API_URL}/questions/${testType}`);
      setQuestions(response.data.questions);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch questions:', error);
      toast.error('Failed to load assessment questions');
      navigate('/dashboard');
    }
  };

  const handleResponse = (questionId, value) => {
    setResponses({
      ...responses,
      [questionId]: value
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    // Check if all questions are answered
    const unanswered = questions.filter(q => !responses[q.id]);
    if (unanswered.length > 0) {
      toast.error(`Please answer all questions. ${unanswered.length} remaining.`);
      // Jump to first unanswered question
      const firstUnansweredIndex = questions.findIndex(q => !responses[q.id]);
      if (firstUnansweredIndex !== -1) {
        setCurrentQuestion(firstUnansweredIndex);
      }
      return;
    }

    setSubmitting(true);

    try {
      // All questions are now Likert scale (1-5)
      const formattedResponses = questions.map(q => ({
        question_id: q.id,
        response: parseInt(responses[q.id])
      }));

      await axios.post(`${API_URL}/tests/submit`, {
        user_id: user.id,
        test_type: testType,
        responses: formattedResponses
      });

      toast.success('Assessment completed successfully!');
      navigate('/dashboard');
    } catch (error) {
      console.error('Submission error:', error);
      toast.error('Failed to submit assessment. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const getTestTitle = () => {
    const titles = {
      orientation: 'Work Orientation Assessment',
      interest: 'Interest Mapping Assessment',
      personality: 'Personality Profile Assessment',
      aptitude: 'Aptitude Assessment',
      eq: 'Emotional Intelligence Assessment'
    };
    return titles[testType] || 'Assessment';
  };

  const progress = ((currentQuestion + 1) / questions.length) * 100;
  const answeredCount = Object.keys(responses).length;

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="animate-spin text-primary" size={48} />
      </div>
    );
  }

  const question = questions[currentQuestion];

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
            <Button 
              variant="outline" 
              onClick={() => navigate('/dashboard')}
              data-testid="back-to-dashboard-btn"
            >
              <ArrowLeft size={18} className="mr-2" />
              Back to Dashboard
            </Button>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-heading font-bold text-primary mb-4" data-testid="assessment-title">
            {getTestTitle()}
          </h1>
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-gray-600">
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <span className="text-sm font-medium text-primary">
              {answeredCount}/{questions.length} Answered
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Question Card */}
        <Card className="card-base p-8 mb-6">
          <h2 className="text-xl font-semibold mb-6" data-testid="question-text">
            {question.question}
          </h2>

          {question.type === 'scale' ? (
            <div className="space-y-4">
              <RadioGroup 
                value={responses[question.id]?.toString()} 
                onValueChange={(val) => handleResponse(question.id, val)}
              >
                {[1, 2, 3, 4, 5].map(value => (
                  <div key={value} className="flex items-center space-x-3" data-testid={`scale-option-${value}`}>
                    <RadioGroupItem value={value.toString()} id={`${question.id}-${value}`} />
                    <Label htmlFor={`${question.id}-${value}`} className="cursor-pointer flex-1">
                      {value === 1 && 'Strongly Disagree'}
                      {value === 2 && 'Disagree'}
                      {value === 3 && 'Neutral'}
                      {value === 4 && 'Agree'}
                      {value === 5 && 'Strongly Agree'}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>
          ) : (
            <div className="space-y-4">
              <RadioGroup 
                value={responses[question.id]} 
                onValueChange={(val) => handleResponse(question.id, val)}
              >
                {question.options.map((option, idx) => (
                  <div key={idx} className="flex items-center space-x-3" data-testid={`mcq-option-${idx}`}>
                    <RadioGroupItem value={option} id={`${question.id}-${idx}`} />
                    <Label htmlFor={`${question.id}-${idx}`} className="cursor-pointer flex-1">
                      {option}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>
          )}
        </Card>

        {/* Navigation Buttons */}
        <div className="flex justify-between items-center">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            data-testid="previous-btn"
          >
            <ArrowLeft size={18} className="mr-2" />
            Previous
          </Button>

          {currentQuestion === questions.length - 1 ? (
            <Button
              className="bg-accent hover:bg-accent/90"
              onClick={handleSubmit}
              disabled={submitting}
              data-testid="submit-assessment-btn"
            >
              {submitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Submitting...
                </>
              ) : (
                'Submit Assessment'
              )}
            </Button>
          ) : (
            <Button
              onClick={handleNext}
              data-testid="next-btn"
            >
              Next
              <ArrowRight size={18} className="ml-2" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
